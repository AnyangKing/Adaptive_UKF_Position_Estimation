import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent


def test_distance_grid():
    spec = importlib.util.spec_from_file_location("runner", HERE / "run_full_range_sweep.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert module.DISTANCES[0] == 0.0
    assert module.DISTANCES[-1] == 1000.0
    assert len(module.DISTANCES) == 11
    assert module.GEOMS == 6
