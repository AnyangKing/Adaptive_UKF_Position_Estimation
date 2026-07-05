"""물리/기존 feature의 관측오차 예측력을 AUC·Spearman·일반화로 진단한다.

원칙: Ground Truth는 오차 label 산출에만 쓴다. validation에서 최선 feature와 문턱을 고르고
독립 test에 고정 적용해 일반화 여부를 본다. test 결과로 feature나 문턱을 재선택하지 않는다.
"""

from pathlib import Path
import json
import numpy as np
from scipy.stats import rankdata, spearmanr

from feature_diagnostic import FEATURE_NAMES, measure_scene

DISTANCES = (100, 200, 400, 600)
COUNT = 60                 # 거리당 독립 장면 수
PRIOR_STDS = (0.0, 5.0)    # 0 m = feature 정보 상한, 5 m = 수렴 후 현실 조건
BAD_QUANTILE = 0.75        # 상위 25% DOA 오차를 이상 관측 label로 (데이터 기반)
REFERENCE_DEG = 5.0        # 참고용 절대 기준 (라우팅 문턱과 동일)


def bad_label(doa_error):
    """상위 (1-BAD_QUANTILE) 분위 DOA 오차를 이상 관측(label=1)으로 정의한다."""
    doa_error = np.asarray(doa_error, dtype=float)
    threshold = float(np.quantile(doa_error, BAD_QUANTILE))
    return (doa_error > threshold).astype(int)


def roc_auc(values, labels):
    """값이 클수록 label=1(나쁨)일 확률. tie는 평균순위로 처리."""
    values = np.asarray(values, dtype=float)
    labels = np.asarray(labels, dtype=int)
    positive = int(np.sum(labels == 1))
    negative = int(np.sum(labels == 0))
    if positive == 0 or negative == 0:
        return float("nan")
    ranks = rankdata(values)
    auc = (np.sum(ranks[labels == 1]) - positive * (positive + 1) / 2.0) / (positive * negative)
    return float(auc)


def collect(split):
    """(prior_std, feature) 별 값과 거리·오차·label을 모은다."""
    rows = {std: {"distance": [], "doa_error_deg": [], "toa_error_m": [], "tdoa_error_m": [],
                  "features": {name: [] for name in FEATURE_NAMES}} for std in PRIOR_STDS}
    for distance in DISTANCES:
        for index in range(COUNT):
            measured = measure_scene(distance, index, split, PRIOR_STDS)
            for std in PRIOR_STDS:
                entry = measured[std]
                rows[std]["distance"].append(distance)
                for key in ("doa_error_deg", "toa_error_m", "tdoa_error_m"):
                    rows[std][key].append(entry["errors"][key])
                for name in FEATURE_NAMES:
                    rows[std]["features"][name].append(entry["features"][name])
    return rows


def summarize(rows):
    """prior_std별 feature 예측력: 전체 AUC, Spearman, 거리별 AUC."""
    summary = {}
    for std in PRIOR_STDS:
        data = rows[std]
        distance = np.asarray(data["distance"])
        doa_error = np.asarray(data["doa_error_deg"])
        label = bad_label(doa_error)
        feature_summary = {}
        for name in FEATURE_NAMES:
            values = np.asarray(data["features"][name])
            per_distance = {}
            for d in DISTANCES:
                mask = distance == d
                per_distance[str(d)] = roc_auc(values[mask], label[mask])
            rho, pvalue = spearmanr(values, doa_error)
            feature_summary[name] = {
                "auc_overall": roc_auc(values, label),
                "spearman_rho_vs_doa_error": float(rho),
                "spearman_p": float(pvalue),
                "auc_by_distance": per_distance,
            }
        summary[str(std)] = {
            "bad_label_rate": float(np.mean(label)),
            "abs_over_5deg_rate": float(np.mean(doa_error > REFERENCE_DEG)),
            "median_doa_error_deg": float(np.median(doa_error)),
            "p90_doa_error_deg": float(np.percentile(doa_error, 90)),
            "features": feature_summary,
        }
    return summary


def generalization(validation_rows, test_rows, std):
    """validation에서 최고 AUC feature와 Youden 문턱을 골라 test 정밀도/재현율 측정."""
    v = validation_rows[std]
    v_label = bad_label(v["doa_error_deg"])
    best_name, best_auc = None, -1.0
    for name in FEATURE_NAMES:
        auc = roc_auc(v["features"][name], v_label)
        if np.isfinite(auc) and auc > best_auc:
            best_name, best_auc = name, auc

    values = np.asarray(v["features"][best_name])
    order = np.unique(values)
    best_threshold, best_j = order[0], -1.0
    for threshold in order:
        predicted = (values >= threshold).astype(int)
        tp = int(np.sum((predicted == 1) & (v_label == 1)))
        fn = int(np.sum((predicted == 0) & (v_label == 1)))
        fp = int(np.sum((predicted == 1) & (v_label == 0)))
        tn = int(np.sum((predicted == 0) & (v_label == 0)))
        tpr = tp / max(tp + fn, 1)
        fpr = fp / max(fp + tn, 1)
        if tpr - fpr > best_j:
            best_j, best_threshold = tpr - fpr, float(threshold)

    t = test_rows[std]
    t_label = bad_label(t["doa_error_deg"])
    t_values = np.asarray(t["features"][best_name])
    predicted = (t_values >= best_threshold).astype(int)
    tp = int(np.sum((predicted == 1) & (t_label == 1)))
    fp = int(np.sum((predicted == 1) & (t_label == 0)))
    fn = int(np.sum((predicted == 0) & (t_label == 1)))
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-12)
    return {
        "selected_feature": best_name,
        "validation_auc": float(best_auc),
        "validation_threshold": best_threshold,
        "test_auc": roc_auc(t_values, t_label),
        "test_precision": float(precision),
        "test_recall": float(recall),
        "test_f1": float(f1),
        "test_bad_ping_rate": float(np.mean(t_label)),
    }


def run():
    validation_rows = collect("validation")
    test_rows = collect("test")
    payload = {
        "config": {"count_per_distance": COUNT, "prior_stds_m": list(PRIOR_STDS),
                   "bad_quantile": BAD_QUANTILE, "reference_deg": REFERENCE_DEG,
                   "distances_m": list(DISTANCES)},
        "validation": summarize(validation_rows),
        "test": summarize(test_rows),
        "generalization": {str(std): generalization(validation_rows, test_rows, std)
                           for std in PRIOR_STDS},
    }
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    (output / "feature_predictiveness.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return payload


if __name__ == "__main__":
    run()
