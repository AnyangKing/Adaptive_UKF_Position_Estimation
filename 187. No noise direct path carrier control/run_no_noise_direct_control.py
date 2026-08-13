"""No-noise direct-path-only carrier-agility control experiment."""

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


DISTANCES = (600.0, 800.0, 1000.0)
GEOMS = 8
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0
FIXED_CARRIER_HZ = 32_000.0
HOP_CARRIERS_HZ = np.linspace(30_000.0, 34_000.0, STEPS)
GEOM_ROOT = 1_870_000
PING_ROOT = 1_873_000


def geometry(distance: float, index: int) -> tuple[np.ndarray, dict[str, float]]:
    rng = np.random.default_rng(GEOM_ROOT + int(distance) * 50 + index)
    azimuth = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    position = np.array([
        distance * np.cos(azimuth),
        distance * np.sin(azimuth),
        -depth,
    ])
    environment = {
        # Kept in metadata for comparability with 185, but noise is disabled below.
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
        _, received, _ = synthesize_received(
            position,
            cfg,
            include_multipath=False,
            include_noise=False,
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


def run_case(distance: float, index: int) -> dict[str, Any]:
    position, environment = geometry(distance, index)
    fixed_carriers = np.full(STEPS, FIXED_CARRIER_HZ)
    obs_fixed, q_fixed = collect(position, environment, distance, index, fixed_carriers)
    obs_hop, q_hop = collect(position, environment, distance, index, HOP_CARRIERS_HZ)
    fixed = run_filter(obs_fixed, q_fixed, position)
    hop = run_filter(obs_hop, q_hop, position)
    return {
        "distance_m": distance,
        "index": index,
        "environment": environment,
        "fixed32": fixed,
        "linear20_30_34": hop,
        "gain_m": fixed["settled_rmse_m"] - hop["settled_rmse_m"],
    }


def bootstrap_ci(values: np.ndarray, seed: int = 187, n: int = 5000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for distance in list(DISTANCES) + ["overall"]:
        subset = rows if distance == "overall" else [r for r in rows if r["distance_m"] == distance]
        gains = np.array([r["gain_m"] for r in subset])
        try:
            p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
        except ValueError:
            p = 1.0
        summary[str(distance)] = {
            "fixed_mean_rmse_m": float(np.mean([r["fixed32"]["settled_rmse_m"] for r in subset])),
            "hop_mean_rmse_m": float(np.mean([r["linear20_30_34"]["settled_rmse_m"] for r in subset])),
            "fixed_median_rmse_m": float(np.median([r["fixed32"]["settled_rmse_m"] for r in subset])),
            "hop_median_rmse_m": float(np.median([r["linear20_30_34"]["settled_rmse_m"] for r in subset])),
            "fixed_mean_p90_error_m": float(np.mean([r["fixed32"]["p90_settled_error_m"] for r in subset])),
            "hop_mean_p90_error_m": float(np.mean([r["linear20_30_34"]["p90_settled_error_m"] for r in subset])),
            "mean_gain_m": float(np.mean(gains)),
            "median_gain_m": float(np.median(gains)),
            "gain_ci95": bootstrap_ci(gains),
            "wilcoxon_gain_gt0_p": p,
            "improved_fraction": float(np.mean(gains > 0.0)),
            "fixed_divergence_rate": float(np.mean([r["fixed32"]["diverged"] for r in subset])),
            "hop_divergence_rate": float(np.mean([r["linear20_30_34"]["diverged"] for r in subset])),
            "n": len(subset),
        }
    return summary


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# No-noise direct-path control result summary",
        "",
        "| distance | fixed mean | hop mean | mean gain | p | fixed div | hop div |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for key in ["600.0", "800.0", "1000.0", "overall"]:
        s = payload["summary"][key]
        lines.append(
            f"| {key} | {s['fixed_mean_rmse_m']:.3f} | {s['hop_mean_rmse_m']:.3f} | "
            f"{s['mean_gain_m']:.3f} | {s['wilcoxon_gain_gt0_p']:.4g} | "
            f"{s['fixed_divergence_rate']:.3f} | {s['hop_divergence_rate']:.3f} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "This control removes both explicit multipath and additive receiver noise.",
        "",
        "If a carrier-agile advantage remains here, the manuscript must not attribute all long-range improvement to multipath phase diversification or colored noise.",
        "",
        "If the advantage disappears here but remains in folder 185, additive noise / extraction-noise interaction becomes the more likely residual mechanism.",
    ])
    return "\n".join(lines) + "\n"


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [(d, i) for d in DISTANCES for i in range(GEOMS)]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for future in as_completed(futures):
            d, i = futures[future]
            rows.append(future.result())
            print(f"completed no-noise direct-only {int(d)} m #{i}", flush=True)
    rows.sort(key=lambda r: (r["distance_m"], r["index"]))
    payload = {
        "config": {
            "stage": "mechanism_control",
            "control": "direct_path_only_no_additive_noise",
            "distances_m": list(DISTANCES),
            "geometries_per_distance": GEOMS,
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "include_multipath": False,
            "include_noise": False,
            "truth_usage": "truth is used for signal synthesis and final error computation only.",
            "manuscript_claim_allowed": "mechanism_boundary_control_only",
        },
        "summary": summarize(rows),
        "trials": rows,
    }
    (HERE / "no_noise_direct_control.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (HERE / "result_summary.md").write_text(markdown(payload), encoding="utf-8")
    print(json.dumps({"summary": payload["summary"]}, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run()

