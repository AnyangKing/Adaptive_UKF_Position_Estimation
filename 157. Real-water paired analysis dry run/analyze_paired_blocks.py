"""Dry-run paired fixed/hop analysis for folder-156 field logs."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import statistics
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VALIDATOR_PATH = ROOT / "156. Real-water acquisition schema dry run" / "validate_field_log.py"
DEFAULT_INPUT = ROOT / "156. Real-water acquisition schema dry run" / "mock_field_log.csv"
DEFAULT_REPORT = HERE / "paired_analysis_dry_run.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("folder156_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load folder-156 validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mean(rows: list[dict], field: str) -> float:
    return statistics.fmean(float(row[field]) for row in rows)


def session_summary(session_id: str, rows: list[dict]) -> dict:
    fixed = [row for row in rows if row["mode"] == "fixed" and row["exclusion_flag"].lower() == "false"]
    hop = [row for row in rows if row["mode"] == "hop" and row["exclusion_flag"].lower() == "false"]
    if not fixed or not hop:
        raise ValueError(f"{session_id}: paired fixed/hop blocks are required")

    fixed_rmse = mean(fixed, "rmse_mean_m")
    hop_rmse = mean(hop, "rmse_mean_m")
    fixed_p90 = mean(fixed, "rmse_p90_m")
    hop_p90 = mean(hop, "rmse_p90_m")
    fixed_lag1 = mean(fixed, "doa_el_residual_lag1")
    hop_lag1 = mean(hop, "doa_el_residual_lag1")
    fixed_gross = mean(fixed, "gross_error_count")
    hop_gross = mean(hop, "gross_error_count")
    rmse_gain = fixed_rmse - hop_rmse
    rmse_reduction_pct = 100.0 * rmse_gain / fixed_rmse if fixed_rmse else None
    lag1_reduction = fixed_lag1 - hop_lag1

    record_statuses = sorted({row["record_status"] for row in rows})
    if record_statuses == ["mock"]:
        decision = "DRY_RUN_ONLY_NOT_EVIDENCE"
    else:
        tier = rows[0]["tier"]
        if tier == "T1":
            decision = (
                "MECHANISM_PASS_CANDIDATE"
                if fixed_lag1 >= 0.2 and lag1_reduction > 0.2
                else "MECHANISM_PARTIAL_OR_NONINFORMATIVE"
            )
        elif tier == "T2":
            decision = (
                "STATIC_PASS_CANDIDATE"
                if rmse_reduction_pct is not None
                and rmse_reduction_pct >= 10
                and hop_p90 <= fixed_p90
                and hop_gross <= fixed_gross
                and lag1_reduction > 0
                else "STATIC_PARTIAL_OR_FAIL_CANDIDATE"
            )
        else:
            decision = "VERY_SLOW_DRIFT_REVIEW_REQUIRED"

    return {
        "session_id": session_id,
        "record_statuses": record_statuses,
        "tier": rows[0]["tier"],
        "included_fixed_blocks": len(fixed),
        "included_hop_blocks": len(hop),
        "fixed_rmse_mean_m": fixed_rmse,
        "hop_rmse_mean_m": hop_rmse,
        "rmse_gain_m": rmse_gain,
        "rmse_reduction_pct": rmse_reduction_pct,
        "fixed_p90_mean_m": fixed_p90,
        "hop_p90_mean_m": hop_p90,
        "p90_hop_minus_fixed_m": hop_p90 - fixed_p90,
        "fixed_lag1_mean": fixed_lag1,
        "hop_lag1_mean": hop_lag1,
        "lag1_reduction": lag1_reduction,
        "fixed_gross_error_mean": fixed_gross,
        "hop_gross_error_mean": hop_gross,
        "decision": decision,
    }


def analyze(path: Path) -> dict:
    validator = load_validator()
    validation = validator.validate(path)
    if validation["error_count"]:
        raise ValueError(f"input failed folder-156 validation: {validation['errors']}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    sessions: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        sessions[row["session_id"]].append(row)
    summaries = [session_summary(session_id, sessions[session_id]) for session_id in sorted(sessions)]
    statuses = sorted({status for summary in summaries for status in summary["record_statuses"]})
    return {
        "schema": "real-water-paired-analysis-dry-run-1",
        "input": path.name,
        "record_statuses": statuses,
        "is_research_evidence": statuses == ["measured"],
        "disclaimer": (
            "Mock outputs validate software flow only and must not be cited as experimental evidence."
            if "mock" in statuses
            else "Measured outputs remain subject to preregistered exclusions and session-level inference."
        ),
        "session_count": len(summaries),
        "sessions": summaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--allow-mock", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = analyze(args.input)
    if "mock" in report["record_statuses"] and not args.allow_mock:
        print("mock input rejected; use --allow-mock only for software dry runs")
        return 1
    if args.write:
        DEFAULT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {DEFAULT_REPORT.name}: {report['session_count']} dry-run session")
        return 0
    if not DEFAULT_REPORT.is_file():
        print("missing dry-run report; run with --allow-mock --write")
        return 1
    expected = json.loads(DEFAULT_REPORT.read_text(encoding="utf-8"))
    if args.input.resolve() == DEFAULT_INPUT.resolve() and report != expected:
        print("paired-analysis dry-run drift detected")
        return 1
    print(f"ok: {report['session_count']} session; evidence={report['is_research_evidence']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
