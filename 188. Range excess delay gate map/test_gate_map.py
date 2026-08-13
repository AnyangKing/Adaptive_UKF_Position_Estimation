from pathlib import Path
import json


def test_gate_map_payload():
    payload = json.loads(Path("range_excess_delay_gate_map.json").read_text(encoding="utf-8"))
    assert payload["config"]["doa_gate_ms"] == 5.0
    assert len(payload["rows"]) == 11
    assert payload["rows"][1]["horizontal_range_m"] == 100


def test_short_range_surface_out_long_range_surface_in():
    payload = json.loads(Path("range_excess_delay_gate_map.json").read_text(encoding="utf-8"))
    by_range = {row["horizontal_range_m"]: row for row in payload["rows"]}
    assert by_range[100]["surface_inside_5ms_gate"] is False
    assert by_range[600]["surface_inside_5ms_gate"] is True
    assert by_range[1000]["bottom_inside_5ms_gate"] is False

