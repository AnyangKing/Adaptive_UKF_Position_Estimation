import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "runner", HERE / "run_toa_guard_independent_validation.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_schedules_have_expected_length():
    runner = load_runner()
    assert set(runner.SCHEDULES) == {"fixed32", "linear20_30_34", "four_carrier_cycle"}
    assert all(len(v) == runner.STEPS for v in runner.SCHEDULES.values())


def test_result_schema_if_present():
    path = HERE / "toa_guard_independent_validation.json"
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["config"]["stage"] == "independent_validation"
    assert "truth_usage" in payload["config"]
    assert "summary" in payload
    assert "comparisons" in payload
    assert "criteria" in payload
