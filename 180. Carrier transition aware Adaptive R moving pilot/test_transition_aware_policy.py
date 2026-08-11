import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent


def test_policy_imports_and_constants():
    spec = importlib.util.spec_from_file_location(
        "runner", HERE / "run_transition_aware_moving_pilot.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert module.GEOMS == 4
    assert module.STEPS == 20
    assert len(module.HOP_CARRIERS_HZ) == module.STEPS
    assert module.RANGE_JUMP_THRESHOLD_M > 0
