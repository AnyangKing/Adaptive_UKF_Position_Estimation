"""59번 도약 ping 필터 검증 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from config import ChannelConfig
from run_hopping import HOP_CARRIERS_HZ, FIXED_CARRIER_HZ, collect
from trajectory import STEPS


def test_hop_set_within_optimal_band():
    bw = ChannelConfig().chirp_bandwidth_hz
    nyq = ChannelConfig().sample_rate_hz / 2
    assert len(HOP_CARRIERS_HZ) == STEPS
    assert HOP_CARRIERS_HZ.min() >= 30000.0 and HOP_CARRIERS_HZ.max() <= 34000.0
    assert HOP_CARRIERS_HZ.max() + bw/2 < nyq
    assert FIXED_CARRIER_HZ in (32000.0,)


def test_hop_carriers_all_distinct():
    assert len(set(HOP_CARRIERS_HZ.tolist())) == STEPS


def test_collect_shapes_and_hop_changes_obs():
    """고정/도약이 같은 궤적(GT 동일)에서 다른 관측을 만든다."""
    fixed = np.full(STEPS, FIXED_CARRIER_HZ)
    truth_f, obs_f, q_f = collect(100, 0, fixed)
    truth_h, obs_h, q_h = collect(100, 0, HOP_CARRIERS_HZ)
    assert np.allclose(truth_f, truth_h)              # 궤적 동일
    assert obs_f.shape == obs_h.shape == (STEPS, 10)
    assert not np.allclose(obs_f, obs_h)              # 관측은 반송파 따라 달라짐


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
