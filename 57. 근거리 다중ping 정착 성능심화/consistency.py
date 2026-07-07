"""필터 일관성 지표: 위치 NEES와 관측 NIS.

NEES_k = e_posᵀ P_pos^{-1} e_pos (3-dof, 이상 평균 3), 필터가 과신/과소를 판단.
NIS_k = νᵀ S^{-1} ν (10-dof, 이상 평균 10), 관측 잔차와 예측 공분산의 정합.
"""

import numpy as np

POS_DOF = 3
MEAS_DOF = 10


def nees(estimate_pos, truth_pos, pos_covariance):
    error = np.asarray(estimate_pos) - np.asarray(truth_pos)
    try:
        return float(error @ np.linalg.solve(pos_covariance, error))
    except np.linalg.LinAlgError:
        return float("nan")


def nis(innovation, innovation_covariance):
    innovation = np.asarray(innovation)
    try:
        return float(innovation @ np.linalg.solve(innovation_covariance, innovation))
    except np.linalg.LinAlgError:
        return float("nan")


def summarize_consistency(nees_values, nis_values):
    nees_values = np.asarray([v for v in nees_values if np.isfinite(v)])
    nis_values = np.asarray([v for v in nis_values if np.isfinite(v)])
    return {
        "mean_nees": float(np.mean(nees_values)) if len(nees_values) else float("nan"),
        "nees_dof": POS_DOF,
        "mean_nis": float(np.mean(nis_values)) if len(nis_values) else float("nan"),
        "nis_dof": MEAS_DOF,
    }
