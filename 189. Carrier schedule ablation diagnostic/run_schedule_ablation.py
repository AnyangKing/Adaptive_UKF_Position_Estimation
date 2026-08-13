"""Carrier schedule ablation diagnostic at 600 m static range."""

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


DISTANCE_M = 600.0
GEOMS = 8
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0
GEOM_ROOT = 1_890_000
PING_ROOT = 1_893_000


def schedules() -> dict[str, list[float]]:
    linear = np.linspace(30_000.0, 34_000.0, STEPS)
    rng = np.random.default_rng(189_123)
    shuffled = np.array(linear)
    rng.shuffle(shuffled)
    sparse = np.resize(np.linspace(30_000.0, 34_000.0, 5), STEPS)
    return {
        "fixed32": list(np.full(STEPS, 32_000.0)),
        "linear20_30_34": list(linear),
        "reverse20_34_30": list(linear[::-1]),
        "shuffled20_30_34": list(shuffled),
        "narrow20_31_33": list(np.linspace(31_000.0, 33_000.0, STEPS)),
        "sparse5_30_34_repeat": list(sparse),
    }


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


def collect(position: np.ndarray, environment: dict[str, float], index: int, carriers: list[float]):
    observations: list[np.ndarray] = []
    qualities: list[dict] = []
    for ping_index, carrier_hz in enumerate(carriers):
        cfg = replace(
            ChannelConfig(),
            seed=PING_ROOT + index * 100 + ping_index,
            carrier_hz=float(carrier_hz),
            **environment,
        )
        _, received, _ = synthesize_received(
            position,
            cfg,
            include_multipath=True,
            include_noise=True,
        )
        observation, quality = extract_measurement(received, cfg)
        observations.append(observation)
        qualities.append(quality)
    return np.asarray(observations), qualities


def run_filter(observations: np.ndarray, qualities: list[dict], position: np.ndarray) -> dict[str, Any]:
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
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[SETTLE_START:] ** 2))),
        "median_settled_error_m": float(np.median(errors[SETTLE_START:])),
        "p90_settled_error_m": float(np.percentile(errors[SETTLE_START:], 90.0)),
        "maximum_position_error_m": float(np.max(errors)),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": int(exceptions),
    }


def run_case(index: int) -> dict[str, Any]:
    position, environment = geometry(index)
    result: dict[str, Any] = {
        "distance_m": DISTANCE_M,
        "index": index,
        "environment": environment,
        "policies": {},
    }
    for name, carriers in schedules().items():
        observations, qualities = collect(position, environment, index, carriers)
        result["policies"][name] = run_filter(observations, qualities, position)
    return result


def bootstrap_ci(values: np.ndarray, seed: int = 189, n: int = 5000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    schedule_names = list(schedules())
    summary: dict[str, Any] = {"policies": {}, "comparisons_vs_fixed": {}}
    fixed = np.array([row["policies"]["fixed32"]["settled_rmse_m"] for row in rows])
    for name in schedule_names:
        values = np.array([row["policies"][name]["settled_rmse_m"] for row in rows])
        summary["policies"][name] = {
            "mean_rmse_m": float(np.mean(values)),
            "median_rmse_m": float(np.median(values)),
            "mean_p90_error_m": float(np.mean([row["policies"][name]["p90_settled_error_m"] for row in rows])),
            "divergence_rate": float(np.mean([row["policies"][name]["diverged"] for row in rows])),
            "n": len(rows),
        }
        if name == "fixed32":
            continue
        gains = fixed - values
        try:
            p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
        except ValueError:
            p = 1.0
        summary["comparisons_vs_fixed"][name] = {
            "mean_gain_m": float(np.mean(gains)),
            "median_gain_m": float(np.median(gains)),
            "gain_ci95": bootstrap_ci(gains),
            "wilcoxon_gain_gt0_p": p,
            "improved_fraction": float(np.mean(gains > 0.0)),
            "tail_worsened_fraction": float(np.mean([
                row["policies"][name]["p90_settled_error_m"] > row["policies"]["fixed32"]["p90_settled_error_m"]
                for row in rows
            ])),
        }
    return summary


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Carrier schedule ablation result summary",
        "",
        "| schedule | mean RMSE | gain vs fixed | p | improved frac | tail worsened |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    summary = payload["summary"]
    fixed_mean = summary["policies"]["fixed32"]["mean_rmse_m"]
    lines.append(f"| fixed32 | {fixed_mean:.3f} | 0.000 |  |  |  |")
    for name, comp in summary["comparisons_vs_fixed"].items():
        mean_rmse = summary["policies"][name]["mean_rmse_m"]
        lines.append(
            f"| {name} | {mean_rmse:.3f} | {comp['mean_gain_m']:.3f} | "
            f"{comp['wilcoxon_gain_gt0_p']:.4g} | {comp['improved_fraction']:.3f} | "
            f"{comp['tail_worsened_fraction']:.3f} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "This is a compact schedule diagnostic at one range, not a final optimization study.",
        "",
        "The main question is whether the manuscript should describe the 30--34 kHz linear schedule as a frozen validated schedule, a generally optimal schedule, or only one workable schedule inside a broader design space.",
    ])
    return "\n".join(lines) + "\n"


def main(max_workers: int = 4) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, index): index for index in range(GEOMS)}
        for future in as_completed(futures):
            index = futures[future]
            rows.append(future.result())
            print(f"completed schedule ablation geom #{index}", flush=True)
    rows.sort(key=lambda row: row["index"])
    payload = {
        "config": {
            "stage": "finite_schedule_ablation_diagnostic",
            "distance_m": DISTANCE_M,
            "geometries": GEOMS,
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "include_multipath": True,
            "include_noise": True,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "truth_usage": "truth is used for signal synthesis and final error computation only.",
            "claim_boundary": "diagnostic only; not schedule optimization",
            "schedules_hz": schedules(),
        },
        "summary": summarize(rows),
        "trials": rows,
    }
    (HERE / "schedule_ablation.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (HERE / "result_summary.md").write_text(markdown(payload), encoding="utf-8")
    print(markdown(payload))
    return payload


if __name__ == "__main__":
    main()

