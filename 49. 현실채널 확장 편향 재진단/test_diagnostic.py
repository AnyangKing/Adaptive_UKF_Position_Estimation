"""49번 현실채널 확장 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

from dataclasses import replace
import numpy as np

from channel import paths_for_sensor, synthesize_received
from config import ChannelConfig
from measurement import usb_array_global_m
from run_rediagnose import geometry, _measure


def test_second_order_adds_paths():
    """2차 반사 옵션이 켜지면 경로가 3개→5개로 늘어난다."""
    cfg3 = ChannelConfig()
    cfg5 = replace(ChannelConfig(), second_order_multipath=True)
    src = np.array([200.0, 30.0, -40.0]); sensor = usb_array_global_m()[0]
    assert len(paths_for_sensor(src, sensor, cfg3)) == 3
    p5 = paths_for_sensor(src, sensor, cfg5)
    assert len(p5) == 5
    assert {p.name for p in p5} == {"direct", "surface", "bottom", "surf_bot", "bot_surf"}


def test_baseline_unchanged_by_default():
    """기본 cfg는 옵션 off라 기존 3경로와 동일(회귀 방지)."""
    cfg = ChannelConfig()
    assert cfg.second_order_multipath is False and cfg.surface_roughness == 0.0
    src = np.array([300.0, 0.0, -30.0]); sensor = usb_array_global_m()[2]
    assert [p.name for p in paths_for_sensor(src, sensor, cfg)] == ["direct", "surface", "bottom"]


def test_roughness_changes_signal():
    """거친 표면 산란이 켜지면 수신 신호가 매끈한 경우와 달라진다."""
    src = np.array([250.0, 20.0, -35.0])
    smooth = replace(ChannelConfig(), second_order_multipath=True, surface_roughness=0.0, seed=5)
    rough = replace(ChannelConfig(), second_order_multipath=True, surface_roughness=0.4, seed=5)
    _, r_smooth, _ = synthesize_received(src, smooth, include_noise=False)
    _, r_rough, _ = synthesize_received(src, rough, include_noise=False)
    assert not np.allclose(r_smooth, r_rough)


def test_measure_runs_both_modes():
    pos, env = geometry(200, 0)
    base = _measure(pos, env, 200, 0, realistic=False)
    real = _measure(pos, env, 200, 0, realistic=True)
    for m in (base, real):
        assert np.isfinite(m["el_bias_deg"]) and np.isfinite(m["ang_err_deg"])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
