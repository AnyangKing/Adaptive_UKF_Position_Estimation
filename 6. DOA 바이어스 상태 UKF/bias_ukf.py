"""방위각·고도각 바이어스를 상태로 포함한 8차원 UKF."""

from __future__ import annotations
import numpy as np

from config import ChannelConfig
from measurement import ideal_measurement, wrap_angle


class DOABiasUKF:
    """상태 [p(3), v(3), b_az, b_el], 각도 bias 단위는 rad."""

    def __init__(self, state, covariance, process_covariance, measurement_covariance,
                 cfg: ChannelConfig, dt_s=1.0, alpha=0.3, beta=2.0, kappa=0.0):
        self.x = np.asarray(state, dtype=float).copy()
        self.P = np.asarray(covariance, dtype=float).copy()
        self.Q = np.asarray(process_covariance, dtype=float).copy()
        self.R = np.asarray(measurement_covariance, dtype=float).copy()
        self.cfg, self.dt, self.n = cfg, dt_s, 8
        self.lam = alpha**2 * (self.n + kappa) - self.n
        count = 2*self.n + 1
        self.wm = np.full(count, 1.0/(2.0*(self.n+self.lam)))
        self.wc = self.wm.copy()
        self.wm[0] = self.lam/(self.n+self.lam)
        self.wc[0] = self.wm[0] + 1.0-alpha**2+beta

    @staticmethod
    def _sym(matrix):
        return 0.5*(matrix+matrix.T)

    def _sigma(self):
        jitter = 0.0
        for _ in range(8):
            try:
                root = np.linalg.cholesky((self.n+self.lam)*
                    (self._sym(self.P)+jitter*np.eye(self.n)))
                break
            except np.linalg.LinAlgError:
                jitter = 1e-12 if jitter == 0 else jitter*10
        else:
            raise np.linalg.LinAlgError("state covariance is not positive definite")
        points = np.empty((2*self.n+1, self.n)); points[0] = self.x
        for i in range(self.n):
            points[i+1] = self.x+root[:, i]
            points[self.n+i+1] = self.x-root[:, i]
        return points

    @staticmethod
    def _z_residual(a, b):
        result = a-b
        result[8:] = wrap_angle(result[8:])
        return result

    def _measurement(self, state):
        result = ideal_measurement(state[:3], self.cfg)
        result[8] = wrap_angle(result[8]+state[6])
        result[9] = wrap_angle(result[9]+state[7])
        return result

    def predict(self):
        sigma = self._sigma(); propagated = sigma.copy()
        propagated[:, :3] += self.dt*propagated[:, 3:6]
        self.x = self.wm@propagated
        difference = propagated-self.x
        self.P = self._sym(self.Q+np.einsum("i,ij,ik->jk", self.wc, difference, difference))

    def measurement_statistics(self, measurement_covariance=None):
        sigma = self._sigma()
        transformed = np.vstack([self._measurement(point) for point in sigma])
        mean = self.wm@transformed
        for j in (8, 9):
            mean[j] = np.arctan2(self.wm@np.sin(transformed[:, j]),
                                 self.wm@np.cos(transformed[:, j]))
        dz = np.vstack([self._z_residual(row.copy(), mean) for row in transformed])
        covariance = self.R if measurement_covariance is None else measurement_covariance
        innovation_covariance = self._sym(covariance+
            np.einsum("i,ij,ik->jk", self.wc, dz, dz))
        return sigma, transformed, mean, dz, innovation_covariance

    def update(self, observation, measurement_covariance=None):
        sigma, _, mean, dz, innovation_covariance = self.measurement_statistics(measurement_covariance)
        dx = sigma-self.x
        cross = np.einsum("i,ij,ik->jk", self.wc, dx, dz)
        gain = np.linalg.solve(innovation_covariance, cross.T).T
        self.x += gain@self._z_residual(np.asarray(observation).copy(), mean)
        self.P = self._sym(self.P-gain@innovation_covariance@gain.T)
        if not np.all(np.isfinite(self.x)) or np.min(np.linalg.eigvalsh(self.P)) < -1e-8:
            raise FloatingPointError("invalid bias UKF state/covariance")

    def step(self, observation, measurement_covariance=None):
        self.predict(); self.update(observation, measurement_covariance)
        return self.x.copy()


def bias_process_covariance(dt_s=1.0, acceleration_std=0.20,
                            bias_walk_std_deg=0.03):
    result = np.zeros((8, 8))
    block = acceleration_std**2*np.array(
        [[dt_s**4/4, dt_s**3/2], [dt_s**3/2, dt_s**2]])
    for axis in range(3):
        ids = [axis, axis+3]
        result[np.ix_(ids, ids)] = block
    result[6, 6] = result[7, 7] = np.radians(bias_walk_std_deg)**2
    return result
