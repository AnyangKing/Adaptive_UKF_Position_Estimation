"""Runtime split audit for the adopted signal-based Adaptive UKF pipeline.

This script intentionally reuses the code from folder 61 without changing the
adopted algorithm. It measures wall-clock time for:

1. received-signal synthesis (simulation-only cost),
2. physically obtainable observation extraction, and
3. causal Adaptive UKF predict/update.

The output is an audit artifact, not a new performance claim.
"""

from __future__ import annotations

from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import platform
import statistics
import sys
import time
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
F61 = next(ROOT.glob("61. *"))
sys.path.insert(0, str(F61))


from channel import synthesize_received  # noqa: E402
from conditional_adaptive import ConditionalAdaptiveRUKF  # noqa: E402
from config import ChannelConfig  # noqa: E402
from measurement import fixed_measurement_covariance, initialize_position  # noqa: E402
from peak_measurement import extract_measurement  # noqa: E402
from ukf import SignalObservationUKF, acceleration_process_covariance  # noqa: E402


SCENARIOS = [
    {"distance_m": 100.0, "azimuth_deg": -35.0, "depth_m": 20.0, "snr_db": 20.0},
    {"distance_m": 200.0, "azimuth_deg": 40.0, "depth_m": 35.0, "snr_db": 20.0},
    {"distance_m": 400.0, "azimuth_deg": 115.0, "depth_m": 55.0, "snr_db": 20.0},
    {"distance_m": 600.0, "azimuth_deg": -150.0, "depth_m": 70.0, "snr_db": 20.0},
]
PINGS_PER_SCENARIO = 5
ROUTING_THRESHOLD_DEG = 5.0
SEED_ROOT = 1770000


def _load_git_head() -> str | None:
    head = ROOT / ".git" / "HEAD"
    try:
        content = head.read_text(encoding="utf-8").strip()
        if content.startswith("ref:"):
            ref = content.split(" ", 1)[1]
            ref_path = ROOT / ".git" / ref
            return ref_path.read_text(encoding="utf-8").strip()[:12]
        return content[:12]
    except OSError:
        return None


def _position(distance_m: float, azimuth_deg: float, depth_m: float) -> np.ndarray:
    az = np.radians(azimuth_deg)
    return np.array([distance_m * np.cos(az), distance_m * np.sin(az), -depth_m], dtype=float)


def _elapsed_ms(fn):
    start = time.perf_counter()
    value = fn()
    return value, (time.perf_counter() - start) * 1000.0


def _stats(values: list[float]) -> dict[str, float]:
    values = [float(v) for v in values]
    return {
        "n": len(values),
        "mean_ms": float(statistics.fmean(values)),
        "median_ms": float(statistics.median(values)),
        "min_ms": float(min(values)),
        "max_ms": float(max(values)),
        "p90_ms": float(np.percentile(values, 90.0)),
    }


def run() -> dict[str, Any]:
    synthesis_ms: list[float] = []
    extraction_ms: list[float] = []
    update_ms: list[float] = []
    online_ms: list[float] = []
    rows: list[dict[str, Any]] = []

    for scenario_index, scenario in enumerate(SCENARIOS):
        pos = _position(
            scenario["distance_m"],
            scenario["azimuth_deg"],
            scenario["depth_m"],
        )
        cfg0 = replace(
            ChannelConfig(),
            seed=SEED_ROOT + scenario_index * 100,
            snr_db=float(scenario["snr_db"]),
            radial_velocity_m_s=0.0,
        )

        init_obs = None
        init_quality = None
        wrapper = None

        for ping in range(PINGS_PER_SCENARIO):
            cfg = replace(cfg0, seed=SEED_ROOT + scenario_index * 100 + ping)
            (_, received, _), synth_ms = _elapsed_ms(lambda: synthesize_received(pos, cfg))
            (observation, quality), meas_ms = _elapsed_ms(lambda: extract_measurement(received, cfg))

            if ping == 0:
                init = initialize_position(observation, cfg)
                ukf = SignalObservationUKF(
                    np.r_[init, np.zeros(3)],
                    np.diag([8.0**2] * 3 + [1.5**2] * 3),
                    acceleration_process_covariance(1.0, 0.20),
                    fixed_measurement_covariance(),
                    cfg,
                )
                wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
                init_obs = observation
                init_quality = quality
                ukf_ms = 0.0
                online_step_ms = meas_ms
                initialized = True
            else:
                assert wrapper is not None
                _, ukf_ms = _elapsed_ms(lambda: wrapper.step(observation, quality))
                online_step_ms = meas_ms + ukf_ms
                initialized = False

            synthesis_ms.append(synth_ms)
            extraction_ms.append(meas_ms)
            if not initialized:
                update_ms.append(ukf_ms)
            online_ms.append(online_step_ms)
            rows.append({
                "scenario_index": scenario_index,
                "ping": ping,
                "distance_m": scenario["distance_m"],
                "initialized_from_first_ping": initialized,
                "signal_synthesis_ms": float(synth_ms),
                "measurement_extraction_ms": float(meas_ms),
                "ukf_update_ms": float(ukf_ms),
                "online_excluding_synthesis_ms": float(online_step_ms),
                "quality_keys": sorted(quality.keys()),
            })

        assert init_obs is not None and init_quality is not None

    payload = {
        "audit_type": "runtime_split_only_no_algorithm_change",
        "source_pipeline_folder": F61.name,
        "git_head": _load_git_head(),
        "platform": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
        "scenario": {
            "scenarios": SCENARIOS,
            "pings_per_scenario": PINGS_PER_SCENARIO,
            "seed_root": SEED_ROOT,
            "routing_threshold_deg": ROUTING_THRESHOLD_DEG,
            "canonical_channel": {
                "sample_rate_hz": ChannelConfig.sample_rate_hz,
                "carrier_hz": ChannelConfig.carrier_hz,
                "chirp_bandwidth_hz": ChannelConfig.chirp_bandwidth_hz,
                "pulse_duration_s": ChannelConfig.pulse_duration_s,
                "guard_time_s": ChannelConfig.guard_time_s,
            },
        },
        "summary": {
            "signal_synthesis_ms": _stats(synthesis_ms),
            "measurement_extraction_ms": _stats(extraction_ms),
            "ukf_update_ms_excluding_initialization": _stats(update_ms),
            "online_excluding_signal_synthesis_ms": _stats(online_ms),
        },
        "rows": rows,
        "claim_boundary": [
            "The measurement extraction and UKF update use current-ping observations and past filter state only.",
            "Signal synthesis is simulation-only and is reported separately from online runtime.",
            "This audit does not update RMSE, thresholds, or adopted claims.",
        ],
    }

    out = Path(__file__).resolve().parent / "runtime_split_summary.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"summary": payload["summary"], "output": out.name}, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run()
