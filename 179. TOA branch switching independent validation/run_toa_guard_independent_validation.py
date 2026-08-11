"""Independent validation for the carrier-transition TOA guard.

This script reuses the adopted signal pipeline and guard implementation from
folder 162, but uses new independent static geometries and ping seeds.
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
F162 = next(ROOT.glob("162. *"))
sys.path.insert(0, str(F162))


from channel import synthesize_received  # noqa: E402
from conditional_adaptive import ConditionalAdaptiveRUKF  # noqa: E402
from config import ChannelConfig  # noqa: E402
from measurement import fixed_measurement_covariance, initialize_position  # noqa: E402
from peak_measurement import extract_measurement  # noqa: E402
from transition_guard import CarrierTransitionTOAGuardUKF  # noqa: E402
from ukf import SignalObservationUKF, acceleration_process_covariance  # noqa: E402


DISTANCE_M = 600.0
GEOMS = 20
STEPS = 20
SETTLE_START = 10
GEOM_ROOT = 1_790_000
PING_ROOT = 1_793_000
RANGE_JUMP_THRESHOLD_M = 0.5
ROUTING_THRESHOLD_DEG = 5.0


def schedules() -> dict[str, np.ndarray]:
    return {
        "fixed32": np.full(STEPS, 32_000.0),
        "linear20_30_34": np.linspace(30_000.0, 34_000.0, STEPS),
        "four_carrier_cycle": np.resize(
            np.array([30_000.0, 31_333.333333, 32_666.666667, 34_000.0]), STEPS
        ),
    }


SCHEDULES = schedules()


def geometry(index: int) -> tuple[np.ndarray, dict[str, float]]:
    rng = np.random.default_rng(GEOM_ROOT + index)
    azimuth = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    position = np.array([
        DISTANCE_M * np.cos(azimuth),
        DISTANCE_M * np.sin(azimuth),
        -depth,
    ])
    environment = {
        "snr_db": float(rng.choice([10.0, 20.0, 30.0])),
        "surface_reflection": float(-rng.uniform(0.72, 0.97)),
        "bottom_reflection": float(rng.uniform(0.32, 0.78)),
        "radial_velocity_m_s": 0.0,
    }
    return position, environment


def collect(position: np.ndarray, environment: dict[str, float], geometry_index: int, carriers_hz: np.ndarray):
    observations: list[np.ndarray] = []
    qualities: list[dict] = []
    raw_range_jumps: list[float] = []
    previous_range = None
    for ping_index, carrier_hz in enumerate(carriers_hz):
        cfg = replace(
            ChannelConfig(),
            seed=PING_ROOT + geometry_index * 100 + ping_index,
            carrier_hz=float(carrier_hz),
            **environment,
        )
        _, received, _ = synthesize_received(position, cfg)
        observation, quality = extract_measurement(received, cfg)
        observations.append(observation)
        qualities.append(quality)
        if previous_range is None:
            raw_range_jumps.append(0.0)
        else:
            raw_range_jumps.append(abs(float(observation[0]) - previous_range))
        previous_range = float(observation[0])
    return np.asarray(observations), qualities, raw_range_jumps


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


def run_filter(
    observations: np.ndarray,
    qualities: list[dict],
    position: np.ndarray,
    carriers_hz: np.ndarray,
    method: str,
) -> dict[str, Any]:
    ukf, initial = make_filter(observations[0])
    if method == "baseline_adaptive_r":
        wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    elif method == "transition_toa_guard":
        wrapper = CarrierTransitionTOAGuardUKF(
            ukf,
            ROUTING_THRESHOLD_DEG,
            range_jump_threshold_m=RANGE_JUMP_THRESHOLD_M,
        )
        wrapper.prime(observations[0], carriers_hz[0])
    else:
        raise ValueError(method)

    estimates = np.zeros((STEPS, 3))
    estimates[0] = initial
    exceptions = 0
    for ping_index in range(1, STEPS):
        try:
            if method == "baseline_adaptive_r":
                wrapper.step(observations[ping_index], qualities[ping_index])
            else:
                wrapper.step(observations[ping_index], qualities[ping_index], carriers_hz[ping_index])
            estimates[ping_index] = ukf.x[:3]
        except Exception:
            exceptions += 1
            estimates[ping_index] = estimates[ping_index - 1]

    errors = np.linalg.norm(estimates - position, axis=1)
    guarded = []
    max_guarded_jump = 0.0
    if method == "transition_toa_guard":
        guarded = [i + 1 for i, item in enumerate(wrapper.history) if item["toa_guarded"]]
        max_guarded_jump = max([item["range_jump_m"] for item in wrapper.history if item["toa_guarded"]] or [0.0])
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[SETTLE_START:] ** 2))),
        "median_settled_error_m": float(np.median(errors[SETTLE_START:])),
        "p90_settled_error_m": float(np.percentile(errors[SETTLE_START:], 90.0)),
        "maximum_position_error_m": float(np.max(errors)),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": exceptions,
        "toa_guard_count": len(guarded),
        "toa_guarded_ping_indices": guarded,
        "max_guarded_range_jump_m": float(max_guarded_jump),
    }


def run_geometry(index: int) -> list[dict[str, Any]]:
    position, environment = geometry(index)
    rows: list[dict[str, Any]] = []
    for schedule_name, carriers_hz in SCHEDULES.items():
        observations, qualities, raw_range_jumps = collect(position, environment, index, carriers_hz)
        for method in ("baseline_adaptive_r", "transition_toa_guard"):
            rows.append({
                "geometry_index": index,
                "schedule_name": schedule_name,
                "method": method,
                "environment": environment,
                "max_adjacent_raw_range_jump_m": float(max(raw_range_jumps)),
                **run_filter(observations, qualities, position, carriers_hz, method),
            })
    return rows


def bootstrap_ci(values: np.ndarray, seed: int = 179, n: int = 5000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def summarize(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    summary: dict[str, Any] = {}
    comparisons: dict[str, Any] = {}
    for schedule_name in SCHEDULES:
        summary[schedule_name] = {}
        methods = {}
        for method in ("baseline_adaptive_r", "transition_toa_guard"):
            subset = [r for r in rows if r["schedule_name"] == schedule_name and r["method"] == method]
            methods[method] = subset
            summary[schedule_name][method] = {
                "mean_settled_rmse_m": float(np.mean([r["settled_rmse_m"] for r in subset])),
                "median_settled_rmse_m": float(np.median([r["settled_rmse_m"] for r in subset])),
                "mean_p90_settled_error_m": float(np.mean([r["p90_settled_error_m"] for r in subset])),
                "divergence_rate": float(np.mean([r["diverged"] for r in subset])),
                "filter_exceptions": int(sum(r["filter_exceptions"] for r in subset)),
                "total_toa_guards": int(sum(r["toa_guard_count"] for r in subset)),
                "n_geometries": len(subset),
            }
        baseline = {r["geometry_index"]: r for r in methods["baseline_adaptive_r"]}
        guard = {r["geometry_index"]: r for r in methods["transition_toa_guard"]}
        gains = np.array([
            baseline[i]["settled_rmse_m"] - guard[i]["settled_rmse_m"]
            for i in sorted(baseline)
        ])
        try:
            p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
        except ValueError:
            p = 1.0
        comparisons[schedule_name] = {
            "mean_gain_m": float(np.mean(gains)),
            "median_gain_m": float(np.median(gains)),
            "gain_ci95": bootstrap_ci(gains),
            "wilcoxon_gain_gt0_p": p,
            "improved_fraction": float(np.mean(gains > 0.0)),
            "tail_worsened_fraction": float(np.mean(gains < -1.0)),
        }
    decision = {
        "guard_validated_for_four_carrier_tail": (
            comparisons["four_carrier_cycle"]["mean_gain_m"] > 0.0
            and comparisons["four_carrier_cycle"]["wilcoxon_gain_gt0_p"] < 0.05
            and summary["four_carrier_cycle"]["transition_toa_guard"]["divergence_rate"]
            <= summary["four_carrier_cycle"]["baseline_adaptive_r"]["divergence_rate"]
        ),
        "guard_non_degrading_for_linear20": (
            comparisons["linear20_30_34"]["mean_gain_m"] > -0.5
            and comparisons["linear20_30_34"]["tail_worsened_fraction"] <= 0.10
        ),
        "fixed32_no_effect_expected": summary["fixed32"]["transition_toa_guard"]["total_toa_guards"] == 0,
    }
    return summary, {"comparisons": comparisons, "criteria": decision}


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_geometry, index): index for index in range(GEOMS)}
        for future in as_completed(futures):
            index = futures[future]
            rows.extend(future.result())
            print(f"completed independent geometry {index}", flush=True)
    rows.sort(key=lambda r: (r["geometry_index"], r["schedule_name"], r["method"]))
    summary, compare_payload = summarize(rows)
    criteria = compare_payload["criteria"]
    payload = {
        "config": {
            "stage": "independent_validation",
            "source_pilot": "162. Carrier transition TOA guard pilot",
            "distance_m": DISTANCE_M,
            "geometries": GEOMS,
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "range_jump_threshold_m": RANGE_JUMP_THRESHOLD_M,
            "toa_guard_variance_m2": 1.0e12,
            "common_random_ping_seeds": True,
            "manuscript_claim_allowed": False,
            "truth_usage": "truth is used for signal synthesis and final error computation only; guard decisions use carrier transition and observed reference TOA jump.",
        },
        "summary": summary,
        **compare_payload,
        "decision": (
            "validated_for_static_four_carrier_tail"
            if all(criteria.values())
            else "not_validated_as_general_static_guard"
        ),
        "trials": rows,
    }
    out = HERE / "toa_guard_independent_validation.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "decision": payload["decision"],
        "criteria": criteria,
        "comparisons": compare_payload["comparisons"],
    }, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run()
