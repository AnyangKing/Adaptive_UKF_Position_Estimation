"""Extended static range validation with transition-aware Adaptive-R."""

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
F61 = next(ROOT.glob("61. *"))
sys.path.insert(0, str(F61))


from channel import synthesize_received  # noqa: E402
from conditional_adaptive import ConditionalAdaptiveRUKF  # noqa: E402
from config import ChannelConfig  # noqa: E402
from measurement import fixed_measurement_covariance, initialize_position  # noqa: E402
from peak_measurement import extract_measurement  # noqa: E402
from ukf import SignalObservationUKF, acceleration_process_covariance  # noqa: E402


DISTANCES = (800.0, 1000.0)
GEOMS = 12
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0
FIXED_CARRIER_HZ = 32_000.0
HOP_CARRIERS_HZ = np.linspace(30_000.0, 34_000.0, STEPS)
GEOM_ROOT = 1_830_000
PING_ROOT = 1_833_000
RANGE_JUMP_THRESHOLD_M = 0.5
MAX_TOA_SCALE = 100.0


class CarrierTransitionSoftRUKF:
    def __init__(self, ukf, disagreement_threshold_deg: float):
        self.ukf = ukf
        self.base_R = ukf.R.copy()
        self.threshold = float(disagreement_threshold_deg)
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
            raise RuntimeError("prime() must be called first")
        observation = np.asarray(observation)
        carrier_hz = float(carrier_hz)
        range_jump_m = abs(float(observation[0]) - self.previous_range_m)
        carrier_changed = abs(carrier_hz - self.previous_carrier_hz) > 1.0e-6
        transition_risk = bool(carrier_changed and range_jump_m > RANGE_JUMP_THRESHOLD_M)
        transition_scale = (
            min(MAX_TOA_SCALE, 1.0 + (range_jump_m / RANGE_JUMP_THRESHOLD_M) ** 2)
            if transition_risk
            else 1.0
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
            "range_jump_m": range_jump_m,
            "carrier_changed": carrier_changed,
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


def geometry(distance: float, index: int) -> tuple[np.ndarray, dict[str, float]]:
    rng = np.random.default_rng(GEOM_ROOT + int(distance) * 50 + index)
    azimuth = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    position = np.array([distance * np.cos(azimuth), distance * np.sin(azimuth), -depth])
    environment = {
        "snr_db": float(rng.choice([10.0, 20.0, 30.0])),
        "surface_reflection": float(-rng.uniform(0.72, 0.97)),
        "bottom_reflection": float(rng.uniform(0.32, 0.78)),
        "radial_velocity_m_s": 0.0,
    }
    return position, environment


def collect(position: np.ndarray, environment: dict[str, float], distance: float, index: int, carriers: np.ndarray):
    observations: list[np.ndarray] = []
    qualities: list[dict] = []
    for ping_index, carrier_hz in enumerate(carriers):
        cfg = replace(
            ChannelConfig(),
            seed=PING_ROOT + int(distance) * 1000 + index * 40 + ping_index,
            carrier_hz=float(carrier_hz),
            **environment,
        )
        _, received, _ = synthesize_received(position, cfg)
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


def run_filter(observations: np.ndarray, qualities: list[dict], position: np.ndarray, carriers: np.ndarray, policy: str):
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
    for ping_index in range(1, STEPS):
        try:
            if policy == "hop_transition_softR":
                wrapper.step(observations[ping_index], qualities[ping_index], carriers[ping_index])
            else:
                wrapper.step(observations[ping_index], qualities[ping_index])
            estimates[ping_index] = ukf.x[:3]
        except Exception:
            exceptions += 1
            estimates[ping_index] = estimates[ping_index - 1]
    errors = np.linalg.norm(estimates - position, axis=1)
    history = getattr(wrapper, "history", [])
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[SETTLE_START:] ** 2))),
        "median_settled_error_m": float(np.median(errors[SETTLE_START:])),
        "p90_settled_error_m": float(np.percentile(errors[SETTLE_START:], 90.0)),
        "maximum_position_error_m": float(np.max(errors)),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": int(exceptions),
        "transition_risk_count": int(sum(1 for h in history if h.get("transition_risk"))),
    }


def run_case(distance: float, index: int) -> dict[str, Any]:
    position, environment = geometry(distance, index)
    fixed_carriers = np.full(STEPS, FIXED_CARRIER_HZ)
    obs_fixed, q_fixed = collect(position, environment, distance, index, fixed_carriers)
    obs_hop, q_hop = collect(position, environment, distance, index, HOP_CARRIERS_HZ)
    return {
        "distance_m": distance,
        "index": index,
        "environment": environment,
        "fixed_baseline": run_filter(obs_fixed, q_fixed, position, fixed_carriers, "fixed_baseline"),
        "hop_baseline": run_filter(obs_hop, q_hop, position, HOP_CARRIERS_HZ, "hop_baseline"),
        "hop_transition_softR": run_filter(obs_hop, q_hop, position, HOP_CARRIERS_HZ, "hop_transition_softR"),
    }


def bootstrap_ci(values: np.ndarray, seed: int = 183, n: int = 5000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    policies = ("fixed_baseline", "hop_baseline", "hop_transition_softR")
    for distance in list(DISTANCES) + ["overall"]:
        subset = rows if distance == "overall" else [r for r in rows if r["distance_m"] == distance]
        summary[str(distance)] = {"policies": {}, "comparisons": {}}
        for policy in policies:
            rmse = np.array([r[policy]["settled_rmse_m"] for r in subset])
            summary[str(distance)]["policies"][policy] = {
                "mean_rmse_m": float(np.mean(rmse)),
                "median_rmse_m": float(np.median(rmse)),
                "mean_p90_error_m": float(np.mean([r[policy]["p90_settled_error_m"] for r in subset])),
                "divergence_rate": float(np.mean([r[policy]["diverged"] for r in subset])),
                "total_transition_risks": int(sum(r[policy].get("transition_risk_count", 0) for r in subset)),
                "n": len(subset),
            }
        for label, ref_policy in (
            ("softR_vs_hop", "hop_baseline"),
            ("softR_vs_fixed", "fixed_baseline"),
            ("hop_vs_fixed", "fixed_baseline"),
        ):
            target_policy = "hop_transition_softR" if label.startswith("softR") else "hop_baseline"
            gains = np.array([r[ref_policy]["settled_rmse_m"] - r[target_policy]["settled_rmse_m"] for r in subset])
            try:
                p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
            except ValueError:
                p = 1.0
            summary[str(distance)]["comparisons"][label] = {
                "mean_gain_m": float(np.mean(gains)),
                "median_gain_m": float(np.median(gains)),
                "gain_ci95": bootstrap_ci(gains),
                "wilcoxon_gain_gt0_p": p,
                "improved_fraction": float(np.mean(gains > 0.0)),
                "tail_worsened_fraction": float(np.mean(gains < -1.0)),
            }
    return summary


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [(d, i) for d in DISTANCES for i in range(GEOMS)]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for future in as_completed(futures):
            d, i = futures[future]
            rows.append(future.result())
            print(f"completed {int(d)} m #{i}", flush=True)
    rows.sort(key=lambda r: (r["distance_m"], r["index"]))
    summary = summarize(rows)
    overall = summary["overall"]
    criteria = {
        "softR_mean_gain_vs_hop_positive": overall["comparisons"]["softR_vs_hop"]["mean_gain_m"] > 0.0,
        "softR_p_vs_hop_lt_0_05": overall["comparisons"]["softR_vs_hop"]["wilcoxon_gain_gt0_p"] < 0.05,
        "softR_divergence_le_hop": overall["policies"]["hop_transition_softR"]["divergence_rate"] <= overall["policies"]["hop_baseline"]["divergence_rate"],
        "softR_mean_gain_vs_fixed_positive": overall["comparisons"]["softR_vs_fixed"]["mean_gain_m"] > 0.0,
    }
    payload = {
        "config": {
            "stage": "extended_range_transition_aware_validation",
            "distances_m": list(DISTANCES),
            "geometries_per_distance": GEOMS,
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "range_jump_threshold_m": RANGE_JUMP_THRESHOLD_M,
            "max_toa_scale": MAX_TOA_SCALE,
            "truth_usage": "truth is used for signal synthesis and final error computation only; softR decisions use observed TOA jump, carrier transition, disagreement, and NIS.",
            "manuscript_claim_allowed": "only after tail audit",
        },
        "summary": summary,
        "criteria": criteria,
        "decision": "extended_transition_aware_validated" if all(criteria.values()) else "extended_transition_aware_not_validated",
        "trials": rows,
    }
    out = HERE / "extended_transition_aware_validation.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"decision": payload["decision"], "criteria": criteria, "overall": overall}, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run()
