"""Minimal diagnostic checks for folder 145."""

from __future__ import annotations

import json
from pathlib import Path


def test_json_exists_and_matches_manuscript_rounding() -> None:
    path = Path(__file__).resolve().parent / "results" / "two_ray_fit.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = {case["distance_m"]: case for case in data["selected_cases"]}
    assert abs(cases[400]["delta_ms"] - 1.34) < 0.01
    assert abs(cases[400]["fit_r2"] - 0.99) < 0.01
    assert abs(cases[600]["delta_ms"] - 1.87) < 0.01
    assert abs(cases[600]["fit_r2"] - 0.75) < 0.01


def test_svg_exists() -> None:
    path = Path(__file__).resolve().parent / "results" / "two_ray_fit.svg"
    assert path.exists()
    assert "<svg" in path.read_text(encoding="utf-8")


if __name__ == "__main__":
    test_json_exists_and_matches_manuscript_rounding()
    test_svg_exists()
    print("ok")
