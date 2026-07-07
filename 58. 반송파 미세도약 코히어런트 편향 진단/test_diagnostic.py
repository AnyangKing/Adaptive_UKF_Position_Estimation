"""58번 반송파 미세도약 진단 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from config import ChannelConfig
from run_agility import (CARRIERS_HZ, cos_fit_r2, el_bias_deg, geometry,
                         surface_direct_delta_s)


def test_carriers_within_optimal_band():
    """모든 반송파가 배열 최적대역 근방(30~34k)이고 Nyquist·대역 안전."""
    bw = ChannelConfig().chirp_bandwidth_hz
    nyq = ChannelConfig().sample_rate_hz / 2
    assert CARRIERS_HZ.min() >= 30000.0 and CARRIERS_HZ.max() <= 34000.0
    assert CARRIERS_HZ.max() + bw/2 < nyq and CARRIERS_HZ.min() - bw/2 > 0


def test_delta_positive_and_reasonable():
    """표면-직접 지연차가 양수이고 물리적 범위(수십 µs~수 ms)."""
    pos, env = geometry(200, 0)
    delta = surface_direct_delta_s(pos, env)
    assert 1e-6 < delta < 20e-3


def test_cos_fit_recovers_synthetic():
    """합성 코사인 곡선에서 cos-fit이 진폭·R²를 복원한다."""
    delta = 0.0005  # 0.5 ms → 주기 2 kHz
    f = np.asarray(CARRIERS_HZ, float)
    y = 0.3 + 0.5*np.cos(2*np.pi*delta*f + 1.0)
    r2, amp, const = cos_fit_r2(f, y, delta)
    assert r2 > 0.99 and abs(amp - 0.5) < 0.02 and abs(const - 0.3) < 0.02


def test_cos_fit_null_on_noise():
    """무관한 잡음 곡선에서는 R²가 낮다."""
    rng = np.random.default_rng(0)
    y = rng.normal(0, 1, len(CARRIERS_HZ))
    r2, _, _ = cos_fit_r2(CARRIERS_HZ, y, 0.0005)
    assert r2 < 0.5


def test_el_bias_runs_single_carrier():
    pos, env = geometry(100, 0)
    b = el_bias_deg(pos, env, 100, 0, 32000.0)
    assert np.isfinite(b)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
