"""Diagnostic tests for the folder-156 field-log validator."""

from __future__ import annotations

import csv
import json

import validate_field_log as validator


def main() -> None:
    report = validator.validate(validator.DEFAULT_INPUT)
    assert report["error_count"] == 0
    assert report["row_count"] == 4
    assert report["session_mode_patterns"]["DRYRUN_T1_001"] == ["fixed", "hop", "hop", "fixed"]

    schema = json.loads(validator.SCHEMA_PATH.read_text(encoding="utf-8"))
    with validator.DEFAULT_INPUT.open("r", encoding="utf-8", newline="") as handle:
        source = next(csv.DictReader(handle))
    parsed = {
        name: validator.validate_scalar(source.get(name, ""), spec)
        for name, spec in schema["fields"].items()
    }
    assert validator.validate_conditionals(source, parsed) == []

    bad = dict(parsed)
    bad["carrier_count"] = 20
    assert "fixed mode must use one 32 kHz carrier" in validator.validate_conditionals(source, bad)

    bad = dict(parsed)
    bad["target_speed_mps"] = 0.005
    assert "static target requires zero speed and drift_direction=none" in validator.validate_conditionals(source, bad)

    bad = dict(parsed)
    bad["receiver_depth_m"] = bad["water_depth_m"] + 1
    assert "sensor depth cannot exceed water depth" in validator.validate_conditionals(source, bad)

    bad_row = dict(source)
    bad_row["raw_data_uri"] = "local://not-marked-as-mock"
    assert "mock rows must use mock:// raw_data_uri" in validator.validate_conditionals(bad_row, parsed)
    print("ok")


if __name__ == "__main__":
    main()
