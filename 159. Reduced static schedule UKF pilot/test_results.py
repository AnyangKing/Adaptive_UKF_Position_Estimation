"""Validate the completed development-pilot result contract."""

from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "reduced_static_schedule_pilot.json"


def test_result_contract():
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    config = payload["config"]
    assert config["stage"] == "stage1a_development_pilot"
    assert config["geometries"] == 4
    assert config["development_only"] is True
    assert config["independent_validation_required"] is True
    assert config["manuscript_claim_allowed"] is False
    assert len(payload["trials"]) == 16
    assert all(row["filter_exceptions"] == 0 for row in payload["trials"])


def test_prefiltered_candidates_pass_without_becoming_claims():
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    summary = payload["summary"]
    for name in (
        "linear20_30_34",
        "random20_30_34_seeded",
        "four_carrier_cycle",
    ):
        assert summary[name]["pilot_decision"] == "advance_to_independent_validation"
        assert summary[name]["mean_gain_vs_fixed_m"] > 0.0
        assert summary[name]["divergence_rate"] == 0.0
    assert (
        summary["four_carrier_cycle"]["mean_settled_rmse_m"]
        < summary["linear20_30_34"]["mean_settled_rmse_m"]
    )


if __name__ == "__main__":
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(f"PASS {name}")
    print("all tests passed")
