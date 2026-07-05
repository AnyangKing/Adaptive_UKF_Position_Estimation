"""UKF 예측 방향과 SRP 점수를 함께 이용하는 다중가설 연관."""

import numpy as np


class HypothesisAdaptiveRUKF:
    def __init__(self, ukf, candidate_count=1, minimum_score_ratio=1.0, score_weight_deg=0.0):
        self.ukf = ukf; self.base_R = ukf.R.copy()
        self.candidate_count = int(candidate_count)
        self.minimum_score_ratio = float(minimum_score_ratio)
        self.score_weight_deg = float(score_weight_deg); self.history = []

    @staticmethod
    def _nis(residual, covariance, indices):
        value = residual[indices]; block = covariance[indices, indices]
        return float(value @ np.linalg.solve(block, value))

    def step(self, observation, quality):
        self.ukf.predict(); R = self.base_R.copy()
        _, _, predicted, _, _ = self.ukf.measurement_statistics(R)
        predicted_direction = np.array([np.cos(predicted[9]) * np.cos(predicted[8]),
                                        np.cos(predicted[9]) * np.sin(predicted[8]), np.sin(predicted[9])])
        eligible = [(i, c) for i, c in enumerate(quality["candidates"][:self.candidate_count])
                    if c["score_ratio"] >= self.minimum_score_ratio]
        if not eligible:
            eligible = [(0, quality["candidates"][0])]
        costs = [np.degrees(np.arccos(np.clip(predicted_direction @ c["direction"], -1.0, 1.0)))
                 + self.score_weight_deg * (1.0 - c["score_ratio"]) for _, c in eligible]
        rank, selected = eligible[int(np.argmin(costs))]
        z = np.asarray(observation).copy(); z[8] = selected["azimuth_rad"]; z[9] = selected["elevation_rad"]

        gcc_direction = np.array([np.cos(quality["gcc_elevation_rad"]) * np.cos(quality["gcc_azimuth_rad"]),
                                  np.cos(quality["gcc_elevation_rad"]) * np.sin(quality["gcc_azimuth_rad"]),
                                  np.sin(quality["gcc_elevation_rad"])])
        disagreement = float(np.degrees(np.arccos(np.clip(gcc_direction @ selected["direction"], -1.0, 1.0))))
        routing_scale = min(100.0, 1.0 + (disagreement / 2.0) ** 2)
        if disagreement > 5.0: R[1:8, 1:8] *= routing_scale
        else: R[8:10, 8:10] *= routing_scale
        _, _, predicted, _, S = self.ukf.measurement_statistics(R)
        residual = self.ukf._z_residual(z.copy(), predicted)
        for indices, limit in ((slice(0, 1), 6.63), (slice(1, 8), 18.48), (slice(8, 10), 9.21)):
            R[indices, indices] *= min(100.0, max(1.0, self._nis(residual, S, indices) / limit))
        self.ukf.update(z, R)
        self.history.append({"selected_rank": rank, "switched": rank > 0, "score_ratio": selected["score_ratio"]})
        return self.ukf.x.copy()
