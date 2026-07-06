"""42번 기하 다양화 진단 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

import bias_geometry as bg
from run_geometry import summarize_rotation, summarize_within


def test_offsets_start_at_zero():
    assert bg.AZIMUTH_OFFSETS_DEG[0] == 0.0


def test_within_track_cheap():
    """반복·스텝을 줄여 한 궤적 통계가 유한하게 나온다."""
    bg.REPEATS, bg.TRACK_STEPS = 2, 3
    try:
        r = bg.within_track(200, 0)
    finally:
        bg.REPEATS, bg.TRACK_STEPS = 6, 10
    assert np.isfinite(r["mean_abs_bias_deg"])
    assert 0.0 <= r["averaging_retention"]
    assert 0.0 <= r["bearing_change_deg"] <= 180.0


def test_rotation_cheap_and_keys():
    bg.REPEATS = 2
    try:
        biases = bg.azimuth_rotation(400, 0)
    finally:
        bg.REPEATS = 6
    assert set(biases) == set(bg.AZIMUTH_OFFSETS_DEG)
    assert all(np.isfinite(v) for v in biases.values())


def test_summarize_rotation_corr_self_is_one():
    points = [{off: float(np.sin(off) + 0.1 * i) for off in bg.AZIMUTH_OFFSETS_DEG}
              for i in range(5)]
    rotation = {d: points for d in bg.DISTANCES}
    s = summarize_rotation(rotation)
    for d in bg.DISTANCES:
        assert s[str(d)]["by_offset"]["0.0"]["corr_with_0deg"] == 1.0


def test_summarize_within_shape():
    recs = [{"distance": 200, "mean_abs_bias_deg": 0.5, "signed_mean_bias_deg": 0.4,
             "within_track_std_deg": 0.05, "averaging_retention": 0.8,
             "bearing_change_deg": 1.2} for _ in range(4)]
    s = summarize_within(recs)
    assert "median_averaging_retention" in s["200"]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
