"""Validate exact replay and the observed carrier-induced TOA-switch pattern."""

from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "sparse_carrier_tail_diagnostic.json"


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def schedule(payload: dict, geometry_index: int, name: str) -> dict:
    geometry = next(item for item in payload["geometries"] if item["geometry_index"] == geometry_index)
    return geometry["schedules"][name]


def test_exact_replay_matches_folder_160_headlines():
    payload = load()
    assert abs(schedule(payload, 2, "fixed32")["summary"]["settled_rmse_m"] - 10.15059265482023) < 1e-9
    assert abs(schedule(payload, 2, "linear20_30_34")["summary"]["settled_rmse_m"] - 7.359864641771166) < 1e-9
    assert abs(schedule(payload, 2, "four_carrier_cycle")["summary"]["settled_rmse_m"] - 53.00129101046352) < 1e-9


def test_catastrophic_case_is_repeated_toa_switch_not_raw_doa_spike():
    payload = load()
    linear = schedule(payload, 2, "linear20_30_34")["summary"]
    four = schedule(payload, 2, "four_carrier_cycle")["summary"]
    assert 3.5 < linear["raw_range_error_span_m"] < 3.6
    assert 3.5 < four["raw_range_error_span_m"] < 3.6
    assert linear["adjacent_raw_range_jumps_over_0_5m"] == 1
    assert four["adjacent_raw_range_jumps_over_0_5m"] == 9
    assert four["raw_range_error_total_variation_m"] > 30.0
    assert four["maximum_toa_block_nis"] > 100.0
    assert four["maximum_abs_raw_elevation_bias_deg"] < 1.0
    assert four["large_error_ping_indices"] == [16, 17, 18, 19]


def test_controls_do_not_have_large_range_switches():
    payload = load()
    for geometry_index in (5, 19):
        four = schedule(payload, geometry_index, "four_carrier_cycle")["summary"]
        assert four["adjacent_raw_range_jumps_over_0_5m"] == 0
        assert four["maximum_adjacent_raw_range_jump_m"] < 0.03


if __name__ == "__main__":
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(f"PASS {name}")
    print("all tests passed")
