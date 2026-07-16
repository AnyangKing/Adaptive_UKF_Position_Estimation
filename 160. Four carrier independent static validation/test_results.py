"""Validate the completed independent-validation result and frozen decision."""

from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "four_carrier_independent_validation.json"


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_independent_result_contract():
    payload = load()
    config = payload["config"]
    assert config["stage"] == "stage1b_independent_validation"
    assert config["geometries"] == 20
    assert config["independent_validation"] is True
    assert config["protocol_frozen_before_execution"] is True
    assert config["automatic_manuscript_update_allowed"] is False
    assert len(payload["trials"]) == 60
    assert all(row["filter_exceptions"] == 0 for row in payload["trials"])


def test_frozen_decision_is_not_overridden_by_median_gain():
    payload = load()
    comparisons = payload["comparisons"]
    assert payload["decision"] == "independent_validation_failed"
    assert comparisons["linear_vs_fixed"]["pass"] is True
    assert comparisons["four_vs_fixed"]["pass"] is False
    assert comparisons["four_vs_linear"]["pass"] is False
    assert comparisons["four_vs_fixed"]["median_gain_m"] > 0.0
    assert comparisons["four_vs_fixed"]["mean_gain_m"] < 0.0
    assert comparisons["four_vs_fixed"]["p90_rmse_gain_m"] < 0.0
    assert payload["summary"]["four_carrier_cycle"]["divergence_rate"] > 0.0


if __name__ == "__main__":
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(f"PASS {name}")
    print("all tests passed")
