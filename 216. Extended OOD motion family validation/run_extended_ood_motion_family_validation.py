"""Extended OOD motion-family validation.

This is a compact extension of the 204 OOD study. It adds motion families that
were not in the original accelerating/curved/mixed/vertical-sine set.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
F191 = next(ROOT.glob("191. Moving full range transition aware independent validation"))
M191_PATH = F191 / "run_moving_full_range_independent_validation.py"

spec = importlib.util.spec_from_file_location("moving191", M191_PATH)
moving191 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(moving191)


DISTANCES = tuple(float(d) for d in range(0, 1001, 200))
GEOMS = 6
GEOM_ROOT = 2_160_000
PING_ROOT = 2_163_000

EXTENDED_OOD_CONDITIONS = (
    ("stop_go", "stop_go"),
    ("direction_reversal", "direction_reversal"),
    ("spiral_climb", "spiral_climb"),
    ("burst_turn", "burst_turn"),
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
    phase = rng.uniform(0.0, 2.0 * np.pi)
    return pos, env, az, sign, phase


def truth_trajectory(pos: np.ndarray, az: float, sign: float, phase: float, mode: str) -> np.ndarray:
    radial = np.array([np.cos(az), np.sin(az), 0.0])
    tangential = np.array([-np.sin(az), np.cos(az), 0.0])
    trajectory = []
    p = pos.astype(float).copy()
    for k in range(moving191.STEPS):
        if mode == "stop_go":
            if k < 5:
                v = 0.02 * sign * radial
            elif k < 13:
                v = sign * (0.15 + 0.10 * (k - 5)) * radial + 0.25 * tangential
            else:
                v = sign * 0.25 * radial + 0.15 * tangential
        elif mode == "direction_reversal":
            direction = 1.0 if k < moving191.STEPS // 2 else -1.0
            v = direction * 0.85 * tangential + sign * 0.18 * radial
        elif mode == "spiral_climb":
            theta = phase + 0.20 * k
            horizontal = np.cos(theta) * radial + np.sin(theta) * tangential
            v = 0.70 * horizontal + np.array([0.0, 0.0, sign * 0.06])
        elif mode == "burst_turn":
            if 8 <= k <= 12:
                theta = phase + 0.35 * (k - 8)
                direction = np.cos(theta) * tangential + sign * np.sin(theta) * radial
                v = 1.45 * direction + np.array([0.0, 0.0, 0.05 * sign])
            else:
                v = 0.45 * tangential + 0.10 * sign * radial
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
            moving191.ChannelConfig(),
            seed=PING_ROOT + int(distance) * 5000 + cond_idx * 4000 + index * 60 + k,
            carrier_hz=float(carriers[k]),
            **env,
        )
        _, received, _ = moving191.synthesize_received(pos, cfg)
        observation, quality = moving191.extract_measurement(received, cfg)
        observations.append(observation)
        qualities.append(quality)
    return np.asarray(observations), qualities


def run_case(distance: float, cond_idx: int, cond: tuple[str, str], index: int) -> list[dict[str, Any]]:
    name, mode = cond
    pos, env, az, sign, phase = geometry(distance, cond_idx, index)
    truth = truth_trajectory(pos, az, sign, phase, mode)
    fixed_carriers = np.full(moving191.STEPS, moving191.FIXED_CARRIER_HZ)
    obs_fixed, q_fixed = collect(truth, env, distance, cond_idx, index, fixed_carriers)
    obs_hop, q_hop = collect(truth, env, distance, cond_idx, index, moving191.HOP_CARRIERS_HZ)
    return [
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "fixed_baseline",
            **moving191.run_filter(obs_fixed, q_fixed, truth, fixed_carriers, "fixed_baseline"),
        },
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "hop_baseline",
            **moving191.run_filter(obs_hop, q_hop, truth, moving191.HOP_CARRIERS_HZ, "hop_baseline"),
        },
        {
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "hop_transition_softR",
            **moving191.run_filter(obs_hop, q_hop, truth, moving191.HOP_CARRIERS_HZ, "hop_transition_softR"),
        },
    ]


def compare(keys: list[tuple[float, str, int]], ref: dict, test: dict) -> dict[str, Any]:
    gains = np.array([ref[k]["settled_rmse_m"] - test[k]["settled_rmse_m"] for k in keys])
    try:
        p = float(moving191.wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
    except ValueError:
        p = 1.0
    return {
        "mean_gain_m": float(np.mean(gains)),
        "median_gain_m": float(np.median(gains)),
        "gain_ci95": moving191.bootstrap_ci(gains, seed=216),
        "wilcoxon_gain_gt0_p": p,
        "improved_fraction": float(np.mean(gains > 0.0)),
        "tail_worsened_fraction": float(np.mean(gains < -1.0)),
        "n": int(len(keys)),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    policies = ("fixed_baseline", "hop_baseline", "hop_transition_softR")
    fixed = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "fixed_baseline"}
    hop = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_baseline"}
    soft = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_transition_softR"}
    keys = sorted(soft)
    summary: dict[str, Any] = {"overall": {}, "comparisons": {}, "by_condition": {}, "by_distance": {}}
    for policy in policies:
        subset = [r for r in rows if r["policy"] == policy]
        summary["overall"][policy] = {
            "mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in subset])),
            "median_rmse_m": float(np.median([r["settled_rmse_m"] for r in subset])),
            "mean_p90_error_m": float(np.mean([r["p90_settled_error_m"] for r in subset])),
            "divergence_rate": float(np.mean([r["diverged"] for r in subset])),
            "n": int(len(subset)),
        }
    summary["comparisons"]["softR_vs_hop"] = compare(keys, hop, soft)
    summary["comparisons"]["softR_vs_fixed"] = compare(keys, fixed, soft)
    summary["comparisons"]["hop_vs_fixed"] = compare(keys, fixed, hop)
    for condition, _ in EXTENDED_OOD_CONDITIONS:
        ckeys = [k for k in keys if k[1] == condition]
        summary["by_condition"][condition] = {
            "fixed_mean_rmse_m": float(np.mean([fixed[k]["settled_rmse_m"] for k in ckeys])),
            "hop_mean_rmse_m": float(np.mean([hop[k]["settled_rmse_m"] for k in ckeys])),
            "softR_mean_rmse_m": float(np.mean([soft[k]["settled_rmse_m"] for k in ckeys])),
            "softR_vs_hop": compare(ckeys, hop, soft),
            "softR_vs_fixed": compare(ckeys, fixed, soft),
        }
    for distance in DISTANCES:
        dkeys = [k for k in keys if k[0] == distance]
        summary["by_distance"][str(distance)] = {
            "fixed_mean_rmse_m": float(np.mean([fixed[k]["settled_rmse_m"] for k in dkeys])),
            "hop_mean_rmse_m": float(np.mean([hop[k]["settled_rmse_m"] for k in dkeys])),
            "softR_mean_rmse_m": float(np.mean([soft[k]["settled_rmse_m"] for k in dkeys])),
            "softR_vs_hop": compare(dkeys, hop, soft),
            "softR_vs_fixed": compare(dkeys, fixed, soft),
        }
    return summary


def markdown(payload: dict[str, Any]) -> str:
    s = payload["summary"]
    lines = [
        "# Extended OOD motion-family validation result",
        "",
        "## Protocol",
        "",
        f"- paired cases: {payload['config']['total_paired_cases']}",
        f"- distances: {payload['config']['distances_m']}",
        f"- conditions: {[c['name'] for c in payload['config']['conditions']]}",
        "- policies: fixed, plain hop, transition-aware soft-R",
        "- claim boundary: additional OOD-family simulation, not arbitrary moving-target proof.",
        "",
        "## Overall",
        "",
        "| policy | mean RMSE | median RMSE | mean P90 | divergence | n |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for policy in ("fixed_baseline", "hop_baseline", "hop_transition_softR"):
        row = s["overall"][policy]
        lines.append(
            f"| {policy} | {row['mean_rmse_m']:.3f} | {row['median_rmse_m']:.3f} | "
            f"{row['mean_p90_error_m']:.3f} | {row['divergence_rate']:.3f} | {row['n']} |"
        )
    lines.extend([
        "",
        "## Paired comparisons",
        "",
        "| comparison | mean gain | p | improved frac | tail worsened | n |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for name, comp in s["comparisons"].items():
        lines.append(
            f"| {name} | {comp['mean_gain_m']:.3f} | {comp['wilcoxon_gain_gt0_p']:.4g} | "
            f"{comp['improved_fraction']:.3f} | {comp['tail_worsened_fraction']:.3f} | {comp['n']} |"
        )
    lines.extend([
        "",
        "## Condition breakdown",
        "",
        "| condition | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for condition, _ in EXTENDED_OOD_CONDITIONS:
        row = s["by_condition"][condition]
        lines.append(
            f"| {condition} | {row['fixed_mean_rmse_m']:.3f} | {row['hop_mean_rmse_m']:.3f} | "
            f"{row['softR_mean_rmse_m']:.3f} | {row['softR_vs_hop']['mean_gain_m']:.3f} | "
            f"{row['softR_vs_hop']['tail_worsened_fraction']:.3f} |"
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
        "## Interpretation boundary",
        "",
        "This extends the simulated OOD motion set, but it still does not prove arbitrary moving-target performance. It should be cited as additional OOD-family evidence only.",
    ])
    return "\n".join(lines) + "\n"


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [
        (distance, ci, cond, i)
        for distance in DISTANCES
        for ci, cond in enumerate(EXTENDED_OOD_CONDITIONS)
        for i in range(GEOMS)
    ]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for future in as_completed(futures):
            distance, _, cond, i = futures[future]
            rows.extend(future.result())
            print(f"completed extended OOD {int(distance)} m {cond[0]} #{i}", flush=True)
    rows.sort(key=lambda r: (r["distance_m"], r["condition"], r["index"], r["policy"]))
    payload = {
        "config": {
            "stage": "extended_ood_motion_family_validation",
            "distances_m": list(DISTANCES),
            "conditions": [{"name": c[0], "mode": c[1]} for c in EXTENDED_OOD_CONDITIONS],
            "geoms_per_distance_condition": GEOMS,
            "total_paired_cases": len(cases),
            "steps": moving191.STEPS,
            "settle_start": moving191.SETTLE_START,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "truth_usage": "truth is used for signal synthesis and final error computation only; filters use signal-extracted TOA/TDOA/DOA and runtime-observable quality metrics.",
            "claim_boundary": "additional simulated OOD motion-family validation; not arbitrary moving-target or real-water validation.",
        },
        "summary": summarize(rows),
        "trials": rows,
    }
    (HERE / "extended_ood_motion_family_validation.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (HERE / "result_summary.md").write_text(markdown(payload), encoding="utf-8")
    print(markdown(payload))
    return payload


if __name__ == "__main__":
    run()
