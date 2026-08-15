"""Smoke checks for OOD motion validation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "run_ood_motion_validation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("ood202", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_ood_case_count():
    module = load_module()
    assert len(module.DISTANCES) * len(module.OOD_CONDITIONS) * module.GEOMS == 20


def test_trajectory_shape():
    module = load_module()
    pos, _, az, sign = module.geometry(600.0, 0, 0)
    truth = module.truth_trajectory(pos, az, sign, "curved_arc")
    assert truth.shape == (module.m191.STEPS, 3)
