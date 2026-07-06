"""동력학 없이 매 ping 위치를 푸는 Gauss-Newton NLS 스냅샷 추정기.

재귀 필터(EKF/UKF)의 동력학 이득을 드러내는 비교 기준선이다. 각 ping에서 관측 z를 가장 잘
맞추는 위치를 R^{-1} 가중 최소제곱으로 반복 추정하고, 공분산은 (Hᵀ R^{-1} H)^{-1}로 근사한다.
"""

from __future__ import annotations

import numpy as np

from config import ChannelConfig
from ekf import _numeric_jacobian
from measurement import wrap_angle


def solve_position(observation, initial_position, cfg: ChannelConfig,
                   measurement_covariance, iterations=8, tol=1e-4):
    """단일 ping Gauss-Newton 위치 추정. 초기값은 직전 추정/초기화 위치."""
    R_inv = np.linalg.inv(measurement_covariance)
    position = np.asarray(initial_position, float).copy()
    for _ in range(iterations):
        predicted, H = _numeric_jacobian(position, cfg)
        residual = np.asarray(observation, float) - predicted
        residual[8:] = wrap_angle(residual[8:])
        normal = H.T @ R_inv @ H
        gradient = H.T @ R_inv @ residual
        try:
            delta = np.linalg.solve(normal + 1e-9 * np.eye(3), gradient)
        except np.linalg.LinAlgError:
            break
        position = position + delta
        if np.linalg.norm(delta) < tol:
            break
    predicted, H = _numeric_jacobian(position, cfg)
    covariance = np.linalg.inv(H.T @ R_inv @ H + 1e-9 * np.eye(3))
    return position, covariance
