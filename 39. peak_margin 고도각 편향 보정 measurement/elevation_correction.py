"""peak_margin으로 고도각 계통 편향을 예측해 관측 고도각에서 차감하는 보정.

38번에서 gated-SRP peak_margin이 고도각 편향(el_bias = 측정고도 - 참고도)의 관측가능한
예측자였다(전 거리 유의, 600m 최강). 여기서는 validation 궤적의 ping별 (peak_margin, el_bias)로
el_bias ≈ a + b·peak_margin을 최소제곱 적합해 (a,b)를 고정하고, test에서 관측 고도각을
z[9] -= clip(a + b·peak_margin)로 보정한다. GT는 validation calibration residual 산출에만 쓴다.

거리 label 없이 쓰도록 계수는 전 거리 공통(global)으로 적합한다. 과보정 폭주를 막기 위해
예측 편향을 물리적으로 타당한 범위(기본 ±3°)로 클립한다.
"""

from __future__ import annotations

import numpy as np

MAX_CORRECTION_RAD = np.radians(3.0)


def fit_correction(validation_records) -> dict:
    """validation ping을 모아 el_bias ≈ a + b·peak_margin을 최소제곱 적합한다."""
    margins, biases = [], []
    for rec in validation_records:
        true_el = rec["true_elevation_rad"]
        obs_el = rec["observations"][:, 9]
        for k in range(len(true_el)):
            margins.append(float(rec["qualities"][k]["peak_margin"]))
            # el_bias는 측정 - 참. angle wrap은 작으므로 직접 차분.
            biases.append(float(obs_el[k] - true_el[k]))
    margins = np.asarray(margins); biases = np.asarray(biases)
    design = np.column_stack([np.ones_like(margins), margins])
    beta, *_ = np.linalg.lstsq(design, biases, rcond=None)
    residual = biases - design @ beta
    return {
        "intercept_rad": float(beta[0]),
        "slope_rad_per_margin": float(beta[1]),
        "n_pings": int(len(margins)),
        "fit_residual_std_deg": float(np.degrees(np.std(residual))),
        "raw_bias_std_deg": float(np.degrees(np.std(biases))),
    }


def predicted_bias_rad(peak_margin: float, correction: dict) -> float:
    value = correction["intercept_rad"] + correction["slope_rad_per_margin"] * peak_margin
    return float(np.clip(value, -MAX_CORRECTION_RAD, MAX_CORRECTION_RAD))


def corrected_observations(record, correction: dict) -> np.ndarray:
    """관측 배열을 복사해 고도각 열(z[9])에서 예측 편향을 차감한다."""
    z = record["observations"].copy()
    for k in range(z.shape[0]):
        z[k, 9] -= predicted_bias_rad(record["qualities"][k]["peak_margin"], correction)
    return z
