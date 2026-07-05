"""5도 조건부 라우팅에 SRP peak-margin DOA 공분산 조절을 추가."""

import numpy as np


class PeakMarginAdaptiveRUKF:
    def __init__(self, ukf, margin_threshold=None, doa_scale=1.0):
        self.ukf = ukf
        self.base_R = ukf.R.copy()
        self.margin_threshold = margin_threshold
        self.doa_scale = float(doa_scale)
        self.history = []

    @staticmethod
    def _nis(residual, covariance, indices):
        value = residual[indices]; block = covariance[indices, indices]
        return float(value @ np.linalg.solve(block, value))

    def step(self, observation, quality):
        self.ukf.predict(); R = self.base_R.copy()
        disagreement = quality["doa_disagreement_deg"]
        routing_scale = min(100.0, 1.0 + (disagreement / 2.0) ** 2)
        routed = disagreement > 5.0
        if routed:
            R[1:8, 1:8] *= routing_scale
        else:
            R[8:10, 8:10] *= routing_scale

        low_margin = self.margin_threshold is not None and quality["peak_margin"] < self.margin_threshold
        if low_margin:
            R[8:10, 8:10] *= self.doa_scale

        _, _, predicted, _, S = self.ukf.measurement_statistics(R)
        residual = self.ukf._z_residual(np.asarray(observation).copy(), predicted)
        for indices, limit in ((slice(0, 1), 6.63), (slice(1, 8), 18.48), (slice(8, 10), 9.21)):
            nis = self._nis(residual, S, indices)
            R[indices, indices] *= min(100.0, max(1.0, nis / limit))
        self.ukf.update(observation, R)
        self.history.append({"routed": routed, "low_margin": low_margin, "peak_margin": quality["peak_margin"]})
        return self.ukf.x.copy()
