"""64. Whitening-aware adaptive-R / schedule gating 후보 검증.

사전 질문:
  H1) 63번에서 확인한 hop의 lag-1 백색화는 유지되는가?
  H2) hop always-on의 이동 표적 outlier 악화를 DOA R 안전화로 줄일 수 있는가?
  H3) 안전화 후보 중 fixed baseline보다 pooled RMSE가 좋아지는 정책이 있는가?

본 실험은 63번과 같은 600 m 이동 표적 4조건을 사용하지만, seed 계열은 새로
분리한다. 관측 시퀀스는 fixed/hop을 한 번만 생성하고 여러 필터 정책을 같은
관측에 적용해 paired 비교한다.
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
GEOMS = 12
STEPS = 20
SETTLE_START = 10
HOP_CARRIERS_HZ = np.linspace(30000.0, 34000.0, STEPS)
FIXED_CARRIER_HZ = 32000.0
GEOM_ROOT = 720000
PING_ROOT = 1600000

CONDITIONS = (
    ("radial_0.05", 0.05, "radial", 0.00),
    ("radial_1.0", 1.00, "radial", 0.00),
    ("tangential_1.0", 1.00, "tangential", 0.00),
    ("tang_1.0_vz", 1.00, "tangential", 0.08),
)

POLICIES = {
    "fixed": {"carrier": "fixed", "base": 1.0, "jump": None, "jump_scale": 1.0, "guard": 1.0},
    "hop_always": {"carrier": "hop", "base": 1.0, "jump": None, "jump_scale": 1.0, "guard": 1.0},
    "hop_R4": {"carrier": "hop", "base": 4.0, "jump": None, "jump_scale": 1.0, "guard": 1.0},
    "hop_R9": {"carrier": "hop", "base": 9.0, "jump": None, "jump_scale": 1.0, "guard": 1.0},
    "hop_jump1_x16": {"carrier": "hop", "base": 1.0, "jump": 1.0, "jump_scale": 16.0, "guard": 1.0},
    "hop_jump2_x16": {"carrier": "hop", "base": 1.0, "jump": 2.0, "jump_scale": 16.0, "guard": 1.0},
    "hop_R4_jump1_x8": {"carrier": "hop", "base": 4.0, "jump": 1.0, "jump_scale": 8.0, "guard": 1.0},
    "hop_guard4": {"carrier": "hop", "base": 1.0, "jump": None, "jump_scale": 1.0, "guard": 4.0},
}


def geometry(cond_idx, index):
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


def truth_trajectory(pos, az, sign, speed, mode, vz):
    radial = np.array([np.cos(az), np.sin(az), 0.0])
    tangential = np.array([-np.sin(az), np.cos(az), 0.0])
    v = sign * speed * radial if mode == "radial" else speed * tangential
    v = v + np.array([0.0, 0.0, sign * vz])
    return pos + np.arange(STEPS)[:, None] * v


def collect(truth, env, cond_idx, index, carriers):
    obs, quals, el_err = [], [], []
    for k, pos in enumerate(truth):
        cfg = replace(
            ChannelConfig(),
            seed=PING_ROOT + cond_idx * 4000 + index * 60 + k,
            carrier_hz=float(carriers[k]),
            **env,
        )
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        truth_z = ideal_measurement(pos, cfg)
        el_err.append(float(z[9] - truth_z[9]))
        obs.append(z)
        quals.append(q)
    return np.asarray(obs), quals, np.asarray(el_err)


def lag1_autocorr(x):
    x = np.asarray(x, float)
    a, b = x[:-1] - x[:-1].mean(), x[1:] - x[1:].mean()
    denom = np.sqrt(np.sum(a * a) * np.sum(b * b))
    return float(np.sum(a * b) / denom) if denom > 1e-12 else 0.0


def make_filter(first_obs, cfg, policy):
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
        base_doa_scale=policy["base"],
        jump_threshold_deg=policy["jump"],
        jump_doa_scale=policy["jump_scale"],
        innovation_guard_scale=policy["guard"],
    )


def run_filter(obs, quals, truth, cfg, policy):
    wrapper = make_filter(obs[0], cfg, policy)
    est = np.zeros((STEPS, 3))
    est[0] = wrapper.ukf.x[:3]
    for k in range(1, STEPS):
        try:
            wrapper.step(obs[k], quals[k])
            est[k] = wrapper.ukf.x[:3]
        except Exception:
            est[k] = est[k - 1]
    err = np.linalg.norm(est - truth, axis=1)
    jump_fraction = float(np.mean([h["jump_gate"] for h in wrapper.history])) if wrapper.history else 0.0
    mean_doa_scale = float(np.mean([h["R_doa_scale"] for h in wrapper.history])) if wrapper.history else 1.0
    return {
        "rmse_m": float(np.sqrt(np.mean(err[SETTLE_START:] ** 2))),
        "diverged": bool(np.any(err[SETTLE_START:] > 80.0)),
        "jump_fraction": jump_fraction,
        "mean_doa_R_scale": mean_doa_scale,
    }


def _bootstrap_ci(values, seed=640, n=5000):
    rng = np.random.default_rng(seed)
    values = np.asarray(values, float)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def summarize(rows):
    policy_names = list(POLICIES)
    summary = {"policies": {}, "by_condition": {}, "whitening": {}}
    fixed = np.array([r["policy_results"]["fixed"]["rmse_m"] for r in rows])
    hop = np.array([r["policy_results"]["hop_always"]["rmse_m"] for r in rows])

    for name in policy_names:
        rmse = np.array([r["policy_results"][name]["rmse_m"] for r in rows])
        gain = fixed - rmse
        lo, hi = _bootstrap_ci(gain)
        try:
            p = float(wilcoxon(gain, alternative="greater").pvalue) if np.any(gain != 0) else 1.0
        except ValueError:
            p = 1.0
        summary["policies"][name] = {
            "mean_rmse_m": float(np.mean(rmse)),
            "median_rmse_m": float(np.median(rmse)),
            "mean_gain_vs_fixed_m": float(np.mean(gain)),
            "median_gain_vs_fixed_m": float(np.median(gain)),
            "gain_ci95": [lo, hi],
            "wilcoxon_gain_gt0_p": p,
            "improved_fraction_vs_fixed": float(np.mean(gain > 0)),
            "div_rate": float(np.mean([r["policy_results"][name]["diverged"] for r in rows])),
            "mean_doa_R_scale": float(np.mean([r["policy_results"][name]["mean_doa_R_scale"] for r in rows])),
        }

    for cond, *_ in CONDITIONS:
        sub = [r for r in rows if r["condition"] == cond]
        summary["by_condition"][cond] = {}
        fixed_sub = np.array([r["policy_results"]["fixed"]["rmse_m"] for r in sub])
        for name in policy_names:
            rmse = np.array([r["policy_results"][name]["rmse_m"] for r in sub])
            gain = fixed_sub - rmse
            summary["by_condition"][cond][name] = {
                "mean_rmse_m": float(np.mean(rmse)),
                "mean_gain_vs_fixed_m": float(np.mean(gain)),
                "median_gain_vs_fixed_m": float(np.median(gain)),
                "improved_fraction_vs_fixed": float(np.mean(gain > 0)),
            }

    lag_fixed = np.array([r["lag1_fixed"] for r in rows])
    lag_hop = np.array([r["lag1_hop"] for r in rows])
    lag_reduction = lag_fixed - lag_hop
    best_name = min(policy_names, key=lambda n: summary["policies"][n]["mean_rmse_m"])
    hop_gain = fixed - np.array([r["policy_results"]["hop_always"]["rmse_m"] for r in rows])
    rho, rho_p = spearmanr(lag_reduction, hop_gain)
    summary["whitening"] = {
        "mean_lag1_fixed": float(np.mean(lag_fixed)),
        "mean_lag1_hop": float(np.mean(lag_hop)),
        "median_lag1_fixed": float(np.median(lag_fixed)),
        "median_lag1_hop": float(np.median(lag_hop)),
        "fixed_gt_hop_p": float(wilcoxon(lag_fixed - lag_hop, alternative="greater").pvalue),
        "reduced_fraction": float(np.mean(lag_fixed > lag_hop)),
        "lag_reduction_vs_hop_gain_spearman": float(rho),
        "lag_reduction_vs_hop_gain_p": float(rho_p),
        "best_policy_by_mean_rmse": best_name,
    }
    summary["hop_always_vs_fixed"] = {
        "mean_delta_m": float(np.mean(fixed - hop)),
        "median_delta_m": float(np.median(fixed - hop)),
    }
    return summary


def run():
    cfg = ChannelConfig()
    fixed_carriers = np.full(STEPS, FIXED_CARRIER_HZ)
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    partial_path = out / "whitening_guard_partial.json"
    rows = json.loads(partial_path.read_text(encoding="utf-8"))["runs"] if partial_path.exists() else []
    done = {(r["condition"], int(r["index"])) for r in rows}

    for ci, (name, speed, mode, vz) in enumerate(CONDITIONS):
        for i in range(GEOMS):
            if (name, i) in done:
                continue
            pos, env, az, sign = geometry(ci, i)
            truth = truth_trajectory(pos, az, sign, speed, mode, vz)
            obs_fixed, q_fixed, el_fixed = collect(truth, env, ci, i, fixed_carriers)
            obs_hop, q_hop, el_hop = collect(truth, env, ci, i, HOP_CARRIERS_HZ)
            policy_results = {}
            for policy_name, policy in POLICIES.items():
                obs, quals = (obs_fixed, q_fixed) if policy["carrier"] == "fixed" else (obs_hop, q_hop)
                policy_results[policy_name] = run_filter(obs, quals, truth, cfg, policy)
            rows.append(
                {
                    "condition": name,
                    "index": i,
                    "lag1_fixed": lag1_autocorr(el_fixed),
                    "lag1_hop": lag1_autocorr(el_hop),
                    "policy_results": policy_results,
                }
            )
            partial_path.write_text(json.dumps({"runs": rows}, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"completed {len(rows)}/{len(CONDITIONS) * GEOMS}: {name} #{i}", flush=True)

    payload = {
        "config": {
            "distance_m": DISTANCE,
            "geoms_per_condition": GEOMS,
            "steps": STEPS,
            "conditions": [c[0] for c in CONDITIONS],
            "policies": POLICIES,
            "note": "63번 독립 후속. hop always-on의 outlier를 DOA R 안전화로 줄일 수 있는지 검증.",
        },
        "summary": summarize(rows),
        "runs": rows,
    }
    (out / "whitening_guard.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": payload["summary"]}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
