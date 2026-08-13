from pathlib import Path
import json


def test_payload_shape():
    payload = json.loads(Path("moving_full_range_diagnostic.json").read_text(encoding="utf-8"))
    assert payload["config"]["distances_m"] == [float(d) for d in range(0, 1001, 100)]
    assert payload["config"]["geoms_per_distance_condition"] == 3
    assert len(payload["trials"]) == 11 * 4 * 3 * 3


def test_comparisons_exist():
    payload = json.loads(Path("moving_full_range_diagnostic.json").read_text(encoding="utf-8"))
    comps = payload["summary"]["comparisons"]
    assert "softR_vs_hop" in comps
    assert "softR_vs_fixed" in comps
    assert "hop_vs_fixed" in comps

