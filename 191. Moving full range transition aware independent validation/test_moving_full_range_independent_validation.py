from pathlib import Path
import json


def test_payload_shape():
    payload = json.loads(Path("moving_full_range_independent_validation.json").read_text(encoding="utf-8"))
    assert payload["config"]["distances_m"] == [float(d) for d in range(0, 1001, 100)]
    assert payload["config"]["geoms_per_distance_condition"] == 12
    assert len(payload["trials"]) == 11 * 4 * 12 * 3
    assert payload["config"]["geometry_seed_root"] == 1_910_000
    assert payload["config"]["ping_seed_root"] == 1_913_000


def test_comparisons_exist():
    payload = json.loads(Path("moving_full_range_independent_validation.json").read_text(encoding="utf-8"))
    comps = payload["summary"]["comparisons"]
    assert "softR_vs_hop" in comps
    assert "softR_vs_fixed" in comps
    assert "hop_vs_fixed" in comps
