"""Validate the completed post-hoc guard pilot without promoting it to a claim."""

from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "transition_toa_guard_pilot.json"


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def trial(payload: dict, geometry: int, schedule: str, method: str) -> dict:
    return next(
        row for row in payload["trials"]
        if row["geometry_index"] == geometry
        and row["schedule_name"] == schedule
        and row["method"] == method
    )


def test_result_scope_and_decision():
    payload = load()
    assert payload["config"]["stage"] == "post_hoc_development_pilot"
    assert payload["config"]["static_scope_only"] is True
    assert payload["config"]["independent_validation_required"] is True
    assert payload["config"]["manuscript_claim_allowed"] is False
    assert payload["decision"] == "advance_to_independent_validation"
    assert all(payload["criteria"].values())


def test_catastrophic_case_is_rescued_only_in_development_data():
    payload = load()
    baseline = trial(payload, 2, "four_carrier_cycle", "baseline_adaptive_r")
    guarded = trial(payload, 2, "four_carrier_cycle", "transition_toa_guard")
    assert abs(baseline["settled_rmse_m"] - 53.00129101046352) < 1.0e-9
    assert guarded["settled_rmse_m"] < 0.25 * baseline["settled_rmse_m"]
    assert guarded["diverged"] is False
    assert guarded["toa_guarded_ping_indices"] == [1, 4, 5, 8, 9, 12, 13, 16, 17]


def test_guard_is_inactive_when_transition_jump_is_absent():
    payload = load()
    for geometry in (2, 5, 19):
        fixed_base = trial(payload, geometry, "fixed32", "baseline_adaptive_r")
        fixed_guard = trial(payload, geometry, "fixed32", "transition_toa_guard")
        assert fixed_guard["toa_guard_count"] == 0
        assert fixed_guard["settled_rmse_m"] == fixed_base["settled_rmse_m"]
    for geometry in (5, 19):
        four_guard = trial(payload, geometry, "four_carrier_cycle", "transition_toa_guard")
        assert four_guard["toa_guard_count"] == 0


if __name__ == "__main__":
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(f"PASS {name}")
    print("all tests passed")
