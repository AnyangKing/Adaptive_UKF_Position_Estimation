"""다양한 얕은 바다 조건에서 세 DOA 추정법의 강건성을 비교한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig, usb_array_global_m
from estimators import (
    estimate_array_doa,
    estimate_gcc_phat_doa,
    estimate_srp_phat_doa,
    estimate_toa_matched_filter,
)


def separation_deg(estimate: np.ndarray, truth: np.ndarray) -> float:
    return float(np.degrees(np.arccos(np.clip(estimate @ truth, -1.0, 1.0))))


def summarize(values: list[float]) -> dict[str, float]:
    array = np.asarray(values)
    return {
        "mean_deg": float(np.mean(array)),
        "median_deg": float(np.median(array)),
        "p90_deg": float(np.percentile(array, 90)),
        "max_deg": float(np.max(array)),
        "failure_over_10deg_rate": float(np.mean(array > 10.0)),
    }


def run(trials: int = 30) -> dict[str, object]:
    rng = np.random.default_rng(20260703)
    errors = {"matched_filter": [], "gcc_phat": [], "srp_phat": []}
    scenarios = []
    for trial in range(trials):
        distance = float(rng.choice([100.0, 300.0, 600.0]))
        azimuth = rng.uniform(-np.pi, np.pi)
        source_depth = rng.uniform(8.0, 85.0)
        source = np.array([
            distance * np.cos(azimuth), distance * np.sin(azimuth), -source_depth
        ])
        cfg = replace(
            ChannelConfig(),
            seed=20260703 + trial,
            snr_db=float(rng.choice([10.0, 20.0, 30.0])),
            surface_reflection=float(-rng.uniform(0.70, 0.98)),
            bottom_reflection=float(rng.uniform(0.30, 0.80)),
            radial_velocity_m_s=float(rng.uniform(-1.5, 1.5)),
        )
        _, received, _ = synthesize_received(source, cfg)
        toas, _ = estimate_toa_matched_filter(received, cfg)
        _, _, matched = estimate_array_doa(toas, cfg)
        _, _, gcc, _ = estimate_gcc_phat_doa(received, cfg)
        _, _, srp, _ = estimate_srp_phat_doa(received, cfg)
        truth = source - usb_array_global_m(cfg.receiver_depth_m).mean(axis=0)
        truth /= np.linalg.norm(truth)
        errors["matched_filter"].append(separation_deg(matched, truth))
        errors["gcc_phat"].append(separation_deg(gcc, truth))
        errors["srp_phat"].append(separation_deg(srp, truth))
        scenarios.append({"distance_m": distance, "source_depth_m": source_depth, "snr_db": cfg.snr_db})

    result = {
        "trials": trials,
        "seed": 20260703,
        "summary": {method: summarize(values) for method, values in errors.items()},
    }
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    (output / "doa_monte_carlo.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    np.savez(output / "doa_monte_carlo.npz", **{k: np.asarray(v) for k, v in errors.items()})
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run()
