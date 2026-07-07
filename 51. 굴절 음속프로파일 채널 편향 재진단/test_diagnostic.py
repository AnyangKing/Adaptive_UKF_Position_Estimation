"""51번 굴절 채널 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from refraction import refraction_elevation_shift, arrival_grazing
from run_refraction import geometry, measure


def test_zero_gradient_matches_baseline():
    """g=0이면 굴절 보정이 없어 신호가 등속 채널과 완전히 동일(회귀 방지)."""
    src = np.array([300.0, 20.0, -35.0])
    c0 = replace(ChannelConfig(), second_order_multipath=True, seed=9, sound_speed_gradient=0.0)
    _, a, _ = synthesize_received(src, c0, include_noise=False)
    _, b, _ = synthesize_received(src, c0, include_noise=False)
    assert np.allclose(a, b)


def test_gradient_shifts_arrival():
    """음속 gradient가 있으면 도착 고도각이 이동하고 신호가 달라진다."""
    src = np.array([400.0, 0.0, -40.0]); center = np.array([0.0, 0.0, -30.0])
    cfg = replace(ChannelConfig(), sound_speed_gradient=-0.05)
    shift = refraction_elevation_shift(src, center, cfg)
    assert abs(np.degrees(shift)) > 0.1     # 400m서 수분의 1도 이동
    c0 = replace(ChannelConfig(), sound_speed_gradient=0.0, seed=3)
    cg = replace(ChannelConfig(), sound_speed_gradient=-0.05, seed=3)
    _, r0, _ = synthesize_received(src, c0, include_noise=False)
    _, rg, _ = synthesize_received(src, cg, include_noise=False)
    assert not np.allclose(r0, rg)


def test_straight_arrival_equals_chord():
    """g=0이면 도착 grazing이 직선 chord 각도와 같다."""
    grazing = arrival_grazing(40.0, 30.0, 400.0, replace(ChannelConfig(), sound_speed_gradient=0.0))
    assert abs(grazing - np.arctan2(30.0 - 40.0, 400.0)) < 1e-3


def test_measure_both_gradients():
    pos, env = geometry(200, 0)
    for g in (0.0, -0.05):
        m = measure(pos, env, 200, 0, g)
        assert np.isfinite(m["el_bias_deg"]) and np.isfinite(m["obs_range_m"])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
