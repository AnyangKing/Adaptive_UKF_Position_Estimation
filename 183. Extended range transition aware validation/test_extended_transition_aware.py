import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent


def test_constants():
    spec = importlib.util.spec_from_file_location(
        "runner", HERE / "run_extended_transition_aware_validation.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert module.DISTANCES == (800.0, 1000.0)
    assert module.RANGE_JUMP_THRESHOLD_M == 0.5
    assert module.MAX_TOA_SCALE == 100.0
