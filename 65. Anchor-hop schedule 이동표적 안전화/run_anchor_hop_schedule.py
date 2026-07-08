"""65. Anchor-hop schedule 이동표적 안전화.

64번 결론:
  - frequency hop은 DOA 오차 lag-1 자기상관을 낮춘다.
  - 그러나 always-on hop과 단순 DOA R 팽창/jump gate는 이동 표적 RMSE를
    안정적으로 개선하지 못했다.

이번 질문:
  fixed 32 kHz를 동역학 anchor로 유지하고 hop을 sparse probe로 넣으면,
  always-on hop의 tail 악화를 줄이면서 백색화 이점을 일부 유지할 수 있는가?

필터/R 정책은 고정하고 carrier schedule만 바꾼다. 따라서 이번 폴더의 판정은
"R 안전화"가 아니라 "송신 스케줄 설계"에 대한 1차 go/no-go다.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import json

import numpy as np
from scipy.stats import spearmanr, wilcoxon

from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance
from whitening_adaptive import WhiteningAwareAdaptiveRUKF


DISTANCE = 600.0
GEOMS = 4
STEPS = 16
SETTLE_START = 8
FIXED_CARRIER_HZ = 32000.0
HOP_BANK_HZ = np.array([30000.0, 30666.6667, 31333.3333, 32666.6667, 33333.3333, 34000.0])
GEOM_ROOT = 810000
PING_ROOT = 1810000

CONDITIONS = (
    ("radial_0.05", 0.05, "radial", 0.00),
    ("radial_1.0", 1.00, "radial", 0.00),
    ("tangential_1.0", 1.00, "tangential", 0.00),
    ("tang_1.0_vz", 1.00, "tangential", 0.08),
)


def _hop_value(counter: int) -> float:
    return float(HOP_BANK_HZ[counter % len(HOP_BANK_HZ)])


def make_schedule(name: str) -> np.ndarray:
    carriers = np.full(STEPS, FIXED_CARRIER_HZ, dtype=float)
    if name == "fixed":
        return carriers
    if name == "hop_always":
        return np.array([_hop_value(k) for k in range(STEPS)], dtype=float)
    if name == "alternating_fh":
        hop_counter = 0
        for k in range(1, STEPS, 2):
            carriers[k] = _hop_value(hop_counter)
            hop_counter += 1
        return carriers
    if name.startswith("fixed") and name.endswith("_hop1"):
        # e.g. fixed3_hop1 means F,F,F,H,F,F,F,H...
        n_fixed = int(name.removeprefix("fixed").removesuffix("_hop1"))
        period = n_fixed + 1
        hop_counter = 0
        for k in range(STEPS):
            if k % period == n_fixed:
                carriers[k] = _hop_value(hop_counter)
                hop_counter += 1
        return carriers
    if name == "edge_sparse_hop":
        # Keep most pings fixed but insert hop probes at settled-window edges.
        hop_counter = 0
        for k in (3, 7, 11, 15, 19, 23):
            carriers[k] = _hop_value(hop_counter)
            hop_counter += 1
        return carriers
    raise KeyError(name)


POLICIES = {
    "fixed": {"description": "32 kHz fixed carrier"},
    "hop_always": {"description": "all pings use 30~34 kHz hop bank"},
    "alternating_fh": {"description": "fixed, hop alternating; starts from fixed"},
    "fixed3_hop1": {"description": "three fixed anchor pings followed by one hop probe"},
    "fixed4_hop1": {"description": "four fixed anchor pings followed by one hop probe"},
}

SCHEDULES = {name: make_schedule(name) for name in POLICIES}


def geometry(cond_idx: int, index: int):
    rng = np.random.default_rng(GEOM_ROOT + cond_idx * 1000 + index)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    pos = np.array([DISTANCE * np.cos(az), DISTANCE * np.sin(az), -depth])
    env = dict(
        snr_db=float(rng.choice([10.0, 20.0, 30.0])),
        surface_reflection=float(-rng.uniform(0.72, 0.97)),
        bottom_reflection=float(rng.uniform(0.32, 0.78)),
        radial_velocity_m_s=0.0,
    )
    sign = 1.0 if rng.uniform() < 0.5 else -1.0
    return pos, env, az, sign


def truth_trajectory(pos: np.ndarray, az: float, sign: float, speed: float, mode: str, vz: float):
    radial = np.array([np.cos(az), np.sin(az), 0.0])
    tangential = np.array([-np.sin(az), np.cos(az), 0.0])
    v = sign * speed * radial if mode == "radial" else speed * tangential
    v = v + np.array([0.0, 0.0, sign * vz])
    return pos + np.arange(STEPS)[:, None] * v


def collect_one(truth: np.ndarray, env: dict, cond_idx: int, index: int, k: int, carrier: float):
    cfg = replace(
        ChannelConfig(),
        seed=PING_ROOT + cond_idx * 5000 + index * 80 + k,
        carrier_hz=float(carrier),
        **env,
    )
    _, received, _ = synthesize_received(truth[k], cfg)
    z, q = extract_measurement(received, cfg)
    truth_z = ideal_measurement(truth[k], cfg)
    return z, q, float(z[9] - truth_z[9])


def collect_cached(
    truth: np.ndarray,
    env: dict,
    cond_idx: int,
    index: int,
    carriers: np.ndarray,
    cache: dict[tuple[int, float], tuple[np.ndarray, dict, float]],
):
    obs, quals, el_err = [], [], []
    for k, carrier in enumerate(carriers):
        key = (k, float(np.round(carrier, 4)))
        if key not in cache:
            cache[key] = collect_one(truth, env, cond_idx, index, k, carrier)
        z, q, el = cache[key]
        el_err.append(el)
        obs.append(z)
        quals.append(q)
    return np.asarray(obs), quals, np.asarray(el_err)


def lag1_autocorr(x: np.ndarray) -> float:
    x = np.asarray(x, float)
    a, b = x[:-1] - x[:-1].mean(), x[1:] - x[1:].mean()
    denom = np.sqrt(np.sum(a * a) * np.sum(b * b))
    return float(np.sum(a * b) / denom) if denom > 1e-12 else 0.0


def make_filter(first_obs: np.ndarray, cfg: ChannelConfig):
    init = initialize_position(first_obs, cfg)
    ukf = SignalObservationUKF(
        np.r_[init, np.zeros(3)],
        np.diag([8.0**2] * 3 + [1.5**2] * 3),
        acceleration_process_covariance(1.0, 0.20),
        fixed_measurement_covariance(),
        cfg,
    )
    return WhiteningAwareAdaptiveRUKF(
        ukf,
        threshold_deg=5.0,
        base_doa_scale=1.0,
        jump_threshold_deg=None,
        jump_doa_scale=1.0,
        innovation_guard_scale=1.0,
    )


def run_filter(obs: np.ndarray, quals: list[dict[str, float]], truth: np.ndarray, cfg: ChannelConfig):
    wrapper = make_filter(obs[0], cfg)
    est = np.zeros((STEPS, 3))
    est[0] = wrapper.ukf.x[:3]
    failures = 0
    for k in range(1, STEPS):
        try:
            wrapper.step(obs[k], quals[k])
            est[k] = wrapper.ukf.x[:3]
        except Exception:
            failures += 1
            est[k] = est[k - 1]
    err = np.linalg.norm(est - truth, axis=1)
    settled = err[SETTLE_START:]
    return {
        "rmse_m": float(np.sqrt(np.mean(settled**2))),
        "median_err_m": float(np.median(settled)),
        "p90_err_m": float(np.percentile(settled, 90)),
        "max_err_m": float(np.max(settled)),
        "diverged": bool(np.any(settled > 80.0)),
        "failures": int(failures),
        "mean_doa_R_scale": float(np.mean([h["R_doa_scale"] for h in wrapper.history])) if wrapper.history else 1.0,
    }


def _bootstrap_ci(values: np.ndarray, seed: int = 650, n: int = 4000):
    rng = np.random.default_rng(seed)
    values = np.asarray(values, float)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def summarize(rows: list[dict]):
    policy_names = list(POLICIES)
    summary = {"policies": {}, "by_condition": {}, "whitening": {}, "safe_candidates": []}
    fixed_rmse = np.array([r["policy_results"]["fixed"]["rmse_m"] for r in rows])
    fixed_lag = np.array([r["lag1_by_policy"]["fixed"] for r in rows])

    for name in policy_names:
        rmse = np.array([r["policy_results"][name]["rmse_m"] for r in rows])
        median_err = np.array([r["policy_results"][name]["median_err_m"] for r in rows])
        p90 = np.array([r["policy_results"][name]["p90_err_m"] for r in rows])
        gain = fixed_rmse - rmse
        lo, hi = _bootstrap_ci(gain)
        try:
            p = float(wilcoxon(gain, alternative="greater").pvalue) if np.any(gain != 0) else 1.0
        except ValueError:
            p = 1.0
        lags = np.array([r["lag1_by_policy"][name] for r in rows])
        lag_reduction = fixed_lag - lags
        summary["policies"][name] = {
            "hop_fraction": float(np.mean(SCHEDULES[name] != FIXED_CARRIER_HZ)),
            "mean_rmse_m": float(np.mean(rmse)),
            "median_rmse_m": float(np.median(rmse)),
            "mean_settled_median_err_m": float(np.mean(median_err)),
            "mean_p90_err_m": float(np.mean(p90)),
            "mean_gain_vs_fixed_m": float(np.mean(gain)),
            "median_gain_vs_fixed_m": float(np.median(gain)),
            "gain_ci95": [lo, hi],
            "wilcoxon_gain_gt0_p": p,
            "improved_fraction_vs_fixed": float(np.mean(gain > 0)),
            "div_rate": float(np.mean([r["policy_results"][name]["diverged"] for r in rows])),
            "mean_lag1_el": float(np.mean(lags)),
            "median_lag1_el": float(np.median(lags)),
            "mean_lag_reduction_vs_fixed": float(np.mean(lag_reduction)),
            "lag_reduced_fraction_vs_fixed": float(np.mean(lag_reduction > 0)),
        }

    for cond, *_ in CONDITIONS:
        sub = [r for r in rows if r["condition"] == cond]
        fixed_sub = np.array([r["policy_results"]["fixed"]["rmse_m"] for r in sub])
        summary["by_condition"][cond] = {}
        for name in policy_names:
            rmse = np.array([r["policy_results"][name]["rmse_m"] for r in sub])
            gain = fixed_sub - rmse
            summary["by_condition"][cond][name] = {
                "mean_rmse_m": float(np.mean(rmse)),
                "mean_gain_vs_fixed_m": float(np.mean(gain)),
                "median_gain_vs_fixed_m": float(np.median(gain)),
                "improved_fraction_vs_fixed": float(np.mean(gain > 0)),
            }

    for name in policy_names:
        if name == "fixed":
            continue
        gain = summary["policies"][name]["mean_gain_vs_fixed_m"]
        tail = summary["policies"][name]["mean_p90_err_m"] - summary["policies"]["fixed"]["mean_p90_err_m"]
        lag = summary["policies"][name]["mean_lag_reduction_vs_fixed"]
        if gain >= -0.25 and tail <= 0.75 and lag > 0:
            summary["safe_candidates"].append(name)

    lag_reductions = np.array([
        summary["policies"][name]["mean_lag_reduction_vs_fixed"] for name in policy_names
    ])
    mean_gains = np.array([
        summary["policies"][name]["mean_gain_vs_fixed_m"] for name in policy_names
    ])
    rho, rho_p = spearmanr(lag_reductions, mean_gains)
    summary["whitening"] = {
        "policy_lag_reduction_vs_gain_spearman": float(rho) if np.isfinite(rho) else None,
        "policy_lag_reduction_vs_gain_p": float(rho_p) if np.isfinite(rho_p) else None,
        "best_policy_by_mean_rmse": min(policy_names, key=lambda n: summary["policies"][n]["mean_rmse_m"]),
        "best_nonfixed_policy_by_mean_rmse": min(
            [n for n in policy_names if n != "fixed"],
            key=lambda n: summary["policies"][n]["mean_rmse_m"],
        ),
    }
    return summary


def run():
    cfg = ChannelConfig()
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    partial_path = out / "anchor_hop_schedule_partial.json"
    rows = json.loads(partial_path.read_text(encoding="utf-8"))["runs"] if partial_path.exists() else []
    done = {(r["condition"], int(r["index"])) for r in rows}

    for ci, (name, speed, mode, vz) in enumerate(CONDITIONS):
        for i in range(GEOMS):
            if (name, i) in done:
                continue
            pos, env, az, sign = geometry(ci, i)
            truth = truth_trajectory(pos, az, sign, speed, mode, vz)
            policy_results = {}
            lag1_by_policy = {}
            measurement_cache = {}
            for policy_name, carriers in SCHEDULES.items():
                obs, quals, el_err = collect_cached(truth, env, ci, i, carriers, measurement_cache)
                policy_results[policy_name] = run_filter(obs, quals, truth, cfg)
                lag1_by_policy[policy_name] = lag1_autocorr(el_err)
            rows.append(
                {
                    "condition": name,
                    "index": i,
                    "policy_results": policy_results,
                    "lag1_by_policy": lag1_by_policy,
                }
            )
            partial_path.write_text(json.dumps({"runs": rows}, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"completed {len(rows)}/{len(CONDITIONS) * GEOMS}: {name} #{i}", flush=True)

    payload = {
        "config": {
            "distance_m": DISTANCE,
            "geoms_per_condition": GEOMS,
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "conditions": [c[0] for c in CONDITIONS],
            "policies": POLICIES,
            "schedules_hz": {name: carriers.tolist() for name, carriers in SCHEDULES.items()},
            "note": "64번 후속. fixed carrier를 anchor로 두고 sparse hop probe schedule을 비교.",
        },
        "summary": summarize(rows),
        "runs": rows,
    }
    (out / "anchor_hop_schedule.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": payload["summary"]}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
