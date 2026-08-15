"""Smoke checks for overnight OOD runner."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUNNER = HERE / "run_overnight_ood_validation.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("runner203", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_case_enumeration_default_config():
    module = load_runner()
    cfg = module.load_config(HERE / "overnight_ood_config.json")
    cases = module.enumerate_cases(cfg)
    assert len(cases) == 11 * 4 * 12
    assert module.case_id(cases[0]).startswith("d0000_")


def test_condition_validation():
    module = load_runner()
    cfg = module.load_config(HERE / "overnight_ood_config.json")
    selected = module.selected_conditions(cfg)
    assert len(selected) == 4
    assert selected[0][1][0] == "accelerating_radial"
