"""37번 C의 고도각 편향 blind 식별을 대규모에서 재현·통계검정한다.

핵심 질문: 관측 신호 feature로 고도각 계통 편향(el_bias)을 예측하면 out-of-sample 잔차가
재현적으로 줄어드는가? 한 번의 우연한 split이 아니라 K개의 무작위 val/test split 분포로 본다.

- 사전등록(pre-registration): target=el_bias, 예측자=3개 gated 신호 feature, 모델=ridge,
  지표=test 잔차감소(1 - model_rmse/baseline_rmse). test로 feature나 모델을 재선택하지 않는다.
- az_bias와 전체 bias는 음성 대조군. 37번대로라면 el_bias만 유의하고 이들은 아니어야 한다.
- feature별 Spearman은 전체 pool에서 부트스트랩 CI로 재현 강도를 본다.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import spearmanr

from bias_features import SIGNAL_FEATURES, DISTANCES

TARGETS = ("el_bias_deg", "az_bias_deg", "bias_angle_deg")
N_SPLITS = 200
TEST_FRACTION = 0.5
N_BOOTSTRAP = 2000
RIDGE = 1e-2


def _design(records):
    rows = [[1.0] + [r["features"][name] for name in SIGNAL_FEATURES] for r in records]
    return np.asarray(rows)


def _standardize(train, test):
    mean = train.mean(axis=0); std = train.std(axis=0)
    mean[0] = 0.0; std[0] = 1.0; std[std < 1e-12] = 1.0
    return (train - mean) / std, (test - mean) / std


def _fit_predict(tx, ty, ex):
    beta = np.linalg.solve(tx.T @ tx + RIDGE * np.eye(tx.shape[1]), tx.T @ ty)
    return ex @ beta


def repeated_split_reduction(records, target, seed=3800):
    """K개 무작위 val/test split에서 out-of-sample 잔차감소 분포를 낸다."""
    rng = np.random.default_rng(seed)
    x_all = _design(records)
    y_all = np.array([r[target] for r in records])
    n = len(records); n_test = int(round(n * TEST_FRACTION))
    reductions = []
    for _ in range(N_SPLITS):
        perm = rng.permutation(n)
        test_idx, train_idx = perm[:n_test], perm[n_test:]
        tx, ex = _standardize(x_all[train_idx], x_all[test_idx])
        ty, ey = y_all[train_idx], y_all[test_idx]
        pred = _fit_predict(tx, ty, ex)
        base_rmse = np.sqrt(np.mean((ey - ty.mean()) ** 2))
        model_rmse = np.sqrt(np.mean((ey - pred) ** 2))
        reductions.append(1.0 - model_rmse / base_rmse if base_rmse > 1e-12 else 0.0)
    reductions = np.asarray(reductions)
    return {
        "target": target,
        "median_reduction": float(np.median(reductions)),
        "reduction_ci90": [float(np.percentile(reductions, 5)),
                           float(np.percentile(reductions, 95))],
        "prob_reduction_positive": float(np.mean(reductions > 0.0)),
    }


def bootstrap_spearman(values, target_values, seed=3801):
    rng = np.random.default_rng(seed)
    values = np.asarray(values); target_values = np.asarray(target_values)
    rho, p = spearmanr(values, target_values)
    n = len(values); samples = []
    for _ in range(N_BOOTSTRAP):
        idx = rng.integers(0, n, n)
        r, _ = spearmanr(values[idx], target_values[idx])
        if np.isfinite(r):
            samples.append(r)
    samples = np.asarray(samples)
    return {
        "rho": float(rho), "p": float(p),
        "ci95": [float(np.percentile(samples, 2.5)), float(np.percentile(samples, 97.5))],
    }


def feature_correlations(records, target):
    y = [r[target] for r in records]
    return {name: bootstrap_spearman([r["features"][name] for r in records], y)
            for name in SIGNAL_FEATURES}


def per_distance_el_spearman(records):
    """고도각 편향 신호가 어느 거리에 사는지 (feature별 거리별 Spearman)."""
    out = {}
    for d in DISTANCES:
        rows = [r for r in records if r["distance"] == d]
        y = [r["el_bias_deg"] for r in rows]
        out[str(d)] = {name: {"rho": float(spearmanr([r["features"][name] for r in rows], y)[0]),
                              "p": float(spearmanr([r["features"][name] for r in rows], y)[1])}
                       for name in SIGNAL_FEATURES}
    return out


def analyze(records):
    return {
        "n_geometries": len(records),
        "reduction": {t: repeated_split_reduction(records, t) for t in TARGETS},
        "el_bias_feature_spearman": feature_correlations(records, "el_bias_deg"),
        "az_bias_feature_spearman": feature_correlations(records, "az_bias_deg"),
        "el_bias_spearman_by_distance": per_distance_el_spearman(records),
    }
