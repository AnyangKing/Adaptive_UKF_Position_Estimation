"""50번 신규 feature 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from newfeatures import FEATURE_NAMES, structure_features
from run_newfeatures import geometry, measure


def test_features_finite_and_named():
    cfg = replace(ChannelConfig(), second_order_multipath=True, surface_roughness=0.3, seed=7)
    pos = np.array([300.0, 20.0, -40.0])
    _, received, _ = synthesize_received(pos, cfg)
    f = structure_features(received[0], cfg)
    assert set(f) == set(FEATURE_NAMES)
    assert all(np.isfinite(v) for v in f.values())


def test_first_reflection_delay_nonnegative():
    cfg = replace(ChannelConfig(), second_order_multipath=True, surface_roughness=0.2, seed=3)
    _, received, _ = synthesize_received(np.array([200.0, 0.0, -30.0]), cfg)
    f = structure_features(received[0], cfg)
    assert f["first_reflection_delay_us"] >= 0.0
    assert f["peak_count"] >= 1.0


def test_measure_row_has_features_and_bias():
    pos, env = geometry(200, 0)
    row = measure(pos, env, 200, 0)
    assert np.isfinite(row["el_bias_deg"])
    for n in FEATURE_NAMES:
        assert n in row and np.isfinite(row[n])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
