"""선형 음속 gradient에서 굴절(휜 경로)로 인한 직접파 도착 고도각 변화 계산.

음속이 깊이에 따라 c(depth)=c0+g·depth로 변하면 광선이 휜다(Snell). 광선 방정식은
  d(depth)/dx = tan θ,  dθ/dx = -g / c(depth)
(θ = 수평 기준 grazing angle, depth 아래 방향 양). g=0이면 θ 일정 = 직선(등속)으로 환원된다.

배열은 매우 작으므로(반경 0.033 m), 굴절의 지배적 효과는 배열에 도착하는 파면의 고도각이
직선 기하 대비 이동하는 것이다. 소스→배열중심 eigenray를 shoot로 풀어 도착 grazing angle을
구하고, 직선(g=0) 대비 차이를 직접파 도착 고도각 이동으로 적용한다(평면파 근사). Ground Truth
미사용 — 순수 물리 채널.
"""

from __future__ import annotations

import numpy as np

from config import ChannelConfig


def c_of_depth(depth, cfg: ChannelConfig):
    return cfg.sound_speed_m_s + cfg.sound_speed_gradient * depth


def _shoot_depth_at_range(theta0, ds, X, cfg, steps=400):
    """launch grazing angle θ0으로 소스 깊이 ds에서 수평거리 X까지 광선을 적분, 도착 깊이·각도."""
    g = cfg.sound_speed_gradient
    dx = X / steps
    d, theta = ds, theta0
    for _ in range(steps):
        def deriv(d_, th_):
            return np.tan(th_), -g / max(c_of_depth(d_, cfg), 1.0)
        k1d, k1t = deriv(d, theta)
        k2d, k2t = deriv(d + 0.5*dx*k1d, theta + 0.5*dx*k1t)
        k3d, k3t = deriv(d + 0.5*dx*k2d, theta + 0.5*dx*k2t)
        k4d, k4t = deriv(d + dx*k3d, theta + dx*k3t)
        d += dx/6.0*(k1d + 2*k2d + 2*k3d + k4d)
        theta += dx/6.0*(k1t + 2*k2t + 2*k3t + k4t)
    return d, theta


def arrival_grazing(ds, dr, X, cfg, iters=12):
    """소스 깊이 ds에서 수평 X 떨어진 깊이 dr에 도달하는 eigenray의 도착 grazing angle."""
    if X < 1e-6:
        return 0.0
    theta = np.arctan2(dr - ds, X)   # 직선 chord 각도로 초기화
    lo, hi = theta - np.radians(30.0), theta + np.radians(30.0)
    d_lo = _shoot_depth_at_range(lo, ds, X, cfg)[0] - dr
    for _ in range(iters):
        mid = 0.5*(lo + hi)
        d_mid = _shoot_depth_at_range(mid, ds, X, cfg)[0] - dr
        if d_lo * d_mid <= 0:
            hi = mid
        else:
            lo, d_lo = mid, d_mid
    theta0 = 0.5*(lo + hi)
    return _shoot_depth_at_range(theta0, ds, X, cfg)[1]


def refraction_elevation_shift(source_m, center_m, cfg: ChannelConfig) -> float:
    """직선(g=0) 대비 굴절 도착 grazing 차이 = 직접파 도착 고도각 이동(rad)."""
    if cfg.sound_speed_gradient == 0.0:
        return 0.0
    ds = -float(source_m[2]); dr = -float(center_m[2])   # 깊이(양)
    X = float(np.hypot(source_m[0] - center_m[0], source_m[1] - center_m[1]))
    straight_cfg = ChannelConfig(sound_speed_m_s=cfg.sound_speed_m_s, sound_speed_gradient=0.0)
    g_arr = arrival_grazing(ds, dr, X, cfg)
    s_arr = arrival_grazing(ds, dr, X, straight_cfg)
    # 도착 grazing 증가 = 소스가 더 아래에서 오는 것처럼 보임 → 고도각 감소.
    return -(g_arr - s_arr)
