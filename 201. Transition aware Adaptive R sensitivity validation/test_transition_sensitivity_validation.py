"""Smoke tests for the transition sensitivity validation script."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "run_transition_sensitivity_validation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("sens201", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_variant_grid_contains_canonical():
    module = load_module()
    assert len(module.VARIANTS) == 9
    assert module.CANONICAL in module.VARIANTS
    assert module.variant_name(0.5, 100.0) == "softR_thr0.5_cap100"


def test_baselines_have_528_cases():
    module = load_module()
    fixed, hop = module.load_191_baselines()
    assert len(fixed) == 528
    assert len(hop) == 528
    assert set(fixed) == set(hop)


def test_subset_size_is_24_cases_per_variant():
    module = load_module()
    assert len(module.SENSITIVITY_DISTANCES) * len(module.m191.CONDITIONS) * module.SENSITIVITY_GEOMS == 24
