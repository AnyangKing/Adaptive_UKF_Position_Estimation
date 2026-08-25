"""Axis-wise error decomposition for the moving full-range protocol.

This reuses the frozen folder-238 step logic and adds state-space error
decomposition: x/y/z, horizontal/vertical, and radial/cross-range components.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
F238 = ROOT / "238. softR filter consistency validation"


def _load_f238():
    path = F238 / "run_softR_consistency_validation.py"
    spec = importlib.util.spec_from_file_location("softR_consistency_238", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


m238 = _load_f238()
m191 = m238.m191

DISTANCES = m238.DISTANCES
CONDITIONS = m238.CONDITIONS
GEOMS = m238.GEOMS
STEPS = m238.STEPS
SETTLE_START = m238.SETTLE_START
POLICIES = m238.POLICIES


def axis_components(error_xyz: np.ndarray, truth_xyz: np.ndarray) -> dict[str, float]:
    ex, ey, ez = [float(v) for v in error_xyz]
    horizontal_error_m = float(np.hypot(ex, ey))
    vertical_error_m = float(abs(ez))

    xy = np.asarray(truth_xyz[:2], dtype=float)
    norm_xy = float(np.linalg.norm(xy))
    if norm_xy < 1.0e-9:
        radial_error_m = float("nan")
        cross_range_error_m = float("nan")
    else:
        radial_unit = xy / norm_xy
        cross_unit = np.array([-radial_unit[1], radial_unit[0]])
        e_xy = np.array([ex, ey])
        radial_error_m = float(e_xy @ radial_unit)
        cross_range_error_m = float(e_xy @ cross_unit)

    return {
        "x_error_m": ex,
        "y_error_m": ey,
        "z_error_m": ez,
        "horizontal_error_m": horizontal_error_m,
        "vertical_error_m": vertical_error_m,
        "radial_error_m": radial_error_m,
        "cross_range_error_m": cross_range_error_m,
    }


def rmse(values: list[float]) -> float | None:
    finite = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if finite.size == 0:
        return None
    return float(np.sqrt(np.mean(finite**2)))


def mean(values: list[float]) -> float | None:
    finite = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if finite.size == 0:
        return None
    return float(np.mean(finite))


def percentile(values: list[float], q: float) -> float | None:
    finite = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if finite.size == 0:
        return None
    return float(np.percentile(finite, q))


def summarize_axis(step_axes: list[dict[str, float]]) -> dict[str, Any]:
    keys = (
        "x_error_m",
        "y_error_m",
        "z_error_m",
        "horizontal_error_m",
        "vertical_error_m",
        "radial_error_m",
        "cross_range_error_m",
    )
    out: dict[str, Any] = {}
    for key in keys:
        values = [row[key] for row in step_axes]
        base = key.removesuffix("_error_m")
        out[f"{base}_rmse_m"] = rmse(values)
        out[f"{base}_mean_signed_m"] = mean(values)
        out[f"{base}_p90_abs_m"] = percentile([abs(v) for v in values], 90.0)
    return out


def run_filter_with_axes(observations, qualities, truth, carriers, policy: str) -> dict[str, Any]:
    ukf, initial = m191.make_filter(observations[0])
    estimates = np.zeros((STEPS, 3))
    estimates[0] = initial
    step_axes: list[dict[str, Any]] = []
    exceptions = 0
    previous_range_m = float(observations[0][0])
    previous_carrier_hz = float(carriers[0])

    for k in range(1, STEPS):
        try:
            _, previous_range_m, previous_carrier_hz = m238.apply_policy_step(
                ukf,
                observations[k],
                qualities[k],
                policy,
                float(carriers[k]),
                previous_range_m,
                previous_carrier_hz,
            )
            estimates[k] = ukf.x[:3]
        except Exception as exc:
            exceptions += 1
            estimates[k] = estimates[k - 1]
            step_axes.append({
                "step": k,
                "exception": type(exc).__name__,
                "message": str(exc),
                **{key: float("nan") for key in (
                    "x_error_m",
                    "y_error_m",
                    "z_error_m",
                    "horizontal_error_m",
                    "vertical_error_m",
                    "radial_error_m",
                    "cross_range_error_m",
                )},
            })
            continue

        error_xyz = estimates[k] - truth[k]
        step_axes.append({"step": k, **axis_components(error_xyz, truth[k])})

    errors = np.linalg.norm(estimates - truth, axis=1)
    settled_axes = [row for row in step_axes if row["step"] >= SETTLE_START]
    axis_summary = summarize_axis(settled_axes)
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[SETTLE_START:] ** 2))),
        "median_settled_error_m": float(np.median(errors[SETTLE_START:])),
        "p90_settled_error_m": float(np.percentile(errors[SETTLE_START:], 90.0)),
        "maximum_position_error_m": float(np.max(errors)),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": int(exceptions),
        **axis_summary,
        "step_axis_errors": step_axes,
    }


def run_case(distance: float, cond_idx: int, cond: tuple[str, float, str, float], index: int) -> list[dict[str, Any]]:
    name, speed, mode, vz = cond
    pos, env, az, sign = m191.geometry(distance, cond_idx, index)
    truth = m191.truth_trajectory(pos, az, sign, speed, mode, vz)
    fixed_carriers = np.full(STEPS, m191.FIXED_CARRIER_HZ)
    obs_fixed, q_fixed = m191.collect(truth, env, distance, cond_idx, index, fixed_carriers)
    obs_hop, q_hop = m191.collect(truth, env, distance, cond_idx, index, m191.HOP_CARRIERS_HZ)
    common = {"distance_m": distance, "condition": name, "index": index}
    return [
        {
            **common,
            "policy": "fixed_baseline",
            **run_filter_with_axes(obs_fixed, q_fixed, truth, fixed_carriers, "fixed_baseline"),
        },
        {
            **common,
            "policy": "hop_baseline",
            **run_filter_with_axes(obs_hop, q_hop, truth, m191.HOP_CARRIERS_HZ, "hop_baseline"),
        },
        {
            **common,
            "policy": "hop_transition_softR",
            **run_filter_with_axes(obs_hop, q_hop, truth, m191.HOP_CARRIERS_HZ, "hop_transition_softR"),
        },
    ]


def bootstrap_ci(values: np.ndarray, seed: int = 239, n: int = 3000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def compare(keys: list[tuple[float, str, int]], ref: dict, test: dict, metric: str) -> dict[str, Any]:
    gains = np.array([
        ref[k][metric] - test[k][metric]
        for k in keys
        if ref[k].get(metric) is not None
        and test[k].get(metric) is not None
        and np.isfinite(ref[k][metric])
        and np.isfinite(test[k][metric])
    ], dtype=float)
    gains = gains[np.isfinite(gains)]
    if gains.size == 0:
        return {
            "metric": metric,
            "mean_gain_m": None,
            "median_gain_m": None,
            "gain_ci95": [None, None],
            "wilcoxon_gain_gt0_p": None,
            "improved_fraction": None,
            "n": 0,
        }
    try:
        p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
    except ValueError:
        p = 1.0
    return {
        "metric": metric,
        "mean_gain_m": float(np.mean(gains)),
        "median_gain_m": float(np.median(gains)),
        "gain_ci95": bootstrap_ci(gains),
        "wilcoxon_gain_gt0_p": p,
        "improved_fraction": float(np.mean(gains > 0)),
        "n": int(gains.size),
    }


def aggregate(subset: list[dict[str, Any]], metric: str) -> float | None:
    values = [row[metric] for row in subset if row.get(metric) is not None and np.isfinite(row[metric])]
    if not values:
        return None
    return float(np.mean(values))


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"overall": {}, "by_distance": {}, "comparisons": {}}
    axis_metrics = (
        "settled_rmse_m",
        "horizontal_rmse_m",
        "vertical_rmse_m",
        "radial_rmse_m",
        "cross_range_rmse_m",
        "z_rmse_m",
    )
    for policy in POLICIES:
        subset = [row for row in rows if row["policy"] == policy]
        summary["overall"][policy] = {
            metric: aggregate(subset, metric)
            for metric in axis_metrics
        }
        summary["overall"][policy]["divergence_rate"] = float(np.mean([row["diverged"] for row in subset]))
        summary["overall"][policy]["n"] = len(subset)

    maps = {
        policy: {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == policy}
        for policy in POLICIES
    }
    keys = sorted(maps["hop_transition_softR"])
    for metric in axis_metrics:
        summary["comparisons"][f"softR_vs_hop_{metric}"] = compare(keys, maps["hop_baseline"], maps["hop_transition_softR"], metric)
        summary["comparisons"][f"softR_vs_fixed_{metric}"] = compare(keys, maps["fixed_baseline"], maps["hop_transition_softR"], metric)

    for distance in DISTANCES:
        dkeys = [key for key in keys if key[0] == distance]
        drows = [row for row in rows if row["distance_m"] == distance]
        summary["by_distance"][str(distance)] = {
            "n": len(dkeys),
            "softR_vs_hop_settled_rmse_m": compare(dkeys, maps["hop_baseline"], maps["hop_transition_softR"], "settled_rmse_m"),
            "softR_vs_hop_horizontal_rmse_m": compare(dkeys, maps["hop_baseline"], maps["hop_transition_softR"], "horizontal_rmse_m"),
            "softR_vs_hop_vertical_rmse_m": compare(dkeys, maps["hop_baseline"], maps["hop_transition_softR"], "vertical_rmse_m"),
            "softR_horizontal_rmse_m": aggregate([r for r in drows if r["policy"] == "hop_transition_softR"], "horizontal_rmse_m"),
            "softR_vertical_rmse_m": aggregate([r for r in drows if r["policy"] == "hop_transition_softR"], "vertical_rmse_m"),
        }
    return summary


def fmt(value: float | None, digits: int = 3) -> str:
    return "NA" if value is None else f"{value:.{digits}f}"


def markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Axis-wise error decomposition validation",
        "",
        "## Overall policy metrics",
        "",
        "| policy | 3D RMSE | horizontal RMSE | vertical RMSE | radial RMSE | cross-range RMSE | div. | n |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for policy, row in summary["overall"].items():
        lines.append(
            f"| {policy} | {fmt(row['settled_rmse_m'])} | {fmt(row['horizontal_rmse_m'])} | "
            f"{fmt(row['vertical_rmse_m'])} | {fmt(row['radial_rmse_m'])} | "
            f"{fmt(row['cross_range_rmse_m'])} | {row['divergence_rate']:.3f} | {row['n']} |"
        )

    lines.extend([
        "",
        "## softR gains against hop baseline",
        "",
        "| metric | mean gain | 95% CI | Wilcoxon p | improved frac | n |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for metric in (
        "settled_rmse_m",
        "horizontal_rmse_m",
        "vertical_rmse_m",
        "radial_rmse_m",
        "cross_range_rmse_m",
    ):
        comp = summary["comparisons"][f"softR_vs_hop_{metric}"]
        ci = comp["gain_ci95"]
        lines.append(
            f"| {metric} | {fmt(comp['mean_gain_m'])} | [{fmt(ci[0])}, {fmt(ci[1])}] | "
            f"{fmt(comp['wilcoxon_gain_gt0_p'], 4)} | {fmt(comp['improved_fraction'])} | {comp['n']} |"
        )

    lines.extend([
        "",
        "## Distance-wise softR decomposition",
        "",
        "| distance m | 3D gain vs hop | horizontal gain vs hop | vertical gain vs hop | softR horizontal RMSE | softR vertical RMSE | n |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for distance in DISTANCES:
        row = summary["by_distance"][str(distance)]
        lines.append(
            f"| {int(distance)} | {fmt(row['softR_vs_hop_settled_rmse_m']['mean_gain_m'])} | "
            f"{fmt(row['softR_vs_hop_horizontal_rmse_m']['mean_gain_m'])} | "
            f"{fmt(row['softR_vs_hop_vertical_rmse_m']['mean_gain_m'])} | "
            f"{fmt(row['softR_horizontal_rmse_m'])} | {fmt(row['softR_vertical_rmse_m'])} | {row['n']} |"
        )

    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "This is a state-space diagnostic under the same simulation protocol as 191/238. It supports axis-wise simulation interpretation only and does not replace real-water validation.",
    ])
    return "\n".join(lines) + "\n"


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [
        (distance, ci, cond, i)
        for distance in DISTANCES
        for ci, cond in enumerate(CONDITIONS)
        for i in range(GEOMS)
    ]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for done, future in enumerate(as_completed(futures), start=1):
            distance, _, cond, i = futures[future]
            rows.extend(future.result())
            print(f"[{done:03d}/{len(cases)}] axis {int(distance)} m {cond[0]} #{i}", flush=True)

    rows.sort(key=lambda r: (r["distance_m"], r["condition"], r["index"], r["policy"]))
    raw_payload = {
        "config": {
            "stage": "axis_wise_error_decomposition_raw_checkpoint",
            "source_protocol": "191/238 moving full-range validation",
            "distances_m": list(DISTANCES),
            "geoms_per_distance_condition": GEOMS,
            "steps": STEPS,
            "settle_start": SETTLE_START,
        },
        "trials": rows,
    }
    (HERE / "axis_wise_validation_raw_checkpoint.json").write_text(json.dumps(raw_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    payload = {
        "config": {
            "stage": "axis_wise_error_decomposition_validation",
            "source_protocol": "191/238 moving full-range validation",
            "distances_m": list(DISTANCES),
            "geoms_per_distance_condition": GEOMS,
            "conditions": [
                {"name": c[0], "speed_m_s": c[1], "mode": c[2], "vertical_speed_m_s": c[3]}
                for c in CONDITIONS
            ],
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "truth_usage": "truth is used for signal synthesis and post-update error decomposition only; filter decisions use observations/qualities/innovations.",
            "claim_boundary": "simulation axis-wise diagnostic; not real-water validation",
        },
        "summary": summarize(rows),
        "trials": rows,
    }
    (HERE / "axis_wise_validation.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    text = markdown(payload)
    (HERE / "result_summary.md").write_text(text, encoding="utf-8")
    print(text)
    return payload


if __name__ == "__main__":
    run()
