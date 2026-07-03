"""관측 quality와 block NIS를 사용하는 adaptive R wrapper."""

from __future__ import annotations
import numpy as np

from ukf import SignalObservationUKF


class AdaptiveRUKF:
    def __init__(self, ukf: SignalObservationUKF):
        self.ukf = ukf
        self.base_R = ukf.R.copy()
        self.history: list[dict[str, float]] = []

    @staticmethod
    def _block_nis(residual: np.ndarray, covariance: np.ndarray, indices: slice) -> float:
        value = residual[indices]
        block = covariance[indices, indices]
        return float(value @ np.linalg.solve(block, value))

    def step(self, observation: np.ndarray, quality: dict[str, float]) -> np.ndarray:
        self.ukf.predict()
        adaptive_R = self.base_R.copy()

        # 두 독립적인 배열 처리 결과가 다르면 DOA를 덜 신뢰한다.
        disagreement = quality["doa_disagreement_deg"]
        quality_scale = min(100.0, 1.0 + (disagreement / 2.0) ** 2)
        adaptive_R[8:10, 8:10] *= quality_scale

        _, _, predicted, _, innovation_covariance = self.ukf.measurement_statistics(adaptive_R)
        residual = self.ukf._z_residual(np.asarray(observation).copy(), predicted)
        blocks = {
            "toa": (slice(0, 1), 6.63),       # chi-square 99%, dof 1
            "tdoa": (slice(1, 8), 18.48),    # chi-square 99%, dof 7
            "doa": (slice(8, 10), 9.21),     # chi-square 99%, dof 2
        }
        diagnostics = {"doa_disagreement_deg": disagreement, "doa_quality_scale": quality_scale}
        for name, (indices, threshold) in blocks.items():
            nis = self._block_nis(residual, innovation_covariance, indices)
            scale = min(100.0, max(1.0, nis / threshold))
            adaptive_R[indices, indices] *= scale
            diagnostics[f"{name}_nis"] = nis
            diagnostics[f"{name}_gate_scale"] = scale

        self.ukf.update(observation, adaptive_R)
        self.history.append(diagnostics)
        return self.ukf.x.copy()
