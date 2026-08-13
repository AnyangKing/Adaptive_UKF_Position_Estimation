from pathlib import Path
import json


def test_result_payload_exists_and_has_all_distances():
    payload = json.loads(Path("no_noise_direct_control.json").read_text(encoding="utf-8"))
    assert payload["config"]["include_multipath"] is False
    assert payload["config"]["include_noise"] is False
    assert set(payload["summary"]) == {"600.0", "800.0", "1000.0", "overall"}
    assert len(payload["trials"]) == 24


def test_truth_usage_boundary_recorded():
    payload = json.loads(Path("no_noise_direct_control.json").read_text(encoding="utf-8"))
    assert "signal synthesis and final error" in payload["config"]["truth_usage"]
    assert payload["config"]["manuscript_claim_allowed"] == "mechanism_boundary_control_only"

