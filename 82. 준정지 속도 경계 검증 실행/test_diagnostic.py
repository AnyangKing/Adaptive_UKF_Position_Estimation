"""82번 준정지 속도 경계 검증 계약을 최소 검증한다 (pytest 없이 순수 Python).

이 폴더는 커밋 전 감사에서 test 파일이 누락된 것을 발견해 추가했다. run_quasi_static_boundary.py
자체는 수정하지 않고, 그 함수들의 계약(정지/이동 궤적 생성, carrier 적용, lag-1 자기상관 계산)만
검증한다.
"""

import numpy as np

from config import ChannelConfig
from run_quasi_static_boundary import (
    CONDITIONS, SPEEDS_M_S, STEPS, FIXED_CARRIER_HZ, HOP_CARRIERS_HZ,
    conditions, geometry, truth_trajectory, collect, lag1_autocorr,
)


def test_conditions_cover_all_speeds_and_modes():
    """0 m/s는 static 1개, 나머지 5속도×2방향=10개, 총 11조건."""
    names = {c["name"] for c in CONDITIONS}
    assert "static_0.000" in names
    assert len(CONDITIONS) == 1 + (len(SPEEDS_M_S) - 1) * 2
    assert all(c["mode"] in ("static", "radial", "tangential") for c in CONDITIONS)


def test_hop_carriers_within_optimal_band_and_distinct():
    bw = ChannelConfig().chirp_bandwidth_hz
    nyq = ChannelConfig().sample_rate_hz / 2
    assert len(HOP_CARRIERS_HZ) == STEPS
    assert HOP_CARRIERS_HZ.min() >= 30000.0 and HOP_CARRIERS_HZ.max() <= 34000.0
    assert HOP_CARRIERS_HZ.max() + bw / 2 < nyq
    assert len(set(HOP_CARRIERS_HZ.tolist())) == STEPS
    assert FIXED_CARRIER_HZ == 32000.0


def test_static_trajectory_is_stationary():
    pos, env, _az, _sign = geometry(0, 0)
    t = truth_trajectory(pos, az=0.3, sign=1.0, speed=0.0, mode="static")
    assert t.shape == (STEPS, 3)
    assert np.allclose(t, pos)


def test_moving_trajectory_matches_speed():
    pos, _env, _az, _sign = geometry(3, 1)
    t_rad = truth_trajectory(pos, az=0.7, sign=1.0, speed=0.05, mode="radial")
    step_dist = np.linalg.norm(t_rad[1] - t_rad[0])
    assert abs(step_dist - 0.05) < 1e-9
    r0 = np.hypot(*pos[:2])
    r_last = np.hypot(*t_rad[-1][:2])
    assert r_last > r0  # sign=+1 radial이면 거리 증가


def test_lag1_autocorr_known_cases():
    """완전 상관(직선 증가)은 +1 근방, 완전 반전(부호교대)은 -1 근방."""
    trending = np.arange(20, dtype=float)
    alternating = np.array([(-1.0) ** i for i in range(20)])
    assert lag1_autocorr(trending) > 0.9
    assert lag1_autocorr(alternating) < -0.9
    assert lag1_autocorr(np.zeros(20)) == 0.0  # 분산 0 → 정의상 0


def test_collect_runs_and_carrier_changes_observation():
    pos, env, _az, _sign = geometry(0, 0)
    truth = truth_trajectory(pos, az=0.1, sign=1.0, speed=0.0, mode="static")
    fixed = np.full(STEPS, FIXED_CARRIER_HZ)
    obs_f, q_f, err_f = collect(truth, env, 0, 0, fixed)
    obs_h, q_h, err_h = collect(truth, env, 0, 0, HOP_CARRIERS_HZ)
    assert obs_f.shape == obs_h.shape == (STEPS, 10)
    assert len(q_f) == len(q_h) == STEPS
    assert not np.allclose(obs_f, obs_h)
    assert np.all(np.isfinite(err_f)) and np.all(np.isfinite(err_h))


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
