"""Carrier-transition-aware selective TOA guard for the adaptive-R UKF.

The guard isolates only absolute TOA (measurement index 0) when a carrier
change coincides with a large adjacent raw-range jump.  TDOA and DOA remain
active.  This first implementation is intentionally scoped to static and
quasi-static operation.
"""

from __future__ import annotations

import numpy as np


class CarrierTransitionTOAGuardUKF:
    def __init__(
        self,
        ukf,
        disagreement_threshold_deg: float,
        range_jump_threshold_m: float = 0.5,
        isolated_toa_variance_m2: float = 1.0e12,
    ):
        self.ukf = ukf
        self.base_R = ukf.R.copy()
        self.disagreement_threshold_deg = float(disagreement_threshold_deg)
        self.range_jump_threshold_m = float(range_jump_threshold_m)
        self.isolated_toa_variance_m2 = float(isolated_toa_variance_m2)
        self.previous_range_m: float | None = None
        self.previous_carrier_hz: float | None = None
        self.history: list[dict] = []

    def prime(self, observation: np.ndarray, carrier_hz: float) -> None:
        self.previous_range_m = float(observation[0])
        self.previous_carrier_hz = float(carrier_hz)

    @staticmethod
    def _nis(residual: np.ndarray, covariance: np.ndarray, indices: slice) -> float:
        value = residual[indices]
        block = covariance[indices, indices]
        return float(value @ np.linalg.solve(block, value))

    def step(self, observation: np.ndarray, quality: dict, carrier_hz: float):
        if self.previous_range_m is None or self.previous_carrier_hz is None:
            raise RuntimeError("prime() must be called with ping 0 before step()")
        observation = np.asarray(observation)
        carrier_hz = float(carrier_hz)
        range_jump_m = abs(float(observation[0]) - self.previous_range_m)
        carrier_changed = abs(carrier_hz - self.previous_carrier_hz) > 1.0e-6
        toa_guarded = bool(carrier_changed and range_jump_m > self.range_jump_threshold_m)

        self.ukf.predict()
        R = self.base_R.copy()
        disagreement = float(quality["doa_disagreement_deg"])
        scale = min(100.0, 1.0 + (disagreement / 2.0) ** 2)
        routed_to_tdoa = disagreement > self.disagreement_threshold_deg
        if routed_to_tdoa:
            R[1:8, 1:8] *= scale
        else:
            R[8:10, 8:10] *= scale

        _, _, predicted, _, S = self.ukf.measurement_statistics(R)
        residual = self.ukf._z_residual(observation.copy(), predicted)
        block_nis = {
            "toa": self._nis(residual, S, slice(0, 1)),
            "tdoa": self._nis(residual, S, slice(1, 8)),
            "doa": self._nis(residual, S, slice(8, 10)),
        }
        for name, indices, limit in (
            ("toa", slice(0, 1), 6.63),
            ("tdoa", slice(1, 8), 18.48),
            ("doa", slice(8, 10), 9.21),
        ):
            if name == "toa" and toa_guarded:
                R[0, 0] = max(R[0, 0], self.isolated_toa_variance_m2)
            else:
                R[indices, indices] *= min(100.0, max(1.0, block_nis[name] / limit))

        total_nis = float(residual @ np.linalg.solve(S, residual))
        self.ukf.update(observation, R)
        self.history.append({
            "carrier_hz": carrier_hz,
            "range_jump_m": range_jump_m,
            "carrier_changed": carrier_changed,
            "toa_guarded": toa_guarded,
            "disagreement_deg": disagreement,
            "routed_to_tdoa": routed_to_tdoa,
            "block_nis": block_nis,
            "total_nis": total_nis,
        })
        self.previous_range_m = float(observation[0])
        self.previous_carrier_hz = carrier_hz
        return self.ukf.x.copy()
