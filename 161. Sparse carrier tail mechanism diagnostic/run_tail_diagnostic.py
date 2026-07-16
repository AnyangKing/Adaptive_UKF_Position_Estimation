"""Post-validation diagnostic of sparse-carrier tail cases from folder 160.

This script exactly replays three already classified geometries and records
per-ping measurements and filter diagnostics.  It is explanatory, not a new
independent performance test and must not be used to rescue the failed
four-carrier candidate.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
import json

import numpy as np

from channel import paths_for_sensor, synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig, usb_array_global_m
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position, wrap_angle
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


HERE = Path(__file__).resolve().parent
DISTANCE_M = 600
STEPS = 20
SETTLE_START = 10
GEOM_ROOT = 1_600_000
PING_ROOT = 1_603_000
DIAGNOSTIC_GEOMETRIES = (2, 5, 19)  # catastrophic, moderate-negative, strong-positive


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


def direct_surface_delay_us(position: np.ndarray, environment: dict[str, float]) -> float:
    cfg = replace(ChannelConfig(), **environment)
    sensor = usb_array_global_m(cfg.receiver_depth_m)[0]
    paths = {path.name: path.delay_s for path in paths_for_sensor(position, sensor, cfg)}
    return float((paths["surface"] - paths["direct"]) * 1.0e6)


def collect(
    position: np.ndarray,
    environment: dict[str, float],
    geometry_index: int,
    carriers_hz: np.ndarray,
) -> tuple[np.ndarray, list[dict[str, float]]]:
    observations = []
    qualities = []
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


def run_trace(
    observations: np.ndarray,
    qualities: list[dict[str, float]],
    position: np.ndarray,
    carriers_hz: np.ndarray,
) -> tuple[list[dict], dict]:
    cfg = ChannelConfig()
    truth = ideal_measurement(position, cfg)
    initial = initialize_position(observations[0], cfg)
    ukf = SignalObservationUKF(
        np.r_[initial, np.zeros(3)],
        np.diag([8.0**2] * 3 + [1.5**2] * 3),
        acceleration_process_covariance(1.0, 0.20),
        fixed_measurement_covariance(),
        cfg,
    )
    wrapper = ConditionalAdaptiveRUKF(ukf, 5.0)

    def block_nis(residual: np.ndarray, covariance: np.ndarray, indices: slice) -> float:
        value = residual[indices]
        block = covariance[indices, indices]
        return float(value @ np.linalg.solve(block, value))

    trace = [{
        "ping_index": 0,
        "carrier_khz": float(carriers_hz[0] / 1000.0),
        "raw_azimuth_bias_deg": float(np.degrees(wrap_angle(observations[0, 8] - truth[8]))),
        "raw_elevation_bias_deg": float(np.degrees(wrap_angle(observations[0, 9] - truth[9]))),
        "raw_range_error_m": float(observations[0, 0] - truth[0]),
        "raw_tdoa_error_rms_m": float(np.sqrt(np.mean((observations[0, 1:8] - truth[1:8]) ** 2))),
        "doa_disagreement_deg": float(qualities[0]["doa_disagreement_deg"]),
        "position_error_m": float(np.linalg.norm(initial - position)),
        "routed_to_tdoa": None,
        "total_nis": None,
        "toa_block_nis": None,
        "tdoa_block_nis": None,
        "doa_block_nis": None,
        "toa_innovation_m": None,
        "tdoa_innovation_rms_m": None,
        "elevation_innovation_deg": None,
    }]
    exceptions = 0
    for ping_index in range(1, STEPS):
        try:
            wrapper.step(observations[ping_index], qualities[ping_index])
            history = wrapper.history[-1]
            routed = bool(history["routed"])
            nis = float(history["nis"])
            innovation_deg = float(np.degrees(history["innovation"][9]))
            toa_nis = block_nis(history["innovation"], history["S"], slice(0, 1))
            tdoa_nis = block_nis(history["innovation"], history["S"], slice(1, 8))
            doa_nis = block_nis(history["innovation"], history["S"], slice(8, 10))
            toa_innovation = float(history["innovation"][0])
            tdoa_innovation_rms = float(np.sqrt(np.mean(history["innovation"][1:8] ** 2)))
        except Exception:
            exceptions += 1
            routed, nis, innovation_deg = None, None, None
            toa_nis, tdoa_nis, doa_nis = None, None, None
            toa_innovation, tdoa_innovation_rms = None, None
        trace.append({
            "ping_index": ping_index,
            "carrier_khz": float(carriers_hz[ping_index] / 1000.0),
            "raw_azimuth_bias_deg": float(np.degrees(wrap_angle(observations[ping_index, 8] - truth[8]))),
            "raw_elevation_bias_deg": float(np.degrees(wrap_angle(observations[ping_index, 9] - truth[9]))),
            "raw_range_error_m": float(observations[ping_index, 0] - truth[0]),
            "raw_tdoa_error_rms_m": float(np.sqrt(np.mean((observations[ping_index, 1:8] - truth[1:8]) ** 2))),
            "doa_disagreement_deg": float(qualities[ping_index]["doa_disagreement_deg"]),
            "position_error_m": float(np.linalg.norm(ukf.x[:3] - position)),
            "routed_to_tdoa": routed,
            "total_nis": nis,
            "toa_block_nis": toa_nis,
            "tdoa_block_nis": tdoa_nis,
            "doa_block_nis": doa_nis,
            "toa_innovation_m": toa_innovation,
            "tdoa_innovation_rms_m": tdoa_innovation_rms,
            "elevation_innovation_deg": innovation_deg,
        })
    settled = np.asarray([row["position_error_m"] for row in trace[SETTLE_START:]])
    raw_range_errors = np.asarray([row["raw_range_error_m"] for row in trace])
    raw_range_jumps = np.abs(np.diff(raw_range_errors))
    valid_nis = [row["total_nis"] for row in trace if row["total_nis"] is not None]
    valid_toa_nis = [row["toa_block_nis"] for row in trace if row["toa_block_nis"] is not None]
    valid_tdoa_nis = [row["tdoa_block_nis"] for row in trace if row["tdoa_block_nis"] is not None]
    valid_doa_nis = [row["doa_block_nis"] for row in trace if row["doa_block_nis"] is not None]
    summary = {
        "settled_rmse_m": float(np.sqrt(np.mean(settled**2))),
        "maximum_position_error_m": float(max(row["position_error_m"] for row in trace)),
        "maximum_total_nis": float(max(valid_nis)) if valid_nis else None,
        "maximum_toa_block_nis": float(max(valid_toa_nis)) if valid_toa_nis else None,
        "maximum_tdoa_block_nis": float(max(valid_tdoa_nis)) if valid_tdoa_nis else None,
        "maximum_doa_block_nis": float(max(valid_doa_nis)) if valid_doa_nis else None,
        "raw_range_error_span_m": float(np.ptp(raw_range_errors)),
        "raw_range_error_total_variation_m": float(np.sum(raw_range_jumps)),
        "maximum_adjacent_raw_range_jump_m": float(np.max(raw_range_jumps)),
        "adjacent_raw_range_jumps_over_0_5m": int(np.sum(raw_range_jumps > 0.5)),
        "mean_abs_raw_elevation_bias_deg": float(np.mean([abs(row["raw_elevation_bias_deg"]) for row in trace])),
        "maximum_abs_raw_elevation_bias_deg": float(max(abs(row["raw_elevation_bias_deg"]) for row in trace)),
        "large_error_ping_indices": [row["ping_index"] for row in trace if row["position_error_m"] > 50.0],
        "filter_exceptions": exceptions,
    }
    return trace, summary


def summarize_four_carriers(trace: list[dict]) -> list[dict]:
    output = []
    for carrier in sorted({row["carrier_khz"] for row in trace}):
        rows = [row for row in trace if row["carrier_khz"] == carrier]
        output.append({
            "carrier_khz": carrier,
            "n": len(rows),
            "mean_raw_elevation_bias_deg": float(np.mean([row["raw_elevation_bias_deg"] for row in rows])),
            "mean_abs_raw_elevation_bias_deg": float(np.mean([abs(row["raw_elevation_bias_deg"]) for row in rows])),
            "mean_raw_range_error_m": float(np.mean([row["raw_range_error_m"] for row in rows])),
            "mean_position_error_m": float(np.mean([row["position_error_m"] for row in rows])),
        })
    return output


def run_geometry(index: int) -> dict:
    position, environment = geometry(index)
    schedules = {}
    for name, carriers in SCHEDULES.items():
        observations, qualities = collect(position, environment, index, carriers)
        trace, summary = run_trace(observations, qualities, position, carriers)
        schedules[name] = {"summary": summary, "trace": trace}
        if name == "four_carrier_cycle":
            schedules[name]["by_carrier"] = summarize_four_carriers(trace)
    return {
        "geometry_index": index,
        "position_m": position.tolist(),
        "environment": environment,
        "surface_direct_delay_us": direct_surface_delay_us(position, environment),
        "classification_from_160": {
            2: "catastrophic_negative",
            5: "moderate_negative",
            19: "strong_positive",
        }[index],
        "schedules": schedules,
    }


def run(max_workers: int = 3) -> dict:
    geometries = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_geometry, index): index for index in DIAGNOSTIC_GEOMETRIES}
        for future in as_completed(futures):
            index = futures[future]
            geometries.append(future.result())
            print(f"completed diagnostic geometry {index}", flush=True)
    geometries.sort(key=lambda row: row["geometry_index"])
    payload = {
        "config": {
            "stage": "post_validation_tail_mechanism_diagnostic",
            "source_validation": "160. Four carrier independent static validation",
            "diagnostic_geometries": list(DIAGNOSTIC_GEOMETRIES),
            "same_seed_exact_replay": True,
            "independent_performance_claim_allowed": False,
            "failed_candidate_rescue_allowed": False,
        },
        "geometries": geometries,
    }
    output = HERE / "results"
    output.mkdir(exist_ok=True)
    (output / "sparse_carrier_tail_diagnostic.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    compact = {
        geometry["geometry_index"]: {
            name: values["summary"] for name, values in geometry["schedules"].items()
        }
        for geometry in geometries
    }
    print(json.dumps(compact, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
