"""Moving development pilot for carrier-transition-aware Adaptive-R.

This is not an independent validation and does not create a manuscript
performance claim.  It tests whether a soft observed-TOA-jump covariance rule is
worth promoting to a larger validation.
"""

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


DISTANCE = 600.0
GEOMS = 4
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0
FIXED_CARRIER_HZ = 32_000.0
HOP_CARRIERS_HZ = np.linspace(30_000.0, 34_000.0, STEPS)
GEOM_ROOT = 1_800_000
PING_ROOT = 1_803_000
RANGE_JUMP_THRESHOLD_M = 0.5
MAX_TOA_SCALE = 100.0


CONDITIONS = (
    ("radial_0.05", 0.05, "radial", 0.00),
    ("radial_1.0", 1.00, "radial", 0.00),
    ("tangential_1.0", 1.00, "tangential", 0.00),
    ("tang_1.0_vz", 1.00, "tangential", 0.08),
)


class CarrierTransitionSoftRUKF:
    """Conditional Adaptive-R plus soft TOA covariance inflation at transitions."""

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
        transition_scale = min(
            self.max_toa_scale,
            1.0 + (range_jump_m / max(self.range_jump_threshold_m, 1.0e-9)) ** 2,
        ) if transition_risk else 1.0

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


def geometry(cond_idx: int, index: int):
    rng = np.random.default_rng(GEOM_ROOT + cond_idx * 1000 + index)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    pos = np.array([DISTANCE * np.cos(az), DISTANCE * np.sin(az), -depth])
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


def collect(truth: np.ndarray, env: dict[str, float], cond_idx: int, index: int, carriers: np.ndarray):
    observations: list[np.ndarray] = []
    qualities: list[dict] = []
    for k, pos in enumerate(truth):
        cfg = replace(
            ChannelConfig(),
            seed=PING_ROOT + cond_idx * 4000 + index * 60 + k,
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


def run_case(cond_idx: int, cond: tuple[str, float, str, float], index: int) -> list[dict[str, Any]]:
    name, speed, mode, vz = cond
    pos, env, az, sign = geometry(cond_idx, index)
    truth = truth_trajectory(pos, az, sign, speed, mode, vz)
    obs_fixed, q_fixed = collect(truth, env, cond_idx, index, np.full(STEPS, FIXED_CARRIER_HZ))
    obs_hop, q_hop = collect(truth, env, cond_idx, index, HOP_CARRIERS_HZ)
    return [
        {
            "condition": name,
            "index": index,
            "policy": "fixed_baseline",
            **run_filter(obs_fixed, q_fixed, truth, np.full(STEPS, FIXED_CARRIER_HZ), "fixed_baseline"),
        },
        {
            "condition": name,
            "index": index,
            "policy": "hop_baseline",
            **run_filter(obs_hop, q_hop, truth, HOP_CARRIERS_HZ, "hop_baseline"),
        },
        {
            "condition": name,
            "index": index,
            "policy": "hop_transition_softR",
            **run_filter(obs_hop, q_hop, truth, HOP_CARRIERS_HZ, "hop_transition_softR"),
        },
    ]


def bootstrap_ci(values: np.ndarray, seed: int = 180, n: int = 5000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"policies": {}, "comparisons": {}, "by_condition": {}}
    policies = ("fixed_baseline", "hop_baseline", "hop_transition_softR")
    for policy in policies:
        subset = [r for r in rows if r["policy"] == policy]
        summary["policies"][policy] = {
            "mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in subset])),
            "median_rmse_m": float(np.median([r["settled_rmse_m"] for r in subset])),
            "mean_p90_error_m": float(np.mean([r["p90_settled_error_m"] for r in subset])),
            "divergence_rate": float(np.mean([r["diverged"] for r in subset])),
            "filter_exceptions": int(sum(r["filter_exceptions"] for r in subset)),
            "total_transition_risks": int(sum(r["transition_risk_count"] for r in subset)),
            "n": len(subset),
        }

    base_by_key = {(r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_baseline"}
    soft_by_key = {(r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_transition_softR"}
    fixed_by_key = {(r["condition"], r["index"]): r for r in rows if r["policy"] == "fixed_baseline"}

    for label, ref in (("softR_vs_hop", base_by_key), ("softR_vs_fixed", fixed_by_key)):
        gains = np.array([
            ref[k]["settled_rmse_m"] - soft_by_key[k]["settled_rmse_m"]
            for k in sorted(soft_by_key)
        ])
        try:
            p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
        except ValueError:
            p = 1.0
        summary["comparisons"][label] = {
            "mean_gain_m": float(np.mean(gains)),
            "median_gain_m": float(np.median(gains)),
            "gain_ci95": bootstrap_ci(gains),
            "wilcoxon_gain_gt0_p": p,
            "improved_fraction": float(np.mean(gains > 0)),
            "tail_worsened_fraction": float(np.mean(gains < -1.0)),
        }

    for condition, *_ in CONDITIONS:
        summary["by_condition"][condition] = {}
        for policy in policies:
            subset = [r for r in rows if r["condition"] == condition and r["policy"] == policy]
            summary["by_condition"][condition][policy] = {
                "mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in subset])),
                "median_rmse_m": float(np.median([r["settled_rmse_m"] for r in subset])),
                "divergence_rate": float(np.mean([r["diverged"] for r in subset])),
            }
    return summary


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [(ci, cond, i) for ci, cond in enumerate(CONDITIONS) for i in range(GEOMS)]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for future in as_completed(futures):
            ci, cond, i = futures[future]
            rows.extend(future.result())
            print(f"completed {cond[0]} #{i}", flush=True)

    rows.sort(key=lambda r: (r["condition"], r["index"], r["policy"]))
    summary = summarize(rows)
    cmp = summary["comparisons"]["softR_vs_hop"]
    criteria = {
        "mean_gain_vs_hop_positive": cmp["mean_gain_m"] > 0.0,
        "tail_worsening_le_10pct": cmp["tail_worsened_fraction"] <= 0.10,
        "wilcoxon_p_lt_0_20_for_development": cmp["wilcoxon_gain_gt0_p"] < 0.20,
        "no_extra_divergence_vs_hop": (
            summary["policies"]["hop_transition_softR"]["divergence_rate"]
            <= summary["policies"]["hop_baseline"]["divergence_rate"]
        ),
    }
    payload = {
        "config": {
            "stage": "development_pilot",
            "distance_m": DISTANCE,
            "geoms_per_condition": GEOMS,
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
            "manuscript_claim_allowed": False,
        },
        "summary": summary,
        "criteria": criteria,
        "decision": "advance_to_independent_validation_candidate" if all(criteria.values()) else "do_not_advance_current_softR",
        "trials": rows,
    }
    out = HERE / "transition_aware_moving_pilot.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"decision": payload["decision"], "criteria": criteria, "comparisons": summary["comparisons"]}, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run()
