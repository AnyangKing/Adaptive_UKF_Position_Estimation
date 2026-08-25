"""Filter-consistency audit for transition-aware softR.

This script reuses the frozen moving-target 0--1000 m protocol from folder 191
and adds position NEES / measurement NIS diagnostics. It intentionally does not
change the estimator decision rule.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
from scipy.stats import chi2, wilcoxon


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
F191 = ROOT / "191. Moving full range transition aware independent validation"
F63 = next(ROOT.glob("63. *"))
sys.path.insert(0, str(F63))


def _load_f191():
    path = F191 / "run_moving_full_range_independent_validation.py"
    spec = importlib.util.spec_from_file_location("moving_full_range_191", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


m191 = _load_f191()

DISTANCES = m191.DISTANCES
CONDITIONS = m191.CONDITIONS
GEOMS = m191.GEOMS
STEPS = m191.STEPS
SETTLE_START = m191.SETTLE_START
ROUTING_THRESHOLD_DEG = m191.ROUTING_THRESHOLD_DEG
RANGE_JUMP_THRESHOLD_M = m191.RANGE_JUMP_THRESHOLD_M
MAX_TOA_SCALE = m191.MAX_TOA_SCALE

POLICIES = ("fixed_baseline", "hop_baseline", "hop_transition_softR")
POS_NEES_DOF = 3
TOTAL_NIS_DOF = 10


def safe_quad(value: np.ndarray, covariance: np.ndarray) -> float:
    value = np.asarray(value, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    try:
        return float(value @ np.linalg.solve(covariance, value))
    except np.linalg.LinAlgError:
        return float(value @ np.linalg.pinv(covariance) @ value)


def block_quad(residual: np.ndarray, covariance: np.ndarray, indices: slice) -> float:
    return safe_quad(residual[indices], covariance[indices, indices])


def apply_policy_step(
    ukf: Any,
    observation: np.ndarray,
    quality: dict[str, Any],
    policy: str,
    carrier_hz: float,
    previous_range_m: float | None,
    previous_carrier_hz: float | None,
) -> tuple[dict[str, Any], float, float]:
    """Run one causal predict/update step and return diagnostic metadata.

    Returns `(diag, current_range_m, current_carrier_hz)`.
    """

    ukf.predict()
    R = ukf.R.copy()
    disagreement = float(quality["doa_disagreement_deg"])
    disagreement_scale = min(100.0, 1.0 + (disagreement / 2.0) ** 2)
    routed_to_tdoa = disagreement > ROUTING_THRESHOLD_DEG
    if routed_to_tdoa:
        R[1:8, 1:8] *= disagreement_scale
    else:
        R[8:10, 8:10] *= disagreement_scale

    current_range_m = float(observation[0])
    current_carrier_hz = float(carrier_hz)
    carrier_changed = False
    range_jump_m = 0.0
    transition_risk = False
    transition_scale = 1.0

    if policy == "hop_transition_softR":
        if previous_range_m is None or previous_carrier_hz is None:
            raise RuntimeError("softR policy must be primed with previous range/carrier")
        range_jump_m = abs(current_range_m - float(previous_range_m))
        carrier_changed = abs(current_carrier_hz - float(previous_carrier_hz)) > 1.0e-6
        transition_risk = bool(carrier_changed and range_jump_m > RANGE_JUMP_THRESHOLD_M)
        if transition_risk:
            transition_scale = min(
                MAX_TOA_SCALE,
                1.0 + (range_jump_m / max(RANGE_JUMP_THRESHOLD_M, 1.0e-9)) ** 2,
            )
            R[0, 0] *= transition_scale

    _, _, predicted_route, _, S_route = ukf.measurement_statistics(R)
    residual_route = ukf._z_residual(np.asarray(observation).copy(), predicted_route)
    block_nis_route = {
        "toa": block_quad(residual_route, S_route, slice(0, 1)),
        "tdoa": block_quad(residual_route, S_route, slice(1, 8)),
        "doa": block_quad(residual_route, S_route, slice(8, 10)),
    }
    for name, indices, limit in (
        ("toa", slice(0, 1), 6.63),
        ("tdoa", slice(1, 8), 18.48),
        ("doa", slice(8, 10), 9.21),
    ):
        R[indices, indices] *= min(100.0, max(1.0, block_nis_route[name] / limit))

    _, _, predicted_final, _, S_final = ukf.measurement_statistics(R)
    residual_final = ukf._z_residual(np.asarray(observation).copy(), predicted_final)
    block_nis_final = {
        "toa": block_quad(residual_final, S_final, slice(0, 1)),
        "tdoa": block_quad(residual_final, S_final, slice(1, 8)),
        "doa": block_quad(residual_final, S_final, slice(8, 10)),
    }
    total_nis_final = safe_quad(residual_final, S_final)
    ukf.update(observation, R)

    diag = {
        "carrier_hz": current_carrier_hz,
        "carrier_changed": carrier_changed,
        "range_jump_m": range_jump_m,
        "transition_risk": transition_risk,
        "transition_scale": float(transition_scale),
        "disagreement_deg": disagreement,
        "routed_to_tdoa": bool(routed_to_tdoa),
        "block_nis_route": block_nis_route,
        "block_nis_final": block_nis_final,
        "total_nis_final": float(total_nis_final),
        "measurement_variance_trace": float(np.trace(R)),
    }
    return diag, current_range_m, current_carrier_hz


def summarize_vector(values: list[float], dof: int) -> dict[str, Any]:
    finite = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if finite.size == 0:
        return {
            "mean": None,
            "median": None,
            "p90": None,
            "chi2_95_exceed_fraction": None,
            "chi2_99_exceed_fraction": None,
            "finite_n": 0,
            "dof": dof,
        }
    return {
        "mean": float(np.mean(finite)),
        "median": float(np.median(finite)),
        "p90": float(np.percentile(finite, 90.0)),
        "chi2_95_exceed_fraction": float(np.mean(finite > chi2.ppf(0.95, dof))),
        "chi2_99_exceed_fraction": float(np.mean(finite > chi2.ppf(0.99, dof))),
        "finite_n": int(finite.size),
        "dof": dof,
    }


def run_filter_with_consistency(observations, qualities, truth, carriers, policy: str) -> dict[str, Any]:
    ukf, initial = m191.make_filter(observations[0])
    estimates = np.zeros((STEPS, 3))
    estimates[0] = initial
    step_diags: list[dict[str, Any]] = []
    pos_nees_values: list[float] = []
    total_nis_values: list[float] = []
    block_nis_values = {"toa": [], "tdoa": [], "doa": []}
    exceptions = 0
    previous_range_m = float(observations[0][0])
    previous_carrier_hz = float(carriers[0])

    for k in range(1, STEPS):
        try:
            diag, previous_range_m, previous_carrier_hz = apply_policy_step(
                ukf,
                observations[k],
                qualities[k],
                policy,
                float(carriers[k]),
                previous_range_m,
                previous_carrier_hz,
            )
            estimates[k] = ukf.x[:3]
            pos_error = ukf.x[:3] - truth[k]
            pos_nees = safe_quad(pos_error, ukf.P[:3, :3])
            diag["position_nees"] = pos_nees
            diag["position_error_m"] = float(np.linalg.norm(pos_error))
            step_diags.append({"step": k, **diag})
        except Exception as exc:  # keep parity with 191's failure handling
            exceptions += 1
            estimates[k] = estimates[k - 1]
            step_diags.append({
                "step": k,
                "exception": type(exc).__name__,
                "message": str(exc),
                "position_nees": float("nan"),
                "total_nis_final": float("nan"),
            })

    errors = np.linalg.norm(estimates - truth, axis=1)
    settled_diags = [d for d in step_diags if d["step"] >= SETTLE_START]
    for diag in settled_diags:
        pos_nees_values.append(float(diag.get("position_nees", float("nan"))))
        total_nis_values.append(float(diag.get("total_nis_final", float("nan"))))
        for block in block_nis_values:
            value = diag.get("block_nis_final", {}).get(block, float("nan"))
            block_nis_values[block].append(float(value))

    transition_events = [d for d in step_diags if d.get("transition_risk")]
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(errors[SETTLE_START:] ** 2))),
        "median_settled_error_m": float(np.median(errors[SETTLE_START:])),
        "p90_settled_error_m": float(np.percentile(errors[SETTLE_START:], 90.0)),
        "maximum_position_error_m": float(np.max(errors)),
        "diverged": bool(np.any(errors > 50.0)),
        "filter_exceptions": int(exceptions),
        "transition_risk_count": len(transition_events),
        "mean_transition_scale": float(np.mean([d["transition_scale"] for d in transition_events])) if transition_events else 1.0,
        "position_nees": summarize_vector(pos_nees_values, POS_NEES_DOF),
        "total_nis": summarize_vector(total_nis_values, TOTAL_NIS_DOF),
        "block_nis": {
            "toa": summarize_vector(block_nis_values["toa"], 1),
            "tdoa": summarize_vector(block_nis_values["tdoa"], 7),
            "doa": summarize_vector(block_nis_values["doa"], 2),
        },
        "step_diagnostics": step_diags,
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
            **run_filter_with_consistency(obs_fixed, q_fixed, truth, fixed_carriers, "fixed_baseline"),
        },
        {
            **common,
            "policy": "hop_baseline",
            **run_filter_with_consistency(obs_hop, q_hop, truth, m191.HOP_CARRIERS_HZ, "hop_baseline"),
        },
        {
            **common,
            "policy": "hop_transition_softR",
            **run_filter_with_consistency(obs_hop, q_hop, truth, m191.HOP_CARRIERS_HZ, "hop_transition_softR"),
        },
    ]


def bootstrap_ci(values: np.ndarray, seed: int = 238, n: int = 3000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def compare(keys: list[tuple[float, str, int]], ref: dict, test: dict) -> dict[str, Any]:
    gains = np.array([ref[k]["settled_rmse_m"] - test[k]["settled_rmse_m"] for k in keys])
    try:
        p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
    except ValueError:
        p = 1.0
    return {
        "mean_gain_m": float(np.mean(gains)),
        "median_gain_m": float(np.median(gains)),
        "gain_ci95": bootstrap_ci(gains),
        "wilcoxon_gain_gt0_p": p,
        "improved_fraction": float(np.mean(gains > 0)),
        "tail_worsened_fraction": float(np.mean(gains < -1.0)),
        "n": len(keys),
    }


def aggregate_metric(subset: list[dict[str, Any]], metric: str, field: str = "mean") -> float | None:
    values = [r[metric][field] for r in subset if r[metric][field] is not None]
    if not values:
        return None
    return float(np.mean(values))


def aggregate_block_metric(subset: list[dict[str, Any]], block: str, field: str = "mean") -> float | None:
    values = [
        r["block_nis"][block][field]
        for r in subset
        if r["block_nis"][block][field] is not None
    ]
    if not values:
        return None
    return float(np.mean(values))


def fmt(value: float | None, digits: int = 2) -> str:
    return "NA" if value is None else f"{value:.{digits}f}"


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"overall": {}, "by_distance": {}, "by_condition": {}, "comparisons": {}}
    by_policy = {p: [r for r in rows if r["policy"] == p] for p in POLICIES}
    for policy, subset in by_policy.items():
        summary["overall"][policy] = {
            "mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in subset])),
            "median_rmse_m": float(np.median([r["settled_rmse_m"] for r in subset])),
            "mean_p90_error_m": float(np.mean([r["p90_settled_error_m"] for r in subset])),
            "divergence_rate": float(np.mean([r["diverged"] for r in subset])),
            "mean_position_nees": aggregate_metric(subset, "position_nees"),
            "median_position_nees": aggregate_metric(subset, "position_nees", "median"),
            "p90_position_nees": aggregate_metric(subset, "position_nees", "p90"),
            "position_nees_chi2_99_exceed_fraction": aggregate_metric(subset, "position_nees", "chi2_99_exceed_fraction"),
            "mean_total_nis": aggregate_metric(subset, "total_nis"),
            "median_total_nis": aggregate_metric(subset, "total_nis", "median"),
            "p90_total_nis": aggregate_metric(subset, "total_nis", "p90"),
            "total_nis_chi2_99_exceed_fraction": aggregate_metric(subset, "total_nis", "chi2_99_exceed_fraction"),
            "mean_toa_nis": aggregate_block_metric(subset, "toa"),
            "mean_tdoa_nis": aggregate_block_metric(subset, "tdoa"),
            "mean_doa_nis": aggregate_block_metric(subset, "doa"),
            "total_transition_risks": int(sum(r["transition_risk_count"] for r in subset)),
            "n": len(subset),
        }

    fixed = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "fixed_baseline"}
    hop = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_baseline"}
    soft = {(r["distance_m"], r["condition"], r["index"]): r for r in rows if r["policy"] == "hop_transition_softR"}
    keys = sorted(soft)
    summary["comparisons"]["softR_vs_hop"] = compare(keys, hop, soft)
    summary["comparisons"]["softR_vs_fixed"] = compare(keys, fixed, soft)
    summary["comparisons"]["hop_vs_fixed"] = compare(keys, fixed, hop)

    for distance in DISTANCES:
        dkeys = [k for k in keys if k[0] == distance]
        drows = [r for r in rows if r["distance_m"] == distance]
        summary["by_distance"][str(distance)] = {
            "softR_vs_hop": compare(dkeys, hop, soft),
            "softR_vs_fixed": compare(dkeys, fixed, soft),
            "mean_softR_position_nees": aggregate_metric([r for r in drows if r["policy"] == "hop_transition_softR"], "position_nees"),
            "mean_softR_total_nis": aggregate_metric([r for r in drows if r["policy"] == "hop_transition_softR"], "total_nis"),
            "n": len(dkeys),
        }

    for condition, *_ in CONDITIONS:
        ckeys = [k for k in keys if k[1] == condition]
        crows = [r for r in rows if r["condition"] == condition]
        summary["by_condition"][condition] = {
            "softR_vs_hop": compare(ckeys, hop, soft),
            "softR_mean_position_nees": aggregate_metric([r for r in crows if r["policy"] == "hop_transition_softR"], "position_nees"),
            "softR_mean_total_nis": aggregate_metric([r for r in crows if r["policy"] == "hop_transition_softR"], "total_nis"),
        }
    return summary


def markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# softR filter consistency validation",
        "",
        "## Headline",
        "",
        "- Position NEES is a 3-dof consistency diagnostic. Ideal mean is approximately 3; values far above 3 indicate overconfidence and values far below 3 indicate underconfidence.",
        "- Total NIS is a 10-dof measurement consistency diagnostic for TOA + 7 TDOA + 2 DOA. Ideal mean is approximately 10.",
        "- This is a diagnostic rerun of the 191 moving-target protocol, not a new algorithm.",
        "",
        "## Overall policy metrics",
        "",
        "| policy | RMSE m | div. | pos NEES | pos NEES P90 | pos NEES > chi2-99 | total NIS | total NIS P90 | total NIS > chi2-99 | n |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for policy, row in summary["overall"].items():
        lines.append(
            f"| {policy} | {row['mean_rmse_m']:.3f} | {row['divergence_rate']:.3f} | "
            f"{fmt(row['mean_position_nees'])} | {fmt(row['p90_position_nees'])} | "
            f"{fmt(row['position_nees_chi2_99_exceed_fraction'], 3)} | {fmt(row['mean_total_nis'])} | "
            f"{fmt(row['p90_total_nis'])} | {fmt(row['total_nis_chi2_99_exceed_fraction'], 3)} | {row['n']} |"
        )
    lines.extend([
        "",
        "## Paired RMSE comparisons",
        "",
        "| comparison | mean gain m | 95% CI | Wilcoxon p | improved frac | tail worsened | n |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for name, comp in summary["comparisons"].items():
        ci = comp["gain_ci95"]
        lines.append(
            f"| {name} | {comp['mean_gain_m']:.3f} | [{ci[0]:.3f}, {ci[1]:.3f}] | "
            f"{comp['wilcoxon_gain_gt0_p']:.4g} | {comp['improved_fraction']:.3f} | "
            f"{comp['tail_worsened_fraction']:.3f} | {comp['n']} |"
        )
    lines.extend([
        "",
        "## softR consistency by distance",
        "",
        "| distance m | softR gain vs hop m | tail worsened | softR pos NEES | softR total NIS | n |",
        "|---:|---:|---:|---:|---:|---:|",
    ])
    for distance in DISTANCES:
        row = summary["by_distance"][str(distance)]
        comp = row["softR_vs_hop"]
        lines.append(
            f"| {int(distance)} | {comp['mean_gain_m']:.3f} | {comp['tail_worsened_fraction']:.3f} | "
            f"{fmt(row['mean_softR_position_nees'])} | {fmt(row['mean_softR_total_nis'])} | {row['n']} |"
        )
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "This folder answers whether the current transition-aware softR result has a covariance-consistency warning flag under the same simulation protocol. It does not claim real-water consistency, hardware response validation, or arbitrary moving-target generalization.",
        "",
    ])
    return "\n".join(lines)


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
            print(f"[{done:03d}/{len(cases)}] consistency {int(distance)} m {cond[0]} #{i}", flush=True)

    rows.sort(key=lambda r: (r["distance_m"], r["condition"], r["index"], r["policy"]))
    raw_payload = {
        "config": {
            "stage": "softR_filter_consistency_validation_raw_checkpoint",
            "source_protocol": "191. Moving full range transition aware independent validation",
            "distances_m": list(DISTANCES),
            "geoms_per_distance_condition": GEOMS,
            "conditions": [
                {"name": c[0], "speed_m_s": c[1], "mode": c[2], "vertical_speed_m_s": c[3]}
                for c in CONDITIONS
            ],
            "steps": STEPS,
            "settle_start": SETTLE_START,
        },
        "trials": rows,
    }
    (HERE / "softR_consistency_validation_raw_checkpoint.json").write_text(
        json.dumps(raw_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    payload = {
        "config": {
            "stage": "softR_filter_consistency_validation",
            "source_protocol": "191. Moving full range transition aware independent validation",
            "distances_m": list(DISTANCES),
            "geoms_per_distance_condition": GEOMS,
            "conditions": [
                {"name": c[0], "speed_m_s": c[1], "mode": c[2], "vertical_speed_m_s": c[3]}
                for c in CONDITIONS
            ],
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "position_nees_dof": POS_NEES_DOF,
            "total_nis_dof": TOTAL_NIS_DOF,
            "divergence_definition": "trial divergent if any per-ping 3D position error exceeds 50 m",
            "truth_usage": "truth is used for signal synthesis, final error computation, and post-update NEES diagnostics only; filter decisions use observations/qualities/innovations.",
            "claim_boundary": "simulation consistency diagnostic; not real-water validation",
        },
        "summary": summarize(rows),
        "trials": rows,
    }
    (HERE / "softR_consistency_validation.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    text = markdown(payload)
    (HERE / "result_summary.md").write_text(text, encoding="utf-8")
    print(text)
    return payload


if __name__ == "__main__":
    run()
