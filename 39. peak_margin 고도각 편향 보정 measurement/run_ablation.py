"""39번 ablation: peak_margin 고도각 편향 보정이 위치 RMSE를 줄이는지 판정한다.

절차 (데이터 분리 엄수):
1. validation 궤적에서만 el_bias ≈ a + b·peak_margin 계수를 적합하고 고정한다.
2. 독립 test 궤적에서 baseline(보정 없음)과 corrected(z[9] 보정) 필터를 같은 관측·같은
   초기화로 각각 돌려 위치 RMSE를 비교한다. test로 계수를 재조정하지 않는다.
3. 필터·초기화·라우팅은 baseline과 corrected가 동일하고 관측 고도각만 다르다.
"""

from pathlib import Path
import json
import numpy as np

from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from elevation_correction import fit_correction, corrected_observations
from measurement import fixed_measurement_covariance, initialize_position
from trajectory import DISTANCES, STEPS, collect_trajectory
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 8            # 거리당 궤적 수 (validation/test 각각)
ROUTING_THRESHOLD_DEG = 5.0


def _run_filter(observations, qualities, cfg):
    """채택 구성(조건부 adaptive-R UKF)으로 궤적을 추정한다."""
    initial = initialize_position(observations[0], cfg)
    wrapper = ConditionalAdaptiveRUKF(
        SignalObservationUKF(np.r_[initial, np.zeros(3)],
                             np.diag([8.0**2] * 3 + [1.5**2] * 3),
                             acceleration_process_covariance(1.0, 0.20),
                             fixed_measurement_covariance(), cfg),
        ROUTING_THRESHOLD_DEG)
    estimate = np.zeros((STEPS, 3)); estimate[0] = initial
    diverged = False
    for k in range(1, STEPS):
        try:
            estimate[k] = wrapper.step(observations[k], qualities[k])[:3]
        except Exception:
            diverged = True
            estimate[k] = estimate[k - 1]
    return estimate, diverged


def _rmse_after(estimate, truth, start=3):
    error = np.linalg.norm(estimate - truth, axis=1)
    return float(np.sqrt(np.mean(error[start:] ** 2))), bool(np.any(error > 50))


def evaluate(test_records, correction):
    cfg = ChannelConfig()
    rows = []
    for rec in test_records:
        truth = rec["truth"]
        base_est, base_div = _run_filter(rec["observations"], rec["qualities"], cfg)
        corr_obs = corrected_observations(rec, correction)
        corr_est, corr_div = _run_filter(corr_obs, rec["qualities"], cfg)
        base_rmse, base_div50 = _rmse_after(base_est, truth)
        corr_rmse, corr_div50 = _rmse_after(corr_est, truth)
        rows.append({"distance": rec["distance"], "trial": rec["trial"],
                     "baseline_rmse_m": base_rmse, "corrected_rmse_m": corr_rmse,
                     "baseline_div50": base_div50 or base_div,
                     "corrected_div50": corr_div50 or corr_div})
    return rows


def summarize(rows):
    out = {}
    for distance in DISTANCES:
        sub = [r for r in rows if r["distance"] == distance]
        base = np.array([r["baseline_rmse_m"] for r in sub])
        corr = np.array([r["corrected_rmse_m"] for r in sub])
        diff = base - corr  # 양수면 보정이 개선
        out[str(distance)] = {
            "baseline_mean_rmse_m": float(np.mean(base)),
            "corrected_mean_rmse_m": float(np.mean(corr)),
            "mean_improvement_m": float(np.mean(diff)),
            "median_improvement_m": float(np.median(diff)),
            "improved_fraction": float(np.mean(diff > 0)),
            "baseline_div50_rate": float(np.mean([r["baseline_div50"] for r in sub])),
            "corrected_div50_rate": float(np.mean([r["corrected_div50"] for r in sub])),
            "n": len(sub),
        }
    all_base = np.array([r["baseline_rmse_m"] for r in rows])
    all_corr = np.array([r["corrected_rmse_m"] for r in rows])
    out["overall"] = {
        "baseline_mean_rmse_m": float(np.mean(all_base)),
        "corrected_mean_rmse_m": float(np.mean(all_corr)),
        "mean_improvement_m": float(np.mean(all_base - all_corr)),
        "improved_fraction": float(np.mean((all_base - all_corr) > 0)),
    }
    return out


def run():
    validation = [collect_trajectory(d, t, "validation")
                  for d in DISTANCES for t in range(TRIALS)]
    correction = fit_correction(validation)
    test = [collect_trajectory(d, t, "test") for d in DISTANCES for t in range(TRIALS)]
    rows = evaluate(test, correction)
    payload = {
        "config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                   "steps": STEPS, "routing_threshold_deg": ROUTING_THRESHOLD_DEG,
                   "max_correction_deg": 3.0,
                   "note": "38번 peak_margin 예측자를 고도각 관측 보정으로 넣어 위치 RMSE ablation"},
        "correction_fit": correction,
        "summary": summarize(rows),
        "trials": rows,
    }
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / "ablation.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                       encoding="utf-8")
    print(json.dumps({"correction_fit": correction, "summary": payload["summary"]},
                     indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
