"""Independent static validation of the four-carrier schedule selected in 159.

The candidate, sample size, seeds, endpoints, and decision rules were frozen
before execution.  Folder 159 data are not reused.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
import json
import math

import numpy as np
from scipy.stats import wilcoxon

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


HERE = Path(__file__).resolve().parent
DISTANCE_M = 600
GEOMS = 20
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0
GEOM_ROOT = 1_600_000
PING_ROOT = 1_603_000


def make_schedules() -> dict[str, np.ndarray]:
    linear = np.linspace(30_000.0, 34_000.0, STEPS)
    return {
        "fixed32": np.full(STEPS, 32_000.0),
        "linear20_30_34": linear,
        "four_carrier_cycle": np.resize(
            np.array([30_000.0, 31_333.333333, 32_666.666667, 34_000.0]),
            STEPS,
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


def collect(
    position: np.ndarray,
    environment: dict[str, float],
    geometry_index: int,
    carriers_hz: np.ndarray,
) -> tuple[np.ndarray, list[dict[str, float]]]:
    observations: list[np.ndarray] = []
    qualities: list[dict[str, float]] = []
    for ping_index, carrier_hz in enumerate(carriers_hz):
        # Common ping seeds across schedules reduce Monte-Carlo noise while the
        # carrier assigned to a ping remains the schedule intervention.
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


def lag1(values: list[float]) -> float | None:
    array = np.asarray(values, dtype=float)
    if len(array) < 3 or np.std(array[:-1]) < 1.0e-12 or np.std(array[1:]) < 1.0e-12:
        return None
    return float(np.corrcoef(array[:-1], array[1:])[0, 1])


def run_filter(
    observations: np.ndarray,
    qualities: list[dict[str, float]],
    position: np.ndarray,
) -> dict[str, float | bool | None]:
    cfg = ChannelConfig()
    initial = initialize_position(observations[0], cfg)
    ukf = SignalObservationUKF(
        np.r_[initial, np.zeros(3)],
        np.diag([8.0**2] * 3 + [1.5**2] * 3),
        acceleration_process_covariance(1.0, 0.20),
        fixed_measurement_covariance(),
        cfg,
    )
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    estimates = np.zeros((STEPS, 3))
    estimates[0] = initial
    exceptions = 0
    for ping_index in range(1, STEPS):
        try:
            wrapper.step(observations[ping_index], qualities[ping_index])
            estimates[ping_index] = ukf.x[:3]
        except Exception:
            exceptions += 1
            estimates[ping_index] = estimates[ping_index - 1]
    errors = np.linalg.norm(estimates - position, axis=1)
    elevation_innovations = [float(item["innovation"][9]) for item in wrapper.history]
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[SETTLE_START:] ** 2))),
        "p90_settled_error_m": float(np.percentile(errors[SETTLE_START:], 90)),
        "elevation_innovation_lag1": lag1(elevation_innovations),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": exceptions,
    }


def run_geometry(index: int) -> list[dict]:
    position, environment = geometry(index)
    rows = []
    for schedule_name, carriers_hz in SCHEDULES.items():
        observations, qualities = collect(position, environment, index, carriers_hz)
        metrics = run_filter(observations, qualities, position)
        rows.append({
            "geometry_index": index,
            "schedule_name": schedule_name,
            "position_m": position.tolist(),
            "environment": environment,
            **metrics,
        })
    return rows


def summarize(rows: list[dict]) -> dict[str, dict]:
    by_name = {
        name: [row for row in rows if row["schedule_name"] == name]
        for name in SCHEDULES
    }
    summaries: dict[str, dict] = {}
    for name, schedule_rows in by_name.items():
        rmse = np.asarray([row["settled_rmse_m"] for row in schedule_rows])
        p90 = np.asarray([row["p90_settled_error_m"] for row in schedule_rows])
        lags = np.asarray([
            abs(row["elevation_innovation_lag1"])
            for row in schedule_rows
            if row["elevation_innovation_lag1"] is not None
        ])
        summaries[name] = {
            "mean_settled_rmse_m": float(np.mean(rmse)),
            "median_settled_rmse_m": float(np.median(rmse)),
            "mean_p90_settled_error_m": float(np.mean(p90)),
            "mean_abs_elevation_innovation_lag1": float(np.mean(lags)) if len(lags) else None,
            "divergence_rate": float(np.mean([row["diverged"] for row in schedule_rows])),
            "filter_exceptions": int(sum(row["filter_exceptions"] for row in schedule_rows)),
            "n_geometries": len(schedule_rows),
        }
    return summaries


def bootstrap_mean_ci(values: np.ndarray, seed: int, draws: int = 10_000) -> list[float]:
    rng = np.random.default_rng(seed)
    sampled = rng.choice(values, size=(draws, len(values)), replace=True).mean(axis=1)
    return [float(np.percentile(sampled, 2.5)), float(np.percentile(sampled, 97.5))]


def paired_comparison(
    rows: list[dict],
    candidate: str,
    reference: str,
    require_lag_reduction: bool,
) -> dict:
    candidate_rows = {row["geometry_index"]: row for row in rows if row["schedule_name"] == candidate}
    reference_rows = {row["geometry_index"]: row for row in rows if row["schedule_name"] == reference}
    indices = sorted(candidate_rows)
    candidate_rmse = np.asarray([candidate_rows[index]["settled_rmse_m"] for index in indices])
    reference_rmse = np.asarray([reference_rows[index]["settled_rmse_m"] for index in indices])
    gains = reference_rmse - candidate_rmse
    candidate_lag = np.asarray([abs(candidate_rows[index]["elevation_innovation_lag1"]) for index in indices])
    reference_lag = np.asarray([abs(reference_rows[index]["elevation_innovation_lag1"]) for index in indices])
    lag_reduction = float(np.mean(reference_lag - candidate_lag))
    try:
        p_value = float(wilcoxon(gains, alternative="greater").pvalue)
    except ValueError:
        p_value = 1.0
    criteria = {
        "mean_gain_positive": bool(np.mean(gains) > 0.0),
        "median_gain_positive": bool(np.median(gains) > 0.0),
        "improved_fraction_ge_0_60": bool(np.mean(gains > 0.0) >= 0.60),
        "p90_rmse_not_worse": bool(np.percentile(candidate_rmse, 90) <= np.percentile(reference_rmse, 90)),
        "wilcoxon_greater_p_lt_0_05": bool(p_value < 0.05),
        "no_candidate_divergence": not any(candidate_rows[index]["diverged"] for index in indices),
    }
    if require_lag_reduction:
        criteria["mean_abs_lag1_reduced"] = bool(lag_reduction > 0.0)
    return {
        "candidate": candidate,
        "reference": reference,
        "mean_gain_m": float(np.mean(gains)),
        "mean_gain_ci95_m": bootstrap_mean_ci(gains, GEOM_ROOT + len(candidate) + len(reference)),
        "median_gain_m": float(np.median(gains)),
        "improved_fraction": float(np.mean(gains > 0.0)),
        "p90_rmse_gain_m": float(np.percentile(reference_rmse, 90) - np.percentile(candidate_rmse, 90)),
        "mean_abs_lag1_reduction": lag_reduction,
        "wilcoxon_greater_p": p_value,
        "criteria": criteria,
        "pass": all(criteria.values()),
        "n": len(indices),
    }


def run(max_workers: int = 4) -> dict:
    rows: list[dict] = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {executor.submit(run_geometry, index): index for index in range(GEOMS)}
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            rows.extend(future.result())
            print(f"completed geometry {index + 1}/{GEOMS}", flush=True)
    rows.sort(key=lambda row: (row["geometry_index"], row["schedule_name"]))
    summaries = summarize(rows)
    comparisons = {
        "linear_vs_fixed": paired_comparison(rows, "linear20_30_34", "fixed32", True),
        "four_vs_fixed": paired_comparison(rows, "four_carrier_cycle", "fixed32", True),
        "four_vs_linear": paired_comparison(rows, "four_carrier_cycle", "linear20_30_34", False),
    }
    if comparisons["four_vs_fixed"]["pass"] and comparisons["four_vs_linear"]["pass"]:
        decision = "validated_superior_to_fixed_and_linear"
    elif comparisons["four_vs_fixed"]["pass"]:
        decision = "validated_vs_fixed_not_superior_to_linear"
    else:
        decision = "independent_validation_failed"
    payload = {
        "config": {
            "stage": "stage1b_independent_validation",
            "distance_m": DISTANCE_M,
            "geometries": GEOMS,
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "common_random_ping_seeds": True,
            "schedule_carriers_khz": {
                name: [float(value / 1000.0) for value in carriers]
                for name, carriers in SCHEDULES.items()
            },
            "development_only": False,
            "independent_validation": True,
            "protocol_frozen_before_execution": True,
            "selection_source": "159. Reduced static schedule UKF pilot",
            "automatic_manuscript_update_allowed": False,
        },
        "summary": summaries,
        "comparisons": comparisons,
        "decision": decision,
        "trials": rows,
    }
    output = HERE / "results"
    output.mkdir(exist_ok=True)
    (output / "four_carrier_independent_validation.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summaries, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
