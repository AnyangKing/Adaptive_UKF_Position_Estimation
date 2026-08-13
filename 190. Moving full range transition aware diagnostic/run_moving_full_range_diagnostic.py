"""Moving-target 0--1000 m diagnostic for transition-aware Adaptive-R."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
F63 = next(ROOT.glob("63. *"))
sys.path.insert(0, str(F63))


from channel import synthesize_received  # noqa: E402
from conditional_adaptive import ConditionalAdaptiveRUKF  # noqa: E402
from config import ChannelConfig  # noqa: E402
from measurement import fixed_measurement_covariance, initialize_position  # noqa: E402
from peak_measurement import extract_measurement  # noqa: E402
from ukf import SignalObservationUKF, acceleration_process_covariance  # noqa: E402


DISTANCES = tuple(float(d) for d in range(0, 1001, 100))
GEOMS = 3
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0
FIXED_CARRIER_HZ = 32_000.0
HOP_CARRIERS_HZ = np.linspace(30_000.0, 34_000.0, STEPS)
GEOM_ROOT = 1_900_000
PING_ROOT = 1_903_000
RANGE_JUMP_THRESHOLD_M = 0.5
MAX_TOA_SCALE = 100.0


CONDITIONS = (
    ("radial_0.05", 0.05, "radial", 0.00),
    ("radial_1.0", 1.00, "radial", 0.00),
    ("tangential_1.0", 1.00, "tangential", 0.00),
    ("tang_1.0_vz", 1.00, "tangential", 0.08),
)


class CarrierTransitionSoftRUKF:
    """Frozen folder-181 rule: Conditional Adaptive-R plus soft TOA inflation."""

    def __init__(
        self,
        ukf,
        disagreement_threshold_deg: float,
        range_jump_threshold_m: float = RANGE_JUMP_THRESHOLD_M,
        max_toa_scale: float = MAX_TOA_SCALE,
    ):
        self.ukf = ukf
        self.base_R = ukf.R.copy()
        self.threshold = float(disagreement_threshold_deg)
        self.range_jump_threshold_m = float(range_jump_threshold_m)
        self.max_toa_scale = float(max_toa_scale)
        self.previous_range_m: float | None = None
        self.previous_carrier_hz: float | None = None
        self.history: list[dict[str, Any]] = []

    def prime(self, observation: np.ndarray, carrier_hz: float) -> None:
        self.previous_range_m = float(observation[0])
        self.previous_carrier_hz = float(carrier_hz)

    @staticmethod
    def _nis(residual: np.ndarray, covariance: np.ndarray, indices: slice) -> float:
        value = residual[indices]
        block = covariance[indices, indices]
        return float(value @ np.linalg.solve(block, value))

    def step(self, observation: np.ndarray, quality: dict, carrier_hz: float):
        if self.previous_range_m is None or self.previous_carrier_hz is None:
            raise RuntimeError("prime() must be called before step()")
        observation = np.asarray(observation)
        carrier_hz = float(carrier_hz)
        range_jump_m = abs(float(observation[0]) - self.previous_range_m)
        carrier_changed = abs(carrier_hz - self.previous_carrier_hz) > 1.0e-6
        transition_risk = bool(carrier_changed and range_jump_m > self.range_jump_threshold_m)
        transition_scale = (
            min(self.max_toa_scale, 1.0 + (range_jump_m / max(self.range_jump_threshold_m, 1.0e-9)) ** 2)
            if transition_risk else 1.0
        )

        self.ukf.predict()
        R = self.base_R.copy()
        disagreement = float(quality["doa_disagreement_deg"])
        disagreement_scale = min(100.0, 1.0 + (disagreement / 2.0) ** 2)
        routed_to_tdoa = disagreement > self.threshold
        if routed_to_tdoa:
            R[1:8, 1:8] *= disagreement_scale
        else:
            R[8:10, 8:10] *= disagreement_scale

        if transition_risk:
            R[0, 0] *= transition_scale

        _, _, predicted, _, S = self.ukf.measurement_statistics(R)
        residual = self.ukf._z_residual(observation.copy(), predicted)
        block_nis = {
            "toa": self._nis(residual, S, slice(0, 1)),
            "tdoa": self._nis(residual, S, slice(1, 8)),
            "doa": self._nis(residual, S, slice(8, 10)),
        }
        for name, indices, limit in (
            ("toa", slice(0, 1), 6.63),
            ("tdoa", slice(1, 8), 18.48),
            ("doa", slice(8, 10), 9.21),
        ):
            R[indices, indices] *= min(100.0, max(1.0, block_nis[name] / limit))

        total_nis = float(residual @ np.linalg.solve(S, residual))
        self.ukf.update(observation, R)
        self.history.append({
            "carrier_hz": carrier_hz,
            "carrier_changed": carrier_changed,
            "range_jump_m": range_jump_m,
            "transition_risk": transition_risk,
            "transition_scale": float(transition_scale),
            "disagreement_deg": disagreement,
            "routed_to_tdoa": routed_to_tdoa,
            "block_nis": block_nis,
            "total_nis": total_nis,
        })
        self.previous_range_m = float(observation[0])
        self.previous_carrier_hz = carrier_hz
        return self.ukf.x.copy()


def geometry(distance: float, cond_idx: int, index: int):
    rng = np.random.default_rng(GEOM_ROOT + int(distance) * 100 + cond_idx * 1000 + index)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    pos = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
    env = {
        "snr_db": float(rng.choice([10.0, 20.0, 30.0])),
        "surface_reflection": float(-rng.uniform(0.72, 0.97)),
        "bottom_reflection": float(rng.uniform(0.32, 0.78)),
        "radial_velocity_m_s": 0.0,
    }
    sign = 1.0 if rng.uniform() < 0.5 else -1.0
    return pos, env, az, sign


def truth_trajectory(pos: np.ndarray, az: float, sign: float, speed: float, mode: str, vz: float) -> np.ndarray:
    radial = np.array([np.cos(az), np.sin(az), 0.0])
    tangential = np.array([-np.sin(az), np.cos(az), 0.0])
    v = (sign * speed * radial) if mode == "radial" else (speed * tangential)
    v = v + np.array([0.0, 0.0, sign * vz])
    return pos + np.arange(STEPS)[:, None] * v


def collect(truth: np.ndarray, env: dict[str, float], distance: float, cond_idx: int, index: int, carriers: np.ndarray):
    observations: list[np.ndarray] = []
    qualities: list[dict] = []
    for k, pos in enumerate(truth):
        cfg = replace(
            ChannelConfig(),
            seed=PING_ROOT + int(distance) * 5000 + cond_idx * 4000 + index * 60 + k,
            carrier_hz=float(carriers[k]),
            **env,
        )
        _, received, _ = synthesize_received(pos, cfg)
        observation, quality = extract_measurement(received, cfg)
        observations.append(observation)
        qualities.append(quality)
    return np.asarray(observations), qualities


def make_filter(initial_observation: np.ndarray):
    cfg = ChannelConfig()
    initial = initialize_position(initial_observation, cfg)
    ukf = SignalObservationUKF(
        np.r_[initial, np.zeros(3)],
        np.diag([8.0**2] * 3 + [1.5**2] * 3),
        acceleration_process_covariance(1.0, 0.20),
        fixed_measurement_covariance(),
        cfg,
    )
    return ukf, initial


def run_filter(observations, qualities, truth, carriers, policy: str) -> dict[str, Any]:
    ukf, initial = make_filter(observations[0])
    if policy in ("fixed_baseline", "hop_baseline"):
        wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    elif policy == "hop_transition_softR":
        wrapper = CarrierTransitionSoftRUKF(ukf, ROUTING_THRESHOLD_DEG)
        wrapper.prime(observations[0], carriers[0])
    else:
        raise ValueError(policy)

    estimates = np.zeros((STEPS, 3))
    estimates[0] = initial
    exceptions = 0
    for k in range(1, STEPS):
        try:
            if policy == "hop_transition_softR":
                wrapper.step(observations[k], qualities[k], carriers[k])
            else:
                wrapper.step(observations[k], qualities[k])
            estimates[k] = ukf.x[:3]
        except Exception:
            exceptions += 1
            estimates[k] = estimates[k - 1]

    errors = np.linalg.norm(estimates - truth, axis=1)
    history = getattr(wrapper, "history", [])
    transition_events = [h for h in history if h.get("transition_risk")]
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[SETTLE_START:] ** 2))),
        "median_settled_error_m": float(np.median(errors[SETTLE_START:])),
        "p90_settled_error_m": float(np.percentile(errors[SETTLE_START:], 90.0)),
        "maximum_position_error_m": float(np.max(errors)),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": int(exceptions),
        "transition_risk_count": len(transition_events),
        "mean_transition_scale": float(np.mean([h["transition_scale"] for h in transition_events])) if transition_events else 1.0,
    }


def run_case(distance: float, cond_idx: int, cond: tuple[str, float, str, float], index: int) -> list[dict[str, Any]]:
    name, speed, mode, vz = cond
    pos, env, az, sign = geometry(distance, cond_idx, index)
    truth = truth_trajectory(pos, az, sign, speed, mode, vz)
    fixed_carriers = np.full(STEPS, FIXED_CARRIER_HZ)
    obs_fixed, q_fixed = collect(truth, env, distance, cond_idx, index, fixed_carriers)
    obs_hop, q_hop = collect(truth, env, distance, cond_idx, index, HOP_CARRIERS_HZ)
    return [
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "fixed_baseline",
            **run_filter(obs_fixed, q_fixed, truth, fixed_carriers, "fixed_baseline"),
        },
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "hop_baseline",
            **run_filter(obs_hop, q_hop, truth, HOP_CARRIERS_HZ, "hop_baseline"),
        },
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "hop_transition_softR",
            **run_filter(obs_hop, q_hop, truth, HOP_CARRIERS_HZ, "hop_transition_softR"),
        },
    ]


def bootstrap_ci(values: np.ndarray, seed: int = 190, n: int = 3000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def compare(keys: list[tuple[float, str, int]], ref: dict, test: dict) -> dict[str, Any]:
    gains = np.array([ref[k]["settled_rmse_m"] - test[k]["settled_rmse_m"] for k in keys])
    try:
        p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
    except ValueError:
        p = 1.0
    return {
        "mean_gain_m": float(np.mean(gains)),
        "median_gain_m": float(np.median(gains)),
        "gain_ci95": bootstrap_ci(gains),
        "wilcoxon_gain_gt0_p": p,
        "improved_fraction": float(np.mean(gains > 0)),
        "tail_worsened_fraction": float(np.mean(gains < -1.0)),
        "n": len(keys),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    policies = ("fixed_baseline", "hop_baseline", "hop_transition_softR")
    summary: dict[str, Any] = {"overall": {}, "by_distance": {}, "by_condition": {}, "comparisons": {}}
    by_policy = {p: [r for r in rows if r["policy"] == p] for p in policies}
    for policy, subset in by_policy.items():
        summary["overall"][policy] = {
            "mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in subset])),
            "median_rmse_m": float(np.median([r["settled_rmse_m"] for r in subset])),
            "mean_p90_error_m": float(np.mean([r["p90_settled_error_m"] for r in subset])),
            "divergence_rate": float(np.mean([r["diverged"] for r in subset])),
            "total_transition_risks": int(sum(r["transition_risk_count"] for r in subset)),
            "n": len(subset),
        }

    fixed = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "fixed_baseline"}
    hop = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_baseline"}
    soft = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_transition_softR"}
    keys = sorted(soft)
    summary["comparisons"]["softR_vs_hop"] = compare(keys, hop, soft)
    summary["comparisons"]["softR_vs_fixed"] = compare(keys, fixed, soft)
    summary["comparisons"]["hop_vs_fixed"] = compare(keys, fixed, hop)

    for distance in DISTANCES:
        dkeys = [k for k in keys if k[0] == distance]
        drows = [r for r in rows if r["distance_m"] == distance]
        summary["by_distance"][str(distance)] = {
            "fixed_mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in drows if r["policy"] == "fixed_baseline"])),
            "hop_mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in drows if r["policy"] == "hop_baseline"])),
            "softR_mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in drows if r["policy"] == "hop_transition_softR"])),
            "hop_gain_vs_fixed_m": compare(dkeys, fixed, hop)["mean_gain_m"],
            "softR_gain_vs_hop_m": compare(dkeys, hop, soft)["mean_gain_m"],
            "softR_gain_vs_fixed_m": compare(dkeys, fixed, soft)["mean_gain_m"],
            "softR_tail_worsened_vs_hop": compare(dkeys, hop, soft)["tail_worsened_fraction"],
            "n": len(dkeys),
        }

    for condition, *_ in CONDITIONS:
        ckeys = [k for k in keys if k[1] == condition]
        summary["by_condition"][condition] = {
            "softR_vs_hop": compare(ckeys, hop, soft),
            "softR_vs_fixed": compare(ckeys, fixed, soft),
            "hop_vs_fixed": compare(ckeys, fixed, hop),
        }
    return summary


def markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Moving full-range diagnostic result summary",
        "",
        "## Overall paired comparisons",
        "",
        "| comparison | mean gain | p | improved frac | tail worsened | n |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, comp in summary["comparisons"].items():
        lines.append(
            f"| {name} | {comp['mean_gain_m']:.3f} | {comp['wilcoxon_gain_gt0_p']:.4g} | "
            f"{comp['improved_fraction']:.3f} | {comp['tail_worsened_fraction']:.3f} | {comp['n']} |"
        )
    lines.extend([
        "",
        "## Distance breakdown",
        "",
        "| distance | fixed | hop | softR | hop gain vs fixed | softR gain vs hop | softR gain vs fixed | softR tail worsened vs hop |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for distance in DISTANCES:
        s = summary["by_distance"][str(distance)]
        lines.append(
            f"| {int(distance)} | {s['fixed_mean_rmse_m']:.3f} | {s['hop_mean_rmse_m']:.3f} | "
            f"{s['softR_mean_rmse_m']:.3f} | {s['hop_gain_vs_fixed_m']:.3f} | "
            f"{s['softR_gain_vs_hop_m']:.3f} | {s['softR_gain_vs_fixed_m']:.3f} | "
            f"{s['softR_tail_worsened_vs_hop']:.3f} |"
        )
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "This is a low-n distance diagnostic. It should guide the next independent validation grid, not replace it.",
    ])
    return "\n".join(lines) + "\n"


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [
        (distance, ci, cond, i)
        for distance in DISTANCES
        for ci, cond in enumerate(CONDITIONS)
        for i in range(GEOMS)
    ]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for future in as_completed(futures):
            distance, _, cond, i = futures[future]
            rows.extend(future.result())
            print(f"completed moving full-range {int(distance)} m {cond[0]} #{i}", flush=True)

    rows.sort(key=lambda r: (r["distance_m"], r["condition"], r["index"], r["policy"]))
    payload = {
        "config": {
            "stage": "moving_full_range_diagnostic",
            "distances_m": list(DISTANCES),
            "geoms_per_distance_condition": GEOMS,
            "conditions": [
                {"name": c[0], "speed_m_s": c[1], "mode": c[2], "vertical_speed_m_s": c[3]}
                for c in CONDITIONS
            ],
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "fixed_carrier_khz": FIXED_CARRIER_HZ / 1000.0,
            "hop_carriers_khz": [float(c / 1000.0) for c in HOP_CARRIERS_HZ],
            "range_jump_threshold_m": RANGE_JUMP_THRESHOLD_M,
            "max_toa_scale": MAX_TOA_SCALE,
            "truth_usage": "truth is used for signal synthesis and final error computation only; transition-aware decisions use observed TOA range jump, carrier transition, disagreement, and NIS.",
            "claim_boundary": "distance diagnostic only; not final moving-target validation",
        },
        "summary": summarize(rows),
        "trials": rows,
    }
    (HERE / "moving_full_range_diagnostic.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (HERE / "result_summary.md").write_text(markdown(payload), encoding="utf-8")
    print(markdown(payload))
    return payload


if __name__ == "__main__":
    run()

