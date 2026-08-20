from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "run_hardware_response_sensitivity.py"

spec = importlib.util.spec_from_file_location("h215", SCRIPT)
h215 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(h215)


def test_response_profile_center_and_edges():
    assert h215.response_delta_snr_db(32_000.0, "edge_loss_6db") == 0.0
    assert h215.response_delta_snr_db(30_000.0, "edge_loss_6db") == -6.0
    assert h215.response_delta_snr_db(34_000.0, "edge_loss_6db") == -6.0
    assert h215.response_delta_snr_db(31_000.0, "edge_loss_6db") == -3.0


def test_case_count():
    n = len(h215.RESPONSE_PROFILES) * len(h215.DISTANCES) * len(h215.CONDITIONS) * h215.GEOMS
    assert n == 576
