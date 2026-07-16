"""Validate real-water block logs against the folder-156 acquisition contract."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "field_log_schema.json"
DEFAULT_INPUT = HERE / "mock_field_log.csv"
DEFAULT_REPORT = HERE / "dry_run_report.json"


def parse_value(value: str, spec: dict):
    kind = spec["type"]
    if kind in {"string", "enum"}:
        parsed = value.strip()
    elif kind == "integer":
        parsed = int(value)
    elif kind == "number":
        parsed = float(value)
    elif kind == "boolean":
        normalized = value.strip().lower()
        if normalized not in {"true", "false"}:
            raise ValueError("expected true or false")
        parsed = normalized == "true"
    elif kind == "datetime_with_timezone":
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            raise ValueError("timezone is required")
    else:
        raise ValueError(f"unknown type {kind}")
    return parsed


def validate_scalar(value: str, spec: dict):
    if not value.strip():
        if spec.get("required"):
            raise ValueError("required value is blank")
        return None
    parsed = parse_value(value, spec)
    if spec["type"] == "enum" and parsed not in spec["values"]:
        raise ValueError(f"expected one of {spec['values']}")
    if "minimum" in spec and parsed < spec["minimum"]:
        raise ValueError(f"below minimum {spec['minimum']}")
    if "minimum_exclusive" in spec and parsed <= spec["minimum_exclusive"]:
        raise ValueError(f"must exceed {spec['minimum_exclusive']}")
    if "maximum" in spec and parsed > spec["maximum"]:
        raise ValueError(f"above maximum {spec['maximum']}")
    return parsed


def validate_conditionals(row: dict, parsed: dict) -> list[str]:
    errors = []
    if parsed["mode"] == "fixed":
        if not (parsed["carrier_min_khz"] == 32 and parsed["carrier_max_khz"] == 32 and parsed["carrier_count"] == 1):
            errors.append("fixed mode must use one 32 kHz carrier")
    elif not (parsed["carrier_min_khz"] < parsed["carrier_max_khz"] and parsed["carrier_count"] > 1):
        errors.append("hop mode must use multiple carriers over a nonzero band")

    if parsed["target_state"] == "static":
        if parsed["target_speed_mps"] != 0 or parsed["drift_direction"] != "none":
            errors.append("static target requires zero speed and drift_direction=none")
    elif parsed["target_speed_mps"] <= 0 or parsed["drift_direction"] == "none":
        errors.append("drift target requires positive speed and a drift direction")

    if parsed["receiver_depth_m"] > parsed["water_depth_m"] or parsed["transmitter_depth_m"] > parsed["water_depth_m"]:
        errors.append("sensor depth cannot exceed water depth")
    if parsed["rmse_p90_m"] < parsed["rmse_median_m"]:
        errors.append("RMSE P90 cannot be below median")
    if parsed["exclusion_flag"] and not row["exclusion_reason"].strip():
        errors.append("excluded block requires exclusion_reason")
    if not parsed["exclusion_flag"] and row["exclusion_reason"].strip():
        errors.append("non-excluded block must leave exclusion_reason blank")
    if parsed["record_status"] == "mock" and not row["raw_data_uri"].startswith("mock://"):
        errors.append("mock rows must use mock:// raw_data_uri")
    if parsed["record_status"] == "measured" and row["raw_data_uri"].startswith("mock://"):
        errors.append("measured rows cannot use mock:// raw_data_uri")
    return errors


def validate(path: Path) -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    fields = schema["fields"]
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        rows = list(reader)

    errors = []
    missing_columns = [name for name in fields if name not in header]
    extra_columns = [name for name in header if name not in fields]
    if missing_columns:
        errors.append({"row": 0, "field": "header", "message": f"missing columns: {missing_columns}"})
    if extra_columns:
        errors.append({"row": 0, "field": "header", "message": f"extra columns: {extra_columns}"})

    parsed_rows = []
    for index, row in enumerate(rows, start=2):
        parsed = {}
        for name, spec in fields.items():
            try:
                parsed[name] = validate_scalar(row.get(name, ""), spec)
            except (TypeError, ValueError) as exc:
                errors.append({"row": index, "field": name, "message": str(exc)})
        if len(parsed) == len(fields):
            for message in validate_conditionals(row, parsed):
                errors.append({"row": index, "field": "conditional", "message": message})
        parsed_rows.append(parsed)

    sessions = defaultdict(list)
    for parsed in parsed_rows:
        if parsed.get("session_id"):
            sessions[parsed["session_id"]].append(parsed)
    patterns = {}
    for session_id, session_rows in sessions.items():
        ordered = sorted(session_rows, key=lambda item: item["sequence_position"])
        modes = [item["mode"] for item in ordered]
        patterns[session_id] = modes
        if ordered and ordered[0]["sequence_design"] == "ABBA" and modes != ["fixed", "hop", "hop", "fixed"]:
            errors.append({"row": 0, "field": "sequence_design", "message": f"{session_id} is not fixed-hop-hop-fixed"})
        if set(modes) != {"fixed", "hop"}:
            errors.append({"row": 0, "field": "mode", "message": f"{session_id} lacks paired fixed/hop blocks"})

    return {
        "schema": "real-water-block-log-validation-1",
        "input": path.name,
        "row_count": len(rows),
        "session_count": len(sessions),
        "record_status_counts": dict(sorted(Counter(str(item.get("record_status")) for item in parsed_rows).items())),
        "mode_counts": dict(sorted(Counter(str(item.get("mode")) for item in parsed_rows).items())),
        "tier_counts": dict(sorted(Counter(str(item.get("tier")) for item in parsed_rows).items())),
        "session_mode_patterns": patterns,
        "error_count": len(errors),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--require-measured", action="store_true")
    args = parser.parse_args()
    report = validate(args.input)
    if args.require_measured and report["record_status_counts"].get("mock", 0):
        print("mock rows are not allowed with --require-measured")
        return 1
    if report["error_count"]:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1
    if args.write:
        DEFAULT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {DEFAULT_REPORT.name}: {report['row_count']} rows, 0 errors")
        return 0
    if not DEFAULT_REPORT.is_file():
        print("missing dry-run report; run with --write")
        return 1
    expected = json.loads(DEFAULT_REPORT.read_text(encoding="utf-8"))
    if args.input.resolve() == DEFAULT_INPUT.resolve() and report != expected:
        print("dry-run report drift detected")
        return 1
    print(f"ok: {report['row_count']} rows, {report['session_count']} session, 0 errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
