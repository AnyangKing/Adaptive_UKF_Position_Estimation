"""Independent static full-range validation over 0--1000 m.

This folder upgrades the low-n diagnostic sweep in folder 184 to n=20 per
distance while preserving the previously frozen observation/filter protocol.
No new algorithmic rule is introduced here.
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
F183 = next(ROOT.glob("183. *"))
sys.path.insert(0, str(F183))


import run_extended_transition_aware_validation as base  # noqa: E402


DISTANCES = tuple(float(v) for v in range(0, 1001, 100))
GEOMS_PER_DISTANCE = 20
STEPS = base.STEPS
SETTLE_START = base.SETTLE_START
FIXED_CARRIER_HZ = base.FIXED_CARRIER_HZ
HOP_CARRIERS_HZ = base.HOP_CARRIERS_HZ
GEOM_ROOT = 2_330_000
PING_ROOT = 2_333_000


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


def collect(
    position: np.ndarray,
    environment: dict[str, float],
    distance: float,
    index: int,
    carriers: np.ndarray,
) -> tuple[np.ndarray, list[dict[str, Any]], float]:
    observations: list[np.ndarray] = []
    qualities: list[dict[str, Any]] = []
    max_jump = 0.0
    previous: float | None = None
    for ping_index, carrier_hz in enumerate(carriers):
        cfg = replace(
            base.ChannelConfig(),
            seed=PING_ROOT + int(distance) * 1000 + index * 40 + ping_index,
            carrier_hz=float(carrier_hz),
            **environment,
        )
        _, received, _ = base.synthesize_received(position, cfg)
        observation, quality = base.extract_measurement(received, cfg)
        if previous is not None:
            max_jump = max(max_jump, abs(float(observation[0]) - previous))
        previous = float(observation[0])
        observations.append(observation)
        qualities.append(quality)
    return np.asarray(observations), qualities, float(max_jump)


def run_case(distance: float, index: int) -> dict[str, Any]:
    position, environment = geometry(distance, index)
    fixed_carriers = np.full(STEPS, FIXED_CARRIER_HZ)
    obs_fixed, q_fixed, fixed_max_jump = collect(position, environment, distance, index, fixed_carriers)
    obs_hop, q_hop, hop_max_jump = collect(position, environment, distance, index, HOP_CARRIERS_HZ)
    return {
        "distance_m": distance,
        "index": index,
        "position_m": [float(v) for v in position],
        "environment": environment,
        "fixed_max_adjacent_range_jump_m": fixed_max_jump,
        "hop_max_adjacent_range_jump_m": hop_max_jump,
        "fixed_baseline": base.run_filter(obs_fixed, q_fixed, position, fixed_carriers, "fixed_baseline"),
        "hop_baseline": base.run_filter(obs_hop, q_hop, position, HOP_CARRIERS_HZ, "hop_baseline"),
        "hop_transition_softR": base.run_filter(obs_hop, q_hop, position, HOP_CARRIERS_HZ, "hop_transition_softR"),
    }


def bootstrap_ci(values: np.ndarray, seed: int = 233, n: int = 5000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def compare(subset: list[dict[str, Any]], ref_policy: str, target_policy: str) -> dict[str, Any]:
    gains = np.array([r[ref_policy]["settled_rmse_m"] - r[target_policy]["settled_rmse_m"] for r in subset])
    try:
        p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
    except ValueError:
        p = 1.0
    return {
        "mean_gain_m": float(np.mean(gains)),
        "median_gain_m": float(np.median(gains)),
        "gain_ci95": bootstrap_ci(gains),
        "wilcoxon_gain_gt0_p": p,
        "improved_fraction": float(np.mean(gains > 0.0)),
        "tail_worsened_fraction": float(np.mean(gains < -1.0)),
        "n": int(len(gains)),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    policies = ("fixed_baseline", "hop_baseline", "hop_transition_softR")
    for distance in list(DISTANCES) + ["overall"]:
        subset = rows if distance == "overall" else [r for r in rows if r["distance_m"] == distance]
        entry: dict[str, Any] = {"policies": {}, "comparisons": {}}
        for policy in policies:
            rmse = np.array([r[policy]["settled_rmse_m"] for r in subset])
            entry["policies"][policy] = {
                "mean_rmse_m": float(np.mean(rmse)),
                "median_rmse_m": float(np.median(rmse)),
                "mean_p90_error_m": float(np.mean([r[policy]["p90_settled_error_m"] for r in subset])),
                "divergence_rate": float(np.mean([r[policy]["diverged"] for r in subset])),
                "total_transition_risks": int(sum(r[policy].get("transition_risk_count", 0) for r in subset)),
                "n": len(subset),
            }
        entry["comparisons"]["hop_vs_fixed"] = compare(subset, "fixed_baseline", "hop_baseline")
        entry["comparisons"]["softR_vs_hop"] = compare(subset, "hop_baseline", "hop_transition_softR")
        entry["comparisons"]["softR_vs_fixed"] = compare(subset, "fixed_baseline", "hop_transition_softR")
        summary[str(distance)] = entry
    return summary


def make_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Static full-range independent validation",
        "",
        "This is an independent n=20-per-distance validation of the frozen static full-range protocol.",
        "It upgrades folder 184 from a low-n diagnostic trend map to a denser validation set.",
        "",
        "## Overall paired comparisons",
        "",
        "| comparison | mean gain | median gain | 95% CI | p | improved frac | tail worsened | n |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    overall = payload["summary"]["overall"]
    for label in ("hop_vs_fixed", "softR_vs_hop", "softR_vs_fixed"):
        c = overall["comparisons"][label]
        lines.append(
            f"| {label} | {c['mean_gain_m']:.3f} | {c['median_gain_m']:.3f} | "
            f"[{c['gain_ci95'][0]:.3f}, {c['gain_ci95'][1]:.3f}] | "
            f"{c['wilcoxon_gain_gt0_p']:.4g} | {c['improved_fraction']:.3f} | "
            f"{c['tail_worsened_fraction']:.3f} | {c['n']} |"
        )
    lines.extend(
        [
            "",
            "## Distance breakdown",
            "",
            "| distance | fixed | hop | softR | hop gain vs fixed | softR gain vs fixed | hop tail worsened | softR tail worsened | n |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for d in DISTANCES:
        s = payload["summary"][str(d)]
        lines.append(
            "| {d:.0f} | {fx:.3f} | {hp:.3f} | {sr:.3f} | {hg:.3f} | {sg:.3f} | {ht:.3f} | {st:.3f} | {n} |".format(
                d=d,
                fx=s["policies"]["fixed_baseline"]["mean_rmse_m"],
                hp=s["policies"]["hop_baseline"]["mean_rmse_m"],
                sr=s["policies"]["hop_transition_softR"]["mean_rmse_m"],
                hg=s["comparisons"]["hop_vs_fixed"]["mean_gain_m"],
                sg=s["comparisons"]["softR_vs_fixed"]["mean_gain_m"],
                ht=s["comparisons"]["hop_vs_fixed"]["tail_worsened_fraction"],
                st=s["comparisons"]["softR_vs_fixed"]["tail_worsened_fraction"],
                n=s["policies"]["fixed_baseline"]["n"],
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "- This validation uses static simulated beacons under the existing shallow-water signal-level simulator.",
            "- It does not add real-water or hardware frequency-response evidence.",
            "- The 0 m case is a near-vertical degenerate geometry and should not be used as positive long-range evidence.",
            "- The main manuscript can use this result only as simulation-level full-range static support.",
        ]
    )
    return "\n".join(lines) + "\n"


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [(d, i) for d in DISTANCES for i in range(GEOMS_PER_DISTANCE)]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for future in as_completed(futures):
            d, i = futures[future]
            rows.append(future.result())
            print(f"completed static {int(d)} m #{i}", flush=True)
    rows.sort(key=lambda r: (r["distance_m"], r["index"]))
    summary = summarize(rows)
    payload = {
        "config": {
            "stage": "static_full_range_independent_validation",
            "distances_m": list(DISTANCES),
            "geometries_per_distance": GEOMS_PER_DISTANCE,
            "total_cases": len(rows),
            "policies": ["fixed_baseline", "hop_baseline", "hop_transition_softR"],
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "fixed_carrier_hz": FIXED_CARRIER_HZ,
            "hop_carriers_hz": [float(v) for v in HOP_CARRIERS_HZ],
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "truth_usage": "truth is used for signal synthesis and final error computation only.",
            "inherits_protocol_from": "183/184 frozen static full-range validation protocol",
        },
        "summary": summary,
        "trials": rows,
    }
    (HERE / "static_full_range_independent_validation.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (HERE / "result_summary.md").write_text(make_markdown(payload), encoding="utf-8")
    print(json.dumps({"overall": summary["overall"]}, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run()

