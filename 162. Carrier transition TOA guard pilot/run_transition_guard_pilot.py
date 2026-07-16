"""Post-hoc development pilot of the carrier-transition-aware TOA guard."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
import json

import numpy as np

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from peak_measurement import extract_measurement
from transition_guard import CarrierTransitionTOAGuardUKF
from ukf import SignalObservationUKF, acceleration_process_covariance


HERE = Path(__file__).resolve().parent
DISTANCE_M = 600
STEPS = 20
SETTLE_START = 10
GEOM_ROOT = 1_600_000
PING_ROOT = 1_603_000
DEVELOPMENT_GEOMETRIES = (2, 5, 19)
RANGE_JUMP_THRESHOLD_M = 0.5


def make_schedules() -> dict[str, np.ndarray]:
    linear = np.linspace(30_000.0, 34_000.0, STEPS)
    return {
        "fixed32": np.full(STEPS, 32_000.0),
        "linear20_30_34": linear,
        "four_carrier_cycle": np.resize(
            np.array([30_000.0, 31_333.333333, 32_666.666667, 34_000.0]), STEPS
        ),
    }


SCHEDULES = make_schedules()


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


def collect(position, environment, geometry_index, carriers_hz):
    observations, qualities = [], []
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


def run_filter(observations, qualities, position, carriers_hz, method):
    ukf, initial = make_filter(observations[0])
    if method == "baseline_adaptive_r":
        wrapper = ConditionalAdaptiveRUKF(ukf, 5.0)
    elif method == "transition_toa_guard":
        wrapper = CarrierTransitionTOAGuardUKF(
            ukf, 5.0, range_jump_threshold_m=RANGE_JUMP_THRESHOLD_M
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
                wrapper.step(
                    observations[ping_index], qualities[ping_index], carriers_hz[ping_index]
                )
            estimates[ping_index] = ukf.x[:3]
        except Exception:
            exceptions += 1
            estimates[ping_index] = estimates[ping_index - 1]
    errors = np.linalg.norm(estimates - position, axis=1)
    guarded = [] if method == "baseline_adaptive_r" else [
        index + 1 for index, item in enumerate(wrapper.history) if item["toa_guarded"]
    ]
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[SETTLE_START:] ** 2))),
        "maximum_position_error_m": float(np.max(errors)),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": exceptions,
        "toa_guard_count": len(guarded),
        "toa_guarded_ping_indices": guarded,
        "position_error_trace_m": [float(value) for value in errors],
    }


def run_geometry(index: int) -> list[dict]:
    position, environment = geometry(index)
    rows = []
    for schedule_name, carriers_hz in SCHEDULES.items():
        observations, qualities = collect(position, environment, index, carriers_hz)
        for method in ("baseline_adaptive_r", "transition_toa_guard"):
            rows.append({
                "geometry_index": index,
                "schedule_name": schedule_name,
                "method": method,
                **run_filter(observations, qualities, position, carriers_hz, method),
            })
    return rows


def summarize(rows: list[dict]) -> dict:
    summary = {}
    for schedule_name in SCHEDULES:
        summary[schedule_name] = {}
        for method in ("baseline_adaptive_r", "transition_toa_guard"):
            subset = [
                row for row in rows
                if row["schedule_name"] == schedule_name and row["method"] == method
            ]
            summary[schedule_name][method] = {
                "mean_settled_rmse_m": float(np.mean([row["settled_rmse_m"] for row in subset])),
                "median_settled_rmse_m": float(np.median([row["settled_rmse_m"] for row in subset])),
                "divergence_count": int(sum(row["diverged"] for row in subset)),
                "filter_exceptions": int(sum(row["filter_exceptions"] for row in subset)),
                "total_toa_guards": int(sum(row["toa_guard_count"] for row in subset)),
                "n_geometries": len(subset),
            }
    catastrophic = {
        (row["schedule_name"], row["method"]): row
        for row in rows if row["geometry_index"] == 2
    }
    criteria = {
        "catastrophic_four_rmse_reduced_by_75pct": (
            catastrophic[("four_carrier_cycle", "transition_toa_guard")]["settled_rmse_m"]
            <= 0.25 * catastrophic[("four_carrier_cycle", "baseline_adaptive_r")]["settled_rmse_m"]
        ),
        "catastrophic_four_no_divergence": not catastrophic[("four_carrier_cycle", "transition_toa_guard")]["diverged"],
        "four_mean_rmse_reduced": (
            summary["four_carrier_cycle"]["transition_toa_guard"]["mean_settled_rmse_m"]
            < summary["four_carrier_cycle"]["baseline_adaptive_r"]["mean_settled_rmse_m"]
        ),
        "linear_mean_rmse_within_10pct": (
            summary["linear20_30_34"]["transition_toa_guard"]["mean_settled_rmse_m"]
            <= 1.10 * summary["linear20_30_34"]["baseline_adaptive_r"]["mean_settled_rmse_m"]
        ),
        "no_guard_filter_exceptions": all(
            summary[name]["transition_toa_guard"]["filter_exceptions"] == 0
            for name in SCHEDULES
        ),
    }
    return summary, criteria


def run(max_workers: int = 3) -> dict:
    rows = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_geometry, index): index for index in DEVELOPMENT_GEOMETRIES}
        for future in as_completed(futures):
            index = futures[future]
            rows.extend(future.result())
            print(f"completed development geometry {index}", flush=True)
    rows.sort(key=lambda row: (row["geometry_index"], row["schedule_name"], row["method"]))
    summary, criteria = summarize(rows)
    payload = {
        "config": {
            "stage": "post_hoc_development_pilot",
            "source_diagnostic": "161. Sparse carrier tail mechanism diagnostic",
            "development_geometries": list(DEVELOPMENT_GEOMETRIES),
            "range_jump_threshold_m": RANGE_JUMP_THRESHOLD_M,
            "toa_guard_variance_m2": 1.0e12,
            "static_scope_only": True,
            "independent_validation_required": True,
            "manuscript_claim_allowed": False,
        },
        "summary": summary,
        "criteria": criteria,
        "decision": "advance_to_independent_validation" if all(criteria.values()) else "reject_guard",
        "trials": rows,
    }
    output = HERE / "results"
    output.mkdir(exist_ok=True)
    (output / "transition_toa_guard_pilot.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({"summary": summary, "criteria": criteria, "decision": payload["decision"]}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
