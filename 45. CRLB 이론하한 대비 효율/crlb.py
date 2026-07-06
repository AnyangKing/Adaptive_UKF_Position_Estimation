"""위치 추정의 Cramér-Rao 하한(CRLB)을 관측모델에서 계산한다.

관측이 z = h(p) + n, n~N(0,R)인 Gaussian이면 위치 p(3차원)의 Fisher 정보는 J = Hᵀ R⁻¹ H,
H = ∂h/∂p (10×3). 불편 추정기의 공분산은 J⁻¹ 이상이고, 위치 RMSE 하한 = sqrt(trace(J⁻¹)).

이 하한은 관측잡음 R만 고려한다. 37~42의 array-intrinsic 계통 편향은 R에 없으므로, 실제 RMSE가
CRLB를 초과하는 부분이 곧 미모델링 편향 floor다(RMSE² ≈ CRLB_var + bias²).
"""

from __future__ import annotations

import numpy as np

from config import ChannelConfig
from ekf import _numeric_jacobian
from measurement import fixed_measurement_covariance


def position_crlb(position, cfg: ChannelConfig, measurement_covariance=None):
    """참위치에서 위치 CRLB 공분산 J⁻¹과 RMSE 하한을 반환한다."""
    R = fixed_measurement_covariance() if measurement_covariance is None else measurement_covariance
    _, H = _numeric_jacobian(np.asarray(position, float), cfg)
    R_inv = np.linalg.inv(R)
    fisher = H.T @ R_inv @ H
    crlb_cov = np.linalg.inv(fisher + 1e-12 * np.eye(3))
    rmse_bound = float(np.sqrt(np.trace(crlb_cov)))
    return crlb_cov, rmse_bound
