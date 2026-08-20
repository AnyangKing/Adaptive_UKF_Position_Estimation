from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "run_extended_ood_motion_family_validation.py"

spec = importlib.util.spec_from_file_location("h216", SCRIPT)
h216 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(h216)


def test_case_count():
    n = len(h216.DISTANCES) * len(h216.EXTENDED_OOD_CONDITIONS) * h216.GEOMS
    assert n == 144


def test_trajectory_shapes():
    pos, env, az, sign, phase = h216.geometry(600.0, 0, 0)
    assert env["snr_db"] in (10.0, 20.0, 30.0)
    for _, mode in h216.EXTENDED_OOD_CONDITIONS:
        truth = h216.truth_trajectory(pos, az, sign, phase, mode)
        assert truth.shape == (h216.moving191.STEPS, 3)
