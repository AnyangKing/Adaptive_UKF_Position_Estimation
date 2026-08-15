"""First-pass OOD motion validation for transition-aware Adaptive-R."""

from __future__ import annotations

from dataclasses import replace
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
F191 = next(ROOT.glob("191. Moving full range transition aware independent validation"))
M191_PATH = F191 / "run_moving_full_range_independent_validation.py"

spec = importlib.util.spec_from_file_location("m191", M191_PATH)
m191 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(m191)


DISTANCES = (400.0, 800.0, 1000.0)
GEOMS = 1
GEOM_ROOT = 2_020_000
PING_ROOT = 2_023_000
OUTPUT_JSON = HERE / "ood_motion_validation.json"
OUTPUT_MD = HERE / "result_summary.md"


OOD_CONDITIONS = (
    ("accelerating_radial", "accelerating_radial"),
    ("curved_arc", "curved_arc"),
    ("mixed_radial_tangential", "mixed_radial_tangential"),
    ("vertical_sine", "vertical_sine"),
)


def geometry(distance: float, cond_idx: int, index: int):
    rng = np.random.default_rng(GEOM_ROOT + int(distance) * 100 + cond_idx * 1000 + index)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(18.0, 72.0)
    pos = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
    env = {
        "snr_db": float(rng.choice([10.0, 20.0, 30.0])),
        "surface_reflection": float(-rng.uniform(0.72, 0.97)),
        "bottom_reflection": float(rng.uniform(0.32, 0.78)),
        "radial_velocity_m_s": 0.0,
    }
    sign = 1.0 if rng.uniform() < 0.5 else -1.0
    return pos, env, az, sign


def truth_trajectory(pos: np.ndarray, az: float, sign: float, mode: str) -> np.ndarray:
    radial = np.array([np.cos(az), np.sin(az), 0.0])
    tangential = np.array([-np.sin(az), np.cos(az), 0.0])
    trajectory = []
    p = pos.astype(float).copy()
    for k in range(m191.STEPS):
        if mode == "accelerating_radial":
            v = sign * (0.10 + 0.055 * k) * radial
        elif mode == "curved_arc":
            theta = 0.055 * k
            direction = np.cos(theta) * tangential + sign * np.sin(theta) * radial
            v = 0.75 * direction
        elif mode == "mixed_radial_tangential":
            v = sign * 0.45 * radial + 0.75 * tangential
            if k >= m191.STEPS // 2:
                v = -0.25 * sign * radial + 0.95 * tangential
        elif mode == "vertical_sine":
            vz = 0.22 * np.sin(2.0 * np.pi * k / max(m191.STEPS - 1, 1))
            v = 0.65 * tangential + np.array([0.0, 0.0, vz])
        else:
            raise ValueError(mode)
        trajectory.append(p.copy())
        p = p + v
    return np.asarray(trajectory)


def collect(truth: np.ndarray, env: dict[str, float], distance: float, cond_idx: int, index: int, carriers: np.ndarray):
    observations: list[np.ndarray] = []
    qualities: list[dict] = []
    for k, pos in enumerate(truth):
        cfg = replace(
            m191.ChannelConfig(),
            seed=PING_ROOT + int(distance) * 5000 + cond_idx * 4000 + index * 60 + k,
            carrier_hz=float(carriers[k]),
            **env,
        )
        _, received, _ = m191.synthesize_received(pos, cfg)
        observation, quality = m191.extract_measurement(received, cfg)
        observations.append(observation)
        qualities.append(quality)
    return np.asarray(observations), qualities


def run_case(distance: float, cond_idx: int, cond: tuple[str, str], index: int) -> list[dict[str, Any]]:
    name, mode = cond
    pos, env, az, sign = geometry(distance, cond_idx, index)
    truth = truth_trajectory(pos, az, sign, mode)
    fixed_carriers = np.full(m191.STEPS, m191.FIXED_CARRIER_HZ)
    obs_fixed, q_fixed = collect(truth, env, distance, cond_idx, index, fixed_carriers)
    obs_hop, q_hop = collect(truth, env, distance, cond_idx, index, m191.HOP_CARRIERS_HZ)
    return [
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "fixed_baseline",
            **m191.run_filter(obs_fixed, q_fixed, truth, fixed_carriers, "fixed_baseline"),
        },
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "hop_baseline",
            **m191.run_filter(obs_hop, q_hop, truth, m191.HOP_CARRIERS_HZ, "hop_baseline"),
        },
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "hop_transition_softR",
            **m191.run_filter(obs_hop, q_hop, truth, m191.HOP_CARRIERS_HZ, "hop_transition_softR"),
        },
    ]


def bootstrap_ci(values: np.ndarray, seed: int = 202, n: int = 3000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def compare(keys: list[tuple[float, str, int]], baseline: dict, candidate: dict) -> dict[str, Any]:
    base = np.asarray([baseline[k]["settled_rmse_m"] for k in keys], dtype=float)
    cand = np.asarray([candidate[k]["settled_rmse_m"] for k in keys], dtype=float)
    gain = base - cand
    try:
        _, p = wilcoxon(base, cand, zero_method="wilcox")
    except ValueError:
        p = 1.0
    return {
        "n": int(len(keys)),
        "baseline_mean_rmse_m": float(np.mean(base)),
        "candidate_mean_rmse_m": float(np.mean(cand)),
        "mean_gain_m": float(np.mean(gain)),
        "median_gain_m": float(np.median(gain)),
        "gain_ci95_m": bootstrap_ci(gain),
        "wilcoxon_p": float(p),
        "improved_fraction": float(np.mean(gain > 0.0)),
        "tail_worsened_fraction": float(np.mean(gain < -1.0)),
        "p10_gain_m": float(np.percentile(gain, 10.0)),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fixed = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "fixed_baseline"}
    hop = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_baseline"}
    soft = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_transition_softR"}
    keys = sorted(soft)
    summary: dict[str, Any] = {"overall": {}, "by_distance": {}, "by_condition": {}, "comparisons": {}}
    for policy in ("fixed_baseline", "hop_baseline", "hop_transition_softR"):
        subset = [r for r in rows if r["policy"] == policy]
        summary["overall"][policy] = {
            "mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in subset])),
            "median_rmse_m": float(np.median([r["settled_rmse_m"] for r in subset])),
            "p90_rmse_m": float(np.percentile([r["settled_rmse_m"] for r in subset], 90.0)),
            "divergence_fraction": float(np.mean([r["diverged"] for r in subset])),
        }
    summary["comparisons"]["softR_vs_hop"] = compare(keys, hop, soft)
    summary["comparisons"]["softR_vs_fixed"] = compare(keys, fixed, soft)
    summary["comparisons"]["hop_vs_fixed"] = compare(keys, fixed, hop)

    for distance in DISTANCES:
        dkeys = [k for k in keys if k[0] == distance]
        summary["by_distance"][str(distance)] = {
            "fixed_mean_rmse_m": float(np.mean([fixed[k]["settled_rmse_m"] for k in dkeys])),
            "hop_mean_rmse_m": float(np.mean([hop[k]["settled_rmse_m"] for k in dkeys])),
            "softR_mean_rmse_m": float(np.mean([soft[k]["settled_rmse_m"] for k in dkeys])),
            "softR_vs_hop": compare(dkeys, hop, soft),
            "softR_vs_fixed": compare(dkeys, fixed, soft),
        }
    for condition, _ in OOD_CONDITIONS:
        ckeys = [k for k in keys if k[1] == condition]
        summary["by_condition"][condition] = {
            "fixed_mean_rmse_m": float(np.mean([fixed[k]["settled_rmse_m"] for k in ckeys])),
            "hop_mean_rmse_m": float(np.mean([hop[k]["settled_rmse_m"] for k in ckeys])),
            "softR_mean_rmse_m": float(np.mean([soft[k]["settled_rmse_m"] for k in ckeys])),
            "softR_vs_hop": compare(ckeys, hop, soft),
            "softR_vs_fixed": compare(ckeys, fixed, soft),
        }
    return summary


def markdown(payload: dict[str, Any]) -> str:
    s = payload["summary"]
    lines = [
        "# OOD motion transition-aware validation result",
        "",
        "## Protocol",
        "",
        f"- paired OOD cases: {payload['config']['total_paired_cases']}",
        f"- distances: {payload['config']['distances_m']}",
        f"- conditions: {[c['name'] for c in payload['config']['conditions']]}",
        "- policies: fixed, plain hop, transition-aware soft-R",
        "- claim boundary: first-pass OOD probe, not full robustness proof.",
        "",
        "## Overall",
        "",
        "| policy | mean RMSE | median RMSE | P90 RMSE | divergence |",
        "|---|---:|---:|---:|---:|",
    ]
    for policy in ("fixed_baseline", "hop_baseline", "hop_transition_softR"):
        row = s["overall"][policy]
        lines.append(
            f"| {policy} | {row['mean_rmse_m']:.3f} | {row['median_rmse_m']:.3f} | "
            f"{row['p90_rmse_m']:.3f} | {row['divergence_fraction']:.3f} |"
        )
    lines.extend([
        "",
        "## Comparisons",
        "",
        "| comparison | mean gain | median gain | improved fraction | tail worsened | p |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for name in ("softR_vs_hop", "softR_vs_fixed", "hop_vs_fixed"):
        c = s["comparisons"][name]
        lines.append(
            f"| {name} | {c['mean_gain_m']:.3f} | {c['median_gain_m']:.3f} | "
            f"{c['improved_fraction']:.3f} | {c['tail_worsened_fraction']:.3f} | {c['wilcoxon_p']:.3e} |"
        )
    lines.extend([
        "",
        "## Distance breakdown",
        "",
        "| distance | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |",
        "|---:|---:|---:|---:|---:|---:|",
    ])
    for distance in DISTANCES:
        row = s["by_distance"][str(distance)]
        lines.append(
            f"| {int(distance)} | {row['fixed_mean_rmse_m']:.3f} | {row['hop_mean_rmse_m']:.3f} | "
            f"{row['softR_mean_rmse_m']:.3f} | {row['softR_vs_hop']['mean_gain_m']:.3f} | "
            f"{row['softR_vs_hop']['tail_worsened_fraction']:.3f} |"
        )
    lines.extend([
        "",
        "## Condition breakdown",
        "",
        "| condition | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for condition, _ in OOD_CONDITIONS:
        row = s["by_condition"][condition]
        lines.append(
            f"| {condition} | {row['fixed_mean_rmse_m']:.3f} | {row['hop_mean_rmse_m']:.3f} | "
            f"{row['softR_mean_rmse_m']:.3f} | {row['softR_vs_hop']['mean_gain_m']:.3f} | "
            f"{row['softR_vs_hop']['tail_worsened_fraction']:.3f} |"
        )
    return "\n".join(lines)


def run() -> dict[str, Any]:
    cases = [
        (distance, ci, cond, i)
        for distance in DISTANCES
        for ci, cond in enumerate(OOD_CONDITIONS)
        for i in range(GEOMS)
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        rows.extend(run_case(*case))
    payload = {
        "config": {
            "stage": "ood_motion_transition_aware_validation",
            "distances_m": list(DISTANCES),
            "conditions": [{"name": c[0], "mode": c[1]} for c in OOD_CONDITIONS],
            "geoms_per_distance_condition": GEOMS,
            "total_paired_cases": len(cases),
            "steps": m191.STEPS,
            "settle_start": m191.SETTLE_START,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "transition_rule": {
                "range_jump_threshold_m": m191.RANGE_JUMP_THRESHOLD_M,
                "max_toa_scale": m191.MAX_TOA_SCALE,
            },
            "truth_usage": "truth is used for signal synthesis and final error computation only; filters use signal-extracted TOA/TDOA/DOA and runtime-observable quality metrics.",
            "claim_boundary": "first-pass OOD motion probe; not full robustness or real-water validation.",
        },
        "summary": summarize(rows),
        "trials": rows,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    OUTPUT_MD.write_text(markdown(payload), encoding="utf-8")
    print(markdown(payload))
    return payload


if __name__ == "__main__":
    run()
