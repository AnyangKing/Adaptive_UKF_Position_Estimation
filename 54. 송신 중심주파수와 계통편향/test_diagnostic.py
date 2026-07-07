"""54번 주파수 스윕 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from run_frequency import geometry, measure, CARRIERS_HZ


def test_carriers_within_nyquist():
    """모든 중심주파수 + 대역폭/2가 표본화 Nyquist(96kHz) 안이다."""
    bw = ChannelConfig().chirp_bandwidth_hz
    nyq = ChannelConfig().sample_rate_hz / 2
    for c in CARRIERS_HZ:
        assert c + bw/2 < nyq and c - bw/2 > 0


def test_frequency_changes_signal():
    """중심주파수를 바꾸면 수신 신호가 달라진다."""
    src = np.array([300.0, 20.0, -35.0])
    lo = replace(ChannelConfig(), carrier_hz=16000.0, seed=4)
    hi = replace(ChannelConfig(), carrier_hz=64000.0, seed=4)
    _, a, _ = synthesize_received(src, lo, include_noise=False)
    _, b, _ = synthesize_received(src, hi, include_noise=False)
    assert not np.allclose(a, b)


def test_measure_finite_all_carriers():
    pos, env = geometry(200, 0)
    for c in CARRIERS_HZ:
        m = measure(pos, env, 200, 0, c)
        assert np.isfinite(m["el_bias_deg"]) and np.isfinite(m["ang_err_deg"])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
