"""6차원 constant-velocity Unscented Kalman Filter."""

from __future__ import annotations

import numpy as np

from simulator import observation_from_position, wrap_angle


class UKF:
    def __init__(
        self,
        initial_state: np.ndarray,
        initial_covariance: np.ndarray,
        process_covariance: np.ndarray,
        measurement_covariance: np.ndarray,
        dt_s: float = 1.0,
        alpha: float = 0.3,
        beta: float = 2.0,
        kappa: float = 0.0,
    ) -> None:
        self.x = np.asarray(initial_state, dtype=np.float64).copy()
        self.P = np.asarray(initial_covariance, dtype=np.float64).copy()
        self.Q = np.asarray(process_covariance, dtype=np.float64).copy()
        self.R = np.asarray(measurement_covariance, dtype=np.float64).copy()
        self.dt = dt_s
        self.n = self.x.size
        self.lam = alpha**2 * (self.n + kappa) - self.n
        count = 2 * self.n + 1
        self.wm = np.full(count, 1.0 / (2.0 * (self.n + self.lam)))
        self.wc = self.wm.copy()
        self.wm[0] = self.lam / (self.n + self.lam)
        self.wc[0] = self.wm[0] + (1.0 - alpha**2 + beta)

    @staticmethod
    def _symmetrize(matrix: np.ndarray) -> np.ndarray:
        return 0.5 * (matrix + matrix.T)

    def _sigma_points(self, mean: np.ndarray, covariance: np.ndarray) -> np.ndarray:
        covariance = self._symmetrize(covariance)
        jitter = 0.0
        for _ in range(8):
            try:
                root = np.linalg.cholesky(
                    (self.n + self.lam) * (covariance + jitter * np.eye(self.n))
                )
                break
            except np.linalg.LinAlgError:
                jitter = 1.0e-12 if jitter == 0.0 else jitter * 10.0
        else:
            raise np.linalg.LinAlgError("UKF covariance is not positive definite")
        points = np.empty((2 * self.n + 1, self.n))
        points[0] = mean
        for i in range(self.n):
            points[i + 1] = mean + root[:, i]
            points[self.n + i + 1] = mean - root[:, i]
        return points

    def _transition(self, state: np.ndarray) -> np.ndarray:
        result = state.copy()
        result[:3] += self.dt * state[3:]
        return result

    @staticmethod
    def _measurement(state: np.ndarray) -> np.ndarray:
        return observation_from_position(state[:3])

    @staticmethod
    def _measurement_residual(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        residual = a - b
        residual[8:] = wrap_angle(residual[8:])
        return residual

    def predict(self) -> None:
        sigma = self._sigma_points(self.x, self.P)
        propagated = np.vstack([self._transition(point) for point in sigma])
        self.x = self.wm @ propagated
        difference = propagated - self.x
        self.P = self._symmetrize(
            self.Q + np.einsum("i,ij,ik->jk", self.wc, difference, difference)
        )

    def update(self, observation: np.ndarray) -> None:
        sigma = self._sigma_points(self.x, self.P)
        transformed = np.vstack([self._measurement(point) for point in sigma])

        predicted_z = self.wm @ transformed
        # 각도 평균은 원형 평균으로 덮어쓴다.
        for j in range(8, 24):
            predicted_z[j] = np.arctan2(
                self.wm @ np.sin(transformed[:, j]),
                self.wm @ np.cos(transformed[:, j]),
            )

        dz = np.vstack(
            [self._measurement_residual(row.copy(), predicted_z) for row in transformed]
        )
        dx = sigma - self.x
        innovation_covariance = self._symmetrize(
            self.R + np.einsum("i,ij,ik->jk", self.wc, dz, dz)
        )
        cross_covariance = np.einsum("i,ij,ik->jk", self.wc, dx, dz)
        gain = np.linalg.solve(innovation_covariance, cross_covariance.T).T
        innovation = self._measurement_residual(
            np.asarray(observation, dtype=np.float64).copy(), predicted_z
        )
        self.x = self.x + gain @ innovation
        self.P = self._symmetrize(self.P - gain @ innovation_covariance @ gain.T)
        if not np.all(np.isfinite(self.x)) or np.min(np.linalg.eigvalsh(self.P)) < -1.0e-8:
            raise FloatingPointError("UKF state/covariance became invalid")

    def step(self, observation: np.ndarray) -> np.ndarray:
        self.predict()
        self.update(observation)
        return self.x.copy()


def constant_acceleration_process_covariance(dt_s: float, acceleration_std: float) -> np.ndarray:
    block = np.array(
        [[dt_s**4 / 4.0, dt_s**3 / 2.0], [dt_s**3 / 2.0, dt_s**2]]
    ) * acceleration_std**2
    covariance = np.zeros((6, 6))
    for axis in range(3):
        indices = [axis, axis + 3]
        covariance[np.ix_(indices, indices)] = block
    return covariance

