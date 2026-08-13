import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent


def test_constants():
    spec = importlib.util.spec_from_file_location("runner", HERE / "run_direct_only_control.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert module.DISTANCES == (600.0, 800.0, 1000.0)
    assert module.GEOMS == 8
    assert len(module.HOP_CARRIERS_HZ) == module.STEPS
