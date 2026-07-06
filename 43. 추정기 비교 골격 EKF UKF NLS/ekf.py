"""동일 관측모델(TOA/TDOA/DOA)에 대한 6차원 EKF. UKF와 공정 비교용.

관측함수는 UKF와 같은 ideal_measurement를 쓰고, 야코비안은 위치 3성분에 대한 중심차분으로
수치 계산한다(속도 열은 0). 각도(z[8], z[9]) 잔차는 wrap한다.
"""

from __future__ import annotations

import numpy as np

from config import ChannelConfig
from measurement import ideal_measurement, wrap_angle


def _numeric_jacobian(position, cfg, eps=1e-4):
    """H = d(ideal_measurement)/d(position), (10, 3). 속도 열은 0이라 따로 안 만든다."""
    base = ideal_measurement(position, cfg)
    H = np.zeros((len(base), 3))
    for i in range(3):
        dp = np.zeros(3); dp[i] = eps
        plus = ideal_measurement(position + dp, cfg)
        minus = ideal_measurement(position - dp, cfg)
        diff = plus - minus
        diff[8:] = wrap_angle(diff[8:])
        H[:, i] = diff / (2.0 * eps)
    return base, H


class ExtendedKalmanFilter:
    def __init__(self, state, covariance, process_covariance, measurement_covariance,
                 cfg: ChannelConfig, dt_s: float = 1.0):
        self.x = np.asarray(state, float).copy()
        self.P = np.asarray(covariance, float).copy()
        self.Q = np.asarray(process_covariance, float).copy()
        self.R = np.asarray(measurement_covariance, float).copy()
        self.cfg, self.dt = cfg, dt_s
        self.F = np.eye(6)
        for i in range(3):
            self.F[i, i + 3] = dt_s

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, observation, measurement_covariance=None):
        R = self.R if measurement_covariance is None else measurement_covariance
        predicted, Hp = _numeric_jacobian(self.x[:3], self.cfg)
        H = np.zeros((len(predicted), 6)); H[:, :3] = Hp
        innovation = np.asarray(observation, float) - predicted
        innovation[8:] = wrap_angle(innovation[8:])
        S = H @ self.P @ H.T + R
        gain = np.linalg.solve(S, H @ self.P).T
        self.x = self.x + gain @ innovation
        self.P = (np.eye(6) - gain @ H) @ self.P
        self.P = 0.5 * (self.P + self.P.T)
        if not np.all(np.isfinite(self.x)):
            raise FloatingPointError("EKF diverged")
        return innovation, S

    def step(self, observation, measurement_covariance=None):
        self.predict()
        self.update(observation, measurement_covariance)
        return self.x.copy()
