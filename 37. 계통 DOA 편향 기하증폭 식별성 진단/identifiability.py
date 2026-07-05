"""진단 B·C: 진단 A가 추출한 계통 편향이 (B) 기하의 결정론적 함수인지, (C) GT 없이
관측 신호 feature만으로 식별 가능한지 검사한다.

두 진단 모두 validation 기하에서 예측자를 적합하고 독립 test 기하에서 잔차 감소를 본다.
test 결과로 예측자나 모델을 재선택하지 않는다. 기저(baseline)는 validation 평균 편향을
test에 상수로 예측하는 것이고, 잔차 RMSE가 그보다 유의하게 줄면 그 정보원이 계통 편향을
설명한다는 뜻이다.

- B (oracle 상한): 예측자 = 참기하(거리·참방위·참고도). GT를 써서 편향의 결정론적
  성분 상한을 잰다. 크면 원리상 보정 가능, 작으면 편향이 기하로도 예측 불가.
- C (blind 식별성): 예측자 = 관측 신호 feature(GCC-SRP 불일치, gated-full SRP 방향차,
  peak margin, 최소 peak 품질). 여기서 잔차가 유의하게 줄어야 필터가 blind로 편향을
  추정할 수 있다. 안 줄면 이 방향(계통 편향의 blind 보정)도 데이터로 반증된다.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import spearmanr


TARGETS = ("bias_angle_deg", "az_bias_deg", "el_bias_deg")
SIGNAL_FEATURES = ("doa_disagreement_deg", "gated_full_gap_deg", "peak_margin",
                   "neg_min_peak_quality")


def _geometry_design(records):
    """B용 참기하 설계행렬: [1, dist/100, sin/cos(az), sin/cos(el), el]."""
    rows = []
    for r in records:
        az = np.radians(r["true_azimuth_deg"])
        el = np.radians(r["true_elevation_deg"])
        rows.append([1.0, r["distance"] / 100.0, np.sin(az), np.cos(az),
                     np.sin(el), np.cos(el), el])
    return np.asarray(rows)


def _signal_design(records):
    """C용 blind 관측 feature 설계행렬 (표준화 전 원값 + 상수항)."""
    rows = []
    for r in records:
        f = r["features"]
        rows.append([1.0] + [f[name] for name in SIGNAL_FEATURES])
    return np.asarray(rows)


def _standardize(train, test):
    """상수항(0열)은 두고 나머지 열을 train 통계로 표준화한다."""
    mean = train.mean(axis=0)
    std = train.std(axis=0)
    std[0] = 1.0; mean[0] = 0.0
    std[std < 1e-12] = 1.0
    return (train - mean) / std, (test - mean) / std


def _fit_predict(train_x, train_y, test_x, ridge=1e-3):
    """작은 ridge 정규화 최소제곱. 소표본에서 과적합을 눌러 test 일반화를 본다."""
    xtx = train_x.T @ train_x + ridge * np.eye(train_x.shape[1])
    beta = np.linalg.solve(xtx, train_x.T @ train_y)
    return test_x @ beta


def _residual_reduction(validation, test, design_fn, target):
    v_x_raw = design_fn(validation)
    t_x_raw = design_fn(test)
    v_x, t_x = _standardize(v_x_raw, t_x_raw)
    v_y = np.array([r[target] for r in validation])
    t_y = np.array([r[target] for r in test])

    baseline_pred = np.full(len(t_y), v_y.mean())
    model_pred = _fit_predict(v_x, v_y, t_x)
    baseline_rmse = float(np.sqrt(np.mean((t_y - baseline_pred) ** 2)))
    model_rmse = float(np.sqrt(np.mean((t_y - model_pred) ** 2)))
    reduction = 1.0 - model_rmse / baseline_rmse if baseline_rmse > 1e-12 else 0.0
    return {
        "target": target,
        "baseline_rmse_deg": baseline_rmse,
        "model_rmse_deg": model_rmse,
        "residual_reduction": float(reduction),
    }


def diagnose_B(validation, test):
    """oracle 상한: 참기하가 계통 편향을 얼마나 설명하는가."""
    return {t: _residual_reduction(validation, test, _geometry_design, t) for t in TARGETS}


def diagnose_C(validation, test):
    """blind 식별성: 관측 feature가 계통 편향을 얼마나 설명하는가 + feature별 Spearman."""
    result = {t: _residual_reduction(validation, test, _signal_design, t) for t in TARGETS}
    correlations = {}
    for name in SIGNAL_FEATURES:
        values = np.array([r["features"][name] for r in test])
        per_target = {}
        for t in TARGETS:
            rho, p = spearmanr(values, [r[t] for r in test])
            per_target[t] = {"spearman_rho": float(rho), "spearman_p": float(p)}
        correlations[name] = per_target
    result["feature_correlations"] = correlations
    return result
