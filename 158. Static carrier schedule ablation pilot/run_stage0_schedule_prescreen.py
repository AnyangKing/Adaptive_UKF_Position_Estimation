"""Stage-0 carrier-sensitivity pre-screen for static 400/600 m schedules.

The script uses only the frozen carrier-bias curves from folder 58.  It does
not run a UKF and cannot establish localization-RMSE improvement.
"""

from __future__ import annotations

from pathlib import Path
import json
import math

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "58. 반송파 미세도약 코히어런트 편향 진단" / "results" / "agility.json"
STEPS = 20


def make_schedules() -> dict[str, np.ndarray]:
    linear = np.linspace(30.0, 34.0, STEPS)
    rng = np.random.default_rng(158)
    fixed3_hop1 = np.full(STEPS, 32.0)
    fixed3_hop1[np.arange(3, STEPS, 4)] = np.array([30.0, 31.0, 33.0, 34.0, 30.0])
    return {
        "fixed32": np.full(STEPS, 32.0),
        "linear20_30_34": linear,
        "narrow_linear20_31_33": np.linspace(31.0, 33.0, STEPS),
        "wide_linear20_28_36": np.linspace(28.0, 36.0, STEPS),
        "four_carrier_cycle": np.resize(np.array([30.0, 31.333333333, 32.666666667, 34.0]), STEPS),
        "two_extreme_alternating": np.resize(np.array([30.0, 34.0]), STEPS),
        "random20_30_34_seeded": rng.permutation(linear),
        "fixed3_hop1_static": fixed3_hop1,
    }


SCHEDULES = make_schedules()


def lag1_autocorr(values: np.ndarray) -> float:
    values = np.asarray(values, float)
    if np.std(values) < 1.0e-12:
        return 1.0
    a = values[:-1] - values[:-1].mean()
    b = values[1:] - values[1:].mean()
    denominator = math.sqrt(float(np.sum(a * a) * np.sum(b * b)))
    return float(np.sum(a * b) / denominator) if denominator > 1.0e-12 else 0.0


def evaluate_geometry(geometry: dict, schedule_name: str, carriers_khz: np.ndarray, source_grid: np.ndarray) -> dict:
    curve = np.asarray(geometry["curve_deg"], float)
    sequence = np.interp(carriers_khz, source_grid, curve)
    fixed_bias = float(np.interp(32.0, source_grid, curve))
    mean_bias = float(np.mean(sequence))
    return {
        "distance_m": geometry["distance"],
        "geometry_index": geometry["index"],
        "schedule_name": schedule_name,
        "fixed_bias_deg": fixed_bias,
        "schedule_mean_bias_deg": mean_bias,
        "absolute_bias_reduction_deg": abs(fixed_bias) - abs(mean_bias),
        "schedule_rms_bias_deg": float(np.sqrt(np.mean(sequence**2))),
        "schedule_lag1": lag1_autocorr(sequence),
    }


def summarize(rows: list[dict], schedule_name: str, carriers_khz: np.ndarray) -> dict:
    reductions = np.array([row["absolute_bias_reduction_deg"] for row in rows])
    fixed_abs = np.array([abs(row["fixed_bias_deg"]) for row in rows])
    scheduled_abs = np.array([abs(row["schedule_mean_bias_deg"]) for row in rows])
    lag1 = np.array([row["schedule_lag1"] for row in rows])
    p90_gain = float(np.percentile(fixed_abs, 90) - np.percentile(scheduled_abs, 90))
    criteria = {
        "mean_abs_bias_reduction_positive": bool(np.mean(reductions) > 0),
        "median_abs_bias_reduction_positive": bool(np.median(reductions) > 0),
        "improved_fraction_ge_0_60": bool(np.mean(reductions > 0) >= 0.60),
        "p90_abs_bias_not_worse": bool(p90_gain >= 0),
        "mean_abs_lag1_below_0_80": bool(np.mean(np.abs(lag1)) < 0.80),
    }
    return {
        "schedule_name": schedule_name,
        "carriers_khz": [float(value) for value in carriers_khz],
        "status": "assessed_within_58_carrier_grid",
        "mean_fixed_abs_bias_deg": float(np.mean(fixed_abs)),
        "mean_schedule_abs_mean_bias_deg": float(np.mean(scheduled_abs)),
        "mean_abs_bias_reduction_deg": float(np.mean(reductions)),
        "median_abs_bias_reduction_deg": float(np.median(reductions)),
        "improved_fraction": float(np.mean(reductions > 0)),
        "p90_abs_bias_gain_deg": p90_gain,
        "mean_schedule_abs_lag1": float(np.mean(np.abs(lag1))),
        "criteria": criteria,
        "decision": "stage0_candidate" if all(criteria.values()) else "reject_or_defer",
        "n_geometries": len(rows),
    }


def run() -> dict:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    source_grid = np.asarray(source["config"]["carriers_khz"], float)
    geometries = [item for item in source["geometries"] if item["distance"] in {400, 600}]
    trials = []
    summaries = {}
    for schedule_name, carriers in SCHEDULES.items():
        if carriers.min() < source_grid.min() or carriers.max() > source_grid.max():
            summaries[schedule_name] = {
                "schedule_name": schedule_name,
                "carriers_khz": [float(value) for value in carriers],
                "status": "not_assessable_without_new_carrier_simulation",
                "decision": "defer_no_extrapolation",
                "reason": f"source grid is {source_grid.min():.1f}-{source_grid.max():.1f} kHz",
                "n_geometries": 0,
            }
            continue
        rows = [evaluate_geometry(item, schedule_name, carriers, source_grid) for item in geometries]
        trials.extend(rows)
        summaries[schedule_name] = summarize(rows, schedule_name, carriers)

    assessed = [name for name, summary in summaries.items() if summary["status"].startswith("assessed")]
    ranking = sorted(
        assessed,
        key=lambda name: (
            summaries[name]["decision"] == "stage0_candidate",
            summaries[name]["mean_abs_bias_reduction_deg"],
            -summaries[name]["mean_schedule_abs_lag1"],
        ),
        reverse=True,
    )
    payload = {
        "config": {
            "stage": "stage0_carrier_sensitivity_prescreen",
            "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "source_carrier_grid_khz": [float(value) for value in source_grid],
            "distances_m": [400, 600],
            "geometries": len(geometries),
            "ukf_executed": False,
            "localization_rmse_claim_allowed": False,
            "independent_validation_required": True,
        },
        "ranking": ranking,
        "summary": summaries,
        "trials": trials,
    }
    output = HERE / "results"
    output.mkdir(exist_ok=True)
    (output / "stage0_schedule_prescreen.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"ranking": ranking, "summary": summaries}, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run()
