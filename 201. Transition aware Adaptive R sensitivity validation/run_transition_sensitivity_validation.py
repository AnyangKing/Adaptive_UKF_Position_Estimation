"""Sensitivity validation for folder-191 transition-aware Adaptive-R.

This script reuses the folder-191 signal-level moving-target protocol and tests
whether the transition-aware soft-R result is fragile to the observed TOA
range-jump threshold and maximum TOA covariance inflation cap.
"""

from __future__ import annotations

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


VARIANTS = tuple(
    (float(th), float(cap))
    for th in (0.25, 0.50, 1.00)
    for cap in (25.0, 100.0, 400.0)
)
CANONICAL = (0.50, 100.0)
SENSITIVITY_DISTANCES = (0.0, 200.0, 400.0, 600.0, 800.0, 1000.0)
SENSITIVITY_GEOMS = 1
OUTPUT_JSON = HERE / "transition_sensitivity_validation.json"
OUTPUT_MD = HERE / "result_summary.md"


def variant_name(threshold_m: float, cap: float) -> str:
    return f"softR_thr{threshold_m:g}_cap{cap:g}"


def run_filter_variant(
    observations: np.ndarray,
    qualities: list[dict[str, Any]],
    truth: np.ndarray,
    carriers: np.ndarray,
    threshold_m: float,
    cap: float,
) -> dict[str, Any]:
    ukf, initial = m191.make_filter(observations[0])
    wrapper = m191.CarrierTransitionSoftRUKF(
        ukf,
        m191.ROUTING_THRESHOLD_DEG,
        range_jump_threshold_m=threshold_m,
        max_toa_scale=cap,
    )
    wrapper.prime(observations[0], carriers[0])

    estimates = np.zeros((m191.STEPS, 3))
    estimates[0] = initial
    exceptions = 0
    for k in range(1, m191.STEPS):
        try:
            wrapper.step(observations[k], qualities[k], carriers[k])
            estimates[k] = ukf.x[:3]
        except Exception:
            exceptions += 1
            estimates[k] = estimates[k - 1]

    errors = np.linalg.norm(estimates - truth, axis=1)
    history = getattr(wrapper, "history", [])
    transition_events = [h for h in history if h.get("transition_risk")]
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[m191.SETTLE_START:] ** 2))),
        "median_settled_error_m": float(np.median(errors[m191.SETTLE_START:])),
        "p90_settled_error_m": float(np.percentile(errors[m191.SETTLE_START:], 90.0)),
        "maximum_position_error_m": float(np.max(errors)),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": int(exceptions),
        "transition_risk_count": len(transition_events),
        "mean_transition_scale": (
            float(np.mean([h["transition_scale"] for h in transition_events]))
            if transition_events else 1.0
        ),
    }


def run_case(distance: float, cond_idx: int, cond: tuple[str, float, str, float], index: int) -> list[dict[str, Any]]:
    name, speed, mode, vz = cond
    pos, env, az, sign = m191.geometry(distance, cond_idx, index)
    truth = m191.truth_trajectory(pos, az, sign, speed, mode, vz)
    obs_hop, q_hop = m191.collect(truth, env, distance, cond_idx, index, m191.HOP_CARRIERS_HZ)

    rows: list[dict[str, Any]] = []
    for threshold_m, cap in VARIANTS:
        rows.append({
            "distance_m": float(distance),
            "condition": name,
            "index": int(index),
            "policy": variant_name(threshold_m, cap),
            "range_jump_threshold_m": float(threshold_m),
            "max_toa_scale": float(cap),
            **run_filter_variant(obs_hop, q_hop, truth, m191.HOP_CARRIERS_HZ, threshold_m, cap),
        })
    return rows


def load_191_baselines() -> tuple[dict[tuple[float, str, int], dict], dict[tuple[float, str, int], dict]]:
    payload = json.loads((F191 / "moving_full_range_independent_validation.json").read_text(encoding="utf-8"))
    fixed = {}
    hop = {}
    for row in payload["trials"]:
        key = (float(row["distance_m"]), row["condition"], int(row["index"]))
        if row["policy"] == "fixed_baseline":
            fixed[key] = row
        elif row["policy"] == "hop_baseline":
            hop[key] = row
    return fixed, hop


def bootstrap_ci(values: np.ndarray, seed: int = 201, n: int = 3000) -> list[float]:
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
        "p90_gain_m": float(np.percentile(gain, 90.0)),
        "p10_gain_m": float(np.percentile(gain, 10.0)),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fixed, hop = load_191_baselines()
    variants = sorted(set(r["policy"] for r in rows))
    candidate_by_variant = {
        variant: {
            (float(r["distance_m"]), r["condition"], int(r["index"])): r
            for r in rows if r["policy"] == variant
        }
        for variant in variants
    }
    keys = sorted(next(iter(candidate_by_variant.values())).keys())
    summary: dict[str, Any] = {
        "overall": {},
        "by_distance": {},
        "by_condition": {},
        "rankings": {},
    }
    for variant in variants:
        cand = candidate_by_variant[variant]
        subset = list(cand.values())
        summary["overall"][variant] = {
            "range_jump_threshold_m": subset[0]["range_jump_threshold_m"],
            "max_toa_scale": subset[0]["max_toa_scale"],
            "mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in subset])),
            "median_rmse_m": float(np.median([r["settled_rmse_m"] for r in subset])),
            "p90_rmse_m": float(np.percentile([r["settled_rmse_m"] for r in subset], 90.0)),
            "divergence_fraction": float(np.mean([r["diverged"] for r in subset])),
            "mean_transition_risk_count": float(np.mean([r["transition_risk_count"] for r in subset])),
            "mean_transition_scale": float(np.mean([r["mean_transition_scale"] for r in subset])),
            "vs_hop": compare(keys, hop, cand),
            "vs_fixed": compare(keys, fixed, cand),
        }

    for distance in SENSITIVITY_DISTANCES:
        dkeys = [k for k in keys if k[0] == float(distance)]
        summary["by_distance"][str(float(distance))] = {}
        for variant in variants:
            cand = candidate_by_variant[variant]
            summary["by_distance"][str(float(distance))][variant] = {
                "mean_rmse_m": float(np.mean([cand[k]["settled_rmse_m"] for k in dkeys])),
                "vs_hop": compare(dkeys, hop, cand),
                "vs_fixed": compare(dkeys, fixed, cand),
            }

    for condition, *_ in m191.CONDITIONS:
        ckeys = [k for k in keys if k[1] == condition]
        summary["by_condition"][condition] = {}
        for variant in variants:
            cand = candidate_by_variant[variant]
            summary["by_condition"][condition][variant] = {
                "mean_rmse_m": float(np.mean([cand[k]["settled_rmse_m"] for k in ckeys])),
                "vs_hop": compare(ckeys, hop, cand),
                "vs_fixed": compare(ckeys, fixed, cand),
            }

    summary["rankings"]["by_mean_gain_vs_hop"] = sorted(
        [
            {
                "policy": v,
                "mean_gain_vs_hop_m": summary["overall"][v]["vs_hop"]["mean_gain_m"],
                "tail_worsened_vs_hop": summary["overall"][v]["vs_hop"]["tail_worsened_fraction"],
                "mean_rmse_m": summary["overall"][v]["mean_rmse_m"],
            }
            for v in variants
        ],
        key=lambda x: x["mean_gain_vs_hop_m"],
        reverse=True,
    )
    return summary


def markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Transition-aware Adaptive-R sensitivity validation result",
        "",
        "## Protocol",
        "",
        f"- total paired subset cases per variant: {payload['config']['cases_per_variant']}",
        f"- variants: {len(payload['config']['variants'])}",
        "- baselines: fixed and plain-hop results are reused from folder 191 for the same subset keys.",
        "- truth usage: truth is used for signal synthesis and final error computation only.",
        "- claim boundary: first-pass subset sensitivity diagnostic, not a replacement for the 528-case validation.",
        "",
        "## Overall sensitivity grid",
        "",
        "| variant | threshold | cap | mean RMSE | gain vs hop | p vs hop | tail worse vs hop | gain vs fixed | p vs fixed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for variant, s in sorted(summary["overall"].items(), key=lambda kv: (kv[1]["range_jump_threshold_m"], kv[1]["max_toa_scale"])):
        lines.append(
            f"| {variant} | {s['range_jump_threshold_m']:.2f} | {s['max_toa_scale']:.0f} | "
            f"{s['mean_rmse_m']:.3f} | {s['vs_hop']['mean_gain_m']:.3f} | {s['vs_hop']['wilcoxon_p']:.3e} | "
            f"{s['vs_hop']['tail_worsened_fraction']:.3f} | {s['vs_fixed']['mean_gain_m']:.3f} | "
            f"{s['vs_fixed']['wilcoxon_p']:.3e} |"
        )
    lines.extend([
        "",
        "## Ranking by gain vs plain hop",
        "",
        "| rank | variant | gain vs hop | tail worse vs hop | mean RMSE |",
        "|---:|---|---:|---:|---:|",
    ])
    for i, row in enumerate(summary["rankings"]["by_mean_gain_vs_hop"], 1):
        lines.append(
            f"| {i} | {row['policy']} | {row['mean_gain_vs_hop_m']:.3f} | "
            f"{row['tail_worsened_vs_hop']:.3f} | {row['mean_rmse_m']:.3f} |"
        )
    lines.extend([
        "",
        "## Canonical setting",
        "",
        "The folder-191 canonical setting is `softR_thr0.5_cap100`. Interpret this folder as a sensitivity check, not as a new parameter search unless a different setting is explicitly revalidated on new seeds.",
        "",
    ])
    return "\n".join(lines)


def run(max_workers: int = 6) -> dict[str, Any]:
    cases = [
        (distance, ci, cond, i)
        for distance in SENSITIVITY_DISTANCES
        for ci, cond in enumerate(m191.CONDITIONS)
        for i in range(SENSITIVITY_GEOMS)
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        rows.extend(run_case(*case))

    payload = {
        "config": {
            "stage": "transition_aware_adaptive_r_sensitivity_validation",
            "source_protocol": str(F191.name),
            "distances_m": list(SENSITIVITY_DISTANCES),
            "conditions": [
                {"name": c[0], "speed_m_s": c[1], "mode": c[2], "vertical_speed_m_s": c[3]}
                for c in m191.CONDITIONS
            ],
            "geoms_per_distance_condition": SENSITIVITY_GEOMS,
            "cases_per_variant": len(cases),
            "steps": m191.STEPS,
            "settle_start": m191.SETTLE_START,
            "geometry_seed_root": m191.GEOM_ROOT,
            "ping_seed_root": m191.PING_ROOT,
            "variants": [
                {
                    "policy": variant_name(th, cap),
                    "range_jump_threshold_m": th,
                    "max_toa_scale": cap,
                    "is_folder_191_canonical": (th, cap) == CANONICAL,
                }
                for th, cap in VARIANTS
            ],
            "truth_usage": "truth is used for signal synthesis and final error computation only; runtime transition decisions use observed TOA range jump, carrier transition, disagreement, and NIS.",
            "claim_boundary": "first-pass subset parameter sensitivity diagnostic on the folder-191 seed set; not a replacement for the full 528-case validation, OOD motion, or real-water validation.",
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
