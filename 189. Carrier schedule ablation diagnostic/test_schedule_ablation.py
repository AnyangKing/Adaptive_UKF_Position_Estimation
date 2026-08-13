from pathlib import Path
import json


def test_schedule_ablation_payload_shape():
    payload = json.loads(Path("schedule_ablation.json").read_text(encoding="utf-8"))
    assert payload["config"]["distance_m"] == 600.0
    assert payload["config"]["include_multipath"] is True
    assert payload["config"]["include_noise"] is True
    assert len(payload["trials"]) == 8
    assert len(payload["config"]["schedules_hz"]) == 6


def test_schedule_comparisons_exist():
    payload = json.loads(Path("schedule_ablation.json").read_text(encoding="utf-8"))
    comps = payload["summary"]["comparisons_vs_fixed"]
    assert "linear20_30_34" in comps
    assert "reverse20_34_30" in comps
    assert "shuffled20_30_34" in comps
    assert "narrow20_31_33" in comps
    assert "sparse5_30_34_repeat" in comps

