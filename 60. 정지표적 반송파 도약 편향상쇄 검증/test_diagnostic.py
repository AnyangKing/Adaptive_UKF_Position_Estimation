"""60번 정지표적 도약 검증 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from config import ChannelConfig
from run_static_hop import (DISTANCES, GEOMS, HOP_CARRIERS_HZ, FIXED_CARRIER_HZ,
                            STEPS, SETTLE_START, collect, geometry)


def test_hop_set_and_settle_window():
    bw = ChannelConfig().chirp_bandwidth_hz
    nyq = ChannelConfig().sample_rate_hz / 2
    assert len(HOP_CARRIERS_HZ) == STEPS and len(set(HOP_CARRIERS_HZ.tolist())) == STEPS
    assert HOP_CARRIERS_HZ.max() + bw/2 < nyq and HOP_CARRIERS_HZ.min() - bw/2 > 0
    assert 0 < SETTLE_START < STEPS


def test_geometry_static():
    """정지 표적: radial_velocity 0, 위치가 거리와 일치."""
    pos, env = geometry(400, 0)
    assert env["radial_velocity_m_s"] == 0.0
    assert abs(np.hypot(pos[0], pos[1]) - 400.0) < 1e-6


def test_collect_fixed_vs_hop_differ():
    pos, env = geometry(100, 0)
    fixed = np.full(STEPS, FIXED_CARRIER_HZ)
    obs_f, _ = collect(pos, env, 100, 0, fixed)
    obs_h, _ = collect(pos, env, 100, 0, HOP_CARRIERS_HZ)
    assert obs_f.shape == obs_h.shape == (STEPS, 10)
    assert not np.allclose(obs_f, obs_h)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
