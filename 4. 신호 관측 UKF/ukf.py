"""TOA/TDOA/배열 DOA 관측용 6차원 UKF."""

from __future__ import annotations
import numpy as np

from config import ChannelConfig
from measurement import ideal_measurement, wrap_angle


class SignalObservationUKF:
    def __init__(self, state, covariance, process_covariance, measurement_covariance,
                 cfg: ChannelConfig, dt_s: float = 1.0, alpha: float = 0.3,
                 beta: float = 2.0, kappa: float = 0.0):
        self.x = np.asarray(state, dtype=float).copy()
        self.P = np.asarray(covariance, dtype=float).copy()
        self.Q = np.asarray(process_covariance, dtype=float).copy()
        self.R = np.asarray(measurement_covariance, dtype=float).copy()
        self.cfg, self.dt, self.n = cfg, dt_s, 6
        self.lam = alpha**2 * (self.n + kappa) - self.n
        self.wm = np.full(13, 1.0 / (2.0 * (self.n + self.lam)))
        self.wc = self.wm.copy()
        self.wm[0] = self.lam / (self.n + self.lam)
        self.wc[0] = self.wm[0] + 1.0 - alpha**2 + beta

    @staticmethod
    def _sym(matrix):
        return 0.5 * (matrix + matrix.T)

    def _sigma(self):
        jitter = 0.0
        for _ in range(8):
            try:
                root = np.linalg.cholesky((self.n + self.lam) *
                                          (self._sym(self.P) + jitter * np.eye(6)))
                break
            except np.linalg.LinAlgError:
                jitter = 1e-12 if jitter == 0 else jitter * 10
        else:
            raise np.linalg.LinAlgError("state covariance is not positive definite")
        points = np.empty((13, 6)); points[0] = self.x
        for i in range(6):
            points[i + 1] = self.x + root[:, i]
            points[i + 7] = self.x - root[:, i]
        return points

    @staticmethod
    def _z_residual(a, b):
        result = a - b
        result[8:] = wrap_angle(result[8:])
        return result

    def predict(self):
        sigma = self._sigma()
        propagated = sigma.copy()
        propagated[:, :3] += self.dt * propagated[:, 3:]
        self.x = self.wm @ propagated
        difference = propagated - self.x
        self.P = self._sym(self.Q + np.einsum("i,ij,ik->jk", self.wc, difference, difference))

    def update(self, observation):
        sigma = self._sigma()
        transformed = np.vstack([ideal_measurement(point[:3], self.cfg) for point in sigma])
        mean = self.wm @ transformed
        for j in (8, 9):
            mean[j] = np.arctan2(self.wm @ np.sin(transformed[:, j]),
                                 self.wm @ np.cos(transformed[:, j]))
        dz = np.vstack([self._z_residual(row.copy(), mean) for row in transformed])
        dx = sigma - self.x
        innovation_covariance = self._sym(
            self.R + np.einsum("i,ij,ik->jk", self.wc, dz, dz)
        )
        cross = np.einsum("i,ij,ik->jk", self.wc, dx, dz)
        gain = np.linalg.solve(innovation_covariance, cross.T).T
        innovation = self._z_residual(np.asarray(observation).copy(), mean)
        self.x += gain @ innovation
        self.P = self._sym(self.P - gain @ innovation_covariance @ gain.T)
        if not np.all(np.isfinite(self.x)) or np.min(np.linalg.eigvalsh(self.P)) < -1e-8:
            raise FloatingPointError("invalid UKF state/covariance")

    def step(self, observation):
        self.predict(); self.update(observation)
        return self.x.copy()


def acceleration_process_covariance(dt_s: float, std_m_s2: float) -> np.ndarray:
    block = std_m_s2**2 * np.array(
        [[dt_s**4 / 4, dt_s**3 / 2], [dt_s**3 / 2, dt_s**2]]
    )
    result = np.zeros((6, 6))
    for axis in range(3):
        ids = [axis, axis + 3]
        result[np.ix_(ids, ids)] = block
    return result
