"""43번 추정기 비교 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from config import ChannelConfig
from consistency import nees, nis
from ekf import _numeric_jacobian, ExtendedKalmanFilter
from measurement import (fixed_measurement_covariance, ideal_measurement,
                        usb_array_global_m)
from nls import solve_position
from ukf import acceleration_process_covariance


def test_jacobian_matches_forward_model():
    """수치 야코비안이 유한하고, 관측함수의 국소 선형화로 예측을 근사한다."""
    cfg = ChannelConfig()
    pos = np.array([300.0, 40.0, -30.0])
    base, H = _numeric_jacobian(pos, cfg)
    assert H.shape == (10, 3) and np.all(np.isfinite(H))
    dp = np.array([1.0, -0.5, 0.3])
    approx = base + H @ dp
    exact = ideal_measurement(pos + dp, cfg)
    # 각도 성분 제외 거리 성분에서 1차 근사가 실제와 가깝다.
    assert np.max(np.abs((approx - exact)[:8])) < 0.05


def test_nls_recovers_position_noise_free():
    """무잡음 이상 관측이면 NLS가 참위치를 cm급으로 복원한다."""
    cfg = ChannelConfig()
    truth = np.array([250.0, -60.0, -35.0])
    z = ideal_measurement(truth, cfg)
    start = truth + np.array([5.0, -4.0, 3.0])
    pos, cov = solve_position(z, start, cfg, fixed_measurement_covariance())
    assert np.linalg.norm(pos - truth) < 0.5
    assert cov.shape == (3, 3)


def test_ekf_step_runs():
    cfg = ChannelConfig()
    truth = np.array([200.0, 30.0, -25.0])
    z = ideal_measurement(truth, cfg)
    state = np.r_[truth + np.array([3.0, 2.0, -1.0]), np.zeros(3)]
    ekf = ExtendedKalmanFilter(state, np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    x = ekf.step(z)
    assert np.all(np.isfinite(x)) and np.linalg.norm(x[:3] - truth) < 8.0


def test_nees_nis_basic():
    cov = np.diag([1.0, 4.0, 9.0])
    assert abs(nees(np.array([1.0, 2.0, 3.0]), np.zeros(3), cov) - (1 + 1 + 1)) < 1e-9
    S = np.eye(4) * 2.0
    assert abs(nis(np.array([2.0, 0, 0, 0]), S) - 2.0) < 1e-9


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
