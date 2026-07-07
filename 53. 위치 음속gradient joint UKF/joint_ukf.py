"""위치·속도·음속 gradient를 함께 추정하는 7차원 joint UKF.

방향 A의 핵심 방법. 상태 x=[px,py,pz,vx,vy,vz,g]. 관측모델은 기존 ideal_measurement(위치)에
굴절에 의한 고도각 이동을 더하는데, 그 이동을 필터 안에서는 gradient·수평거리의 선형 근사로
계산한다(el_shift ≈ K·g·range; 51번에서 shift가 g·range에 선형임을 확인). 이렇게 gradient가
관측(고도각)에 미치는 영향을 모델에 넣어, 궤적의 거리 변화가 만드는 편향 패턴으로부터 상수
gradient를 식별한다. gradient는 궤적 내내 거의 상수라 process noise를 작게 준다.

관측 합성(진짜 채널)은 eigenray 굴절을 쓰고 필터는 선형 근사를 쓰므로 약간의 모델 불일치가 있다
(현실적). Ground Truth는 평가에만.
"""

from __future__ import annotations

import numpy as np

from config import ChannelConfig
from measurement import ideal_measurement, usb_array_global_m, wrap_angle

# 굴절 고도각 이동 선형계수: el_shift[rad] ≈ K · g[s^-1] · horizontal_range[m]
# (51번 eigenray: 400m, g=0.05 → 0.368° = 6.42e-3 rad → K=3.21e-4)
REFRACTION_K = 3.21e-4


class JointPositionGradientUKF:
    def __init__(self, state, covariance, process_covariance, measurement_covariance,
                 cfg: ChannelConfig, dt_s: float = 1.0, alpha: float = 0.3, beta: float = 2.0,
                 kappa: float = 0.0):
        self.x = np.asarray(state, float).copy()
        self.P = np.asarray(covariance, float).copy()
        self.Q = np.asarray(process_covariance, float).copy()
        self.R = np.asarray(measurement_covariance, float).copy()
        self.cfg, self.dt, self.n = cfg, dt_s, 7
        self.center = usb_array_global_m(cfg.receiver_depth_m).mean(axis=0)
        self.lam = alpha**2 * (self.n + kappa) - self.n
        self.wm = np.full(2*self.n+1, 1.0/(2.0*(self.n+self.lam)))
        self.wc = self.wm.copy()
        self.wm[0] = self.lam/(self.n+self.lam)
        self.wc[0] = self.wm[0] + 1.0 - alpha**2 + beta

    @staticmethod
    def _sym(m):
        return 0.5*(m + m.T)

    def _measure(self, point):
        """h(state): 위치 관측 + gradient·거리 선형 굴절 고도각 이동."""
        z = ideal_measurement(point[:3], self.cfg).copy()
        rng = float(np.hypot(point[0]-self.center[0], point[1]-self.center[1]))
        z[9] += REFRACTION_K * point[6] * rng
        return z

    def _sigma(self):
        jitter = 0.0
        for _ in range(8):
            try:
                root = np.linalg.cholesky((self.n+self.lam)*(self._sym(self.P)+jitter*np.eye(self.n)))
                break
            except np.linalg.LinAlgError:
                jitter = 1e-12 if jitter == 0 else jitter*10
        else:
            raise np.linalg.LinAlgError("P not PD")
        pts = np.empty((2*self.n+1, self.n)); pts[0] = self.x
        for i in range(self.n):
            pts[i+1] = self.x + root[:, i]; pts[i+1+self.n] = self.x - root[:, i]
        return pts

    @staticmethod
    def _zres(a, b):
        r = a - b; r[8:] = wrap_angle(r[8:]); return r

    def predict(self):
        sig = self._sigma(); prop = sig.copy()
        prop[:, :3] += self.dt*prop[:, 3:6]     # 위치 += dt·속도, gradient는 유지
        self.x = self.wm @ prop
        d = prop - self.x
        self.P = self._sym(self.Q + np.einsum("i,ij,ik->jk", self.wc, d, d))

    def update(self, observation, measurement_covariance=None):
        R = self.R if measurement_covariance is None else measurement_covariance
        sig = self._sigma()
        Z = np.vstack([self._measure(p) for p in sig])
        zmean = self.wm @ Z
        for j in (8, 9):
            zmean[j] = np.arctan2(self.wm @ np.sin(Z[:, j]), self.wm @ np.cos(Z[:, j]))
        dz = np.vstack([self._zres(row.copy(), zmean) for row in Z])
        S = self._sym(R + np.einsum("i,ij,ik->jk", self.wc, dz, dz))
        dx = sig - self.x
        cross = np.einsum("i,ij,ik->jk", self.wc, dx, dz)
        gain = np.linalg.solve(S, cross.T).T
        innov = self._zres(np.asarray(observation).copy(), zmean)
        self.x = self.x + gain @ innov
        self.P = self._sym(self.P - gain @ S @ gain.T)
        if not np.all(np.isfinite(self.x)):
            raise FloatingPointError("joint UKF diverged")

    def step(self, observation, measurement_covariance=None):
        self.predict(); self.update(observation, measurement_covariance)
        return self.x.copy()
