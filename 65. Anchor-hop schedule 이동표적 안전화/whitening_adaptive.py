"""Whitening-aware adaptive-R wrappers for frequency-agile observations.

63번에서 frequency hop은 고도각 오차의 lag-1 자기상관을 강하게 낮췄지만,
이동 표적 RMSE 개선으로 항상 이어지지는 않았다. 이 파일은 hop이 만든
백색화 관측을 무조건 강하게 믿지 않고, ping 간 DOA jump와 innovation을
이용해 DOA R을 추가로 키우는 안전화 wrapper를 제공한다.
"""

from __future__ import annotations

import numpy as np

from measurement import wrap_angle


class WhiteningAwareAdaptiveRUKF:
    def __init__(
        self,
        ukf,
        threshold_deg: float = 5.0,
        base_doa_scale: float = 1.0,
        jump_threshold_deg: float | None = None,
        jump_doa_scale: float = 1.0,
        innovation_guard_scale: float = 1.0,
    ):
        self.ukf = ukf
        self.base_R = ukf.R.copy()
        self.threshold = float(threshold_deg)
        self.base_doa_scale = float(base_doa_scale)
        self.jump_threshold = None if jump_threshold_deg is None else float(jump_threshold_deg)
        self.jump_doa_scale = float(jump_doa_scale)
        self.innovation_guard_scale = float(innovation_guard_scale)
        self.previous_doa = None
        self.history = []

    @staticmethod
    def _nis(residual, covariance, indices):
        value = residual[indices]
        block = covariance[indices, indices]
        return float(value @ np.linalg.solve(block, value))

    def _apply_conditional_routing(self, R, quality):
        disagreement = float(quality["doa_disagreement_deg"])
        scale = min(100.0, 1.0 + (disagreement / 2.0) ** 2)
        routed = disagreement > self.threshold
        if routed:
            R[1:8, 1:8] *= scale
        else:
            R[8:10, 8:10] *= scale
        return disagreement, routed

    def _doa_jump_deg(self, observation):
        doa = np.asarray(observation[8:10], dtype=float)
        if self.previous_doa is None:
            self.previous_doa = doa.copy()
            return 0.0
        diff = wrap_angle(doa - self.previous_doa)
        self.previous_doa = doa.copy()
        return float(np.degrees(np.linalg.norm(diff)))

    def step(self, observation, quality):
        self.ukf.predict()
        R = self.base_R.copy()
        disagreement, routed = self._apply_conditional_routing(R, quality)

        R[8:10, 8:10] *= self.base_doa_scale
        jump_deg = self._doa_jump_deg(observation)
        jump_gate = False
        if self.jump_threshold is not None and jump_deg > self.jump_threshold:
            R[8:10, 8:10] *= self.jump_doa_scale
            jump_gate = True

        _, _, predicted, _, S = self.ukf.measurement_statistics(R)
        residual = self.ukf._z_residual(np.asarray(observation).copy(), predicted)

        block_reports = {}
        for name, indices, limit in (
            ("toa", slice(0, 1), 6.63),
            ("tdoa", slice(1, 8), 18.48),
            ("doa", slice(8, 10), 9.21),
        ):
            nis = self._nis(residual, S, indices)
            block_reports[name] = nis
            R[indices, indices] *= min(100.0, max(1.0, nis / limit))

        if self.innovation_guard_scale > 1.0 and block_reports["doa"] > 9.21:
            R[8:10, 8:10] *= self.innovation_guard_scale

        total_nis = float(residual @ np.linalg.solve(S, residual))
        self.ukf.update(observation, R)
        self.history.append(
            {
                "disagreement_deg": disagreement,
                "routed": routed,
                "jump_deg": jump_deg,
                "jump_gate": jump_gate,
                "nis": total_nis,
                "doa_nis": block_reports["doa"],
                "R_doa_scale": float(R[8, 8] / self.base_R[8, 8]),
            }
        )
        return self.ukf.x.copy()
