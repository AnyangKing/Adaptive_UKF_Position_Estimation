"""40번 ablation: 거리적응 고도각 편향 보정이 39번 global의 중거리 악화를 없애면서 장거리
이득을 유지하는지 판정한다.

절차 (데이터 분리 엄수): validation 궤적에서만 global/gated/interaction 계수를 각각 적합해
고정하고, 독립 test 궤적에서 baseline과 세 보정을 같은 관측·초기화·라우팅으로 돌려 거리별
위치 RMSE를 비교한다. test로 계수·모델을 재선택하지 않는다.
"""

from pathlib import Path
import json
import numpy as np

from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from correction_models import FITTERS, corrected_observations
from measurement import fixed_measurement_covariance, initialize_position
from trajectory import DISTANCES, STEPS, collect_trajectory
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 16           # 거리당 궤적 (39번 8→16으로 확대)
ROUTING_THRESHOLD_DEG = 5.0
MODELS = ("global", "gated", "interaction")


def _run_filter(observations, qualities, cfg):
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
            diverged = True; estimate[k] = estimate[k - 1]
    return estimate, diverged


def _rmse_after(estimate, truth, start=3):
    error = np.linalg.norm(estimate - truth, axis=1)
    return float(np.sqrt(np.mean(error[start:] ** 2))), bool(np.any(error > 50))


def evaluate(test_records, corrections):
    cfg = ChannelConfig()
    rows = []
    for rec in test_records:
        truth = rec["truth"]
        base_est, base_div = _run_filter(rec["observations"], rec["qualities"], cfg)
        base_rmse, base_div50 = _rmse_after(base_est, truth)
        entry = {"distance": rec["distance"], "trial": rec["trial"],
                 "baseline_rmse_m": base_rmse, "baseline_div50": base_div50 or base_div}
        for name in MODELS:
            est, div = _run_filter(corrected_observations(rec, corrections[name]),
                                   rec["qualities"], cfg)
            rmse, div50 = _rmse_after(est, truth)
            entry[f"{name}_rmse_m"] = rmse
            entry[f"{name}_div50"] = div50 or div
        rows.append(entry)
    return rows


def summarize(rows):
    out = {}
    for distance in list(DISTANCES) + ["overall"]:
        sub = rows if distance == "overall" else [r for r in rows if r["distance"] == distance]
        base = np.array([r["baseline_rmse_m"] for r in sub])
        cell = {"baseline_mean_rmse_m": float(np.mean(base)),
                "baseline_div50_rate": float(np.mean([r["baseline_div50"] for r in sub])),
                "n": len(sub)}
        for name in MODELS:
            corr = np.array([r[f"{name}_rmse_m"] for r in sub])
            diff = base - corr
            cell[name] = {
                "mean_rmse_m": float(np.mean(corr)),
                "mean_improvement_m": float(np.mean(diff)),
                "improved_fraction": float(np.mean(diff > 0)),
                "div50_rate": float(np.mean([r[f"{name}_div50"] for r in sub])),
            }
        out[str(distance)] = cell
    return out


def run():
    validation = [collect_trajectory(d, t, "validation")
                  for d in DISTANCES for t in range(TRIALS)]
    corrections = {name: FITTERS[name](validation) for name in MODELS}
    test = [collect_trajectory(d, t, "test") for d in DISTANCES for t in range(TRIALS)]
    rows = evaluate(test, corrections)
    payload = {
        "config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                   "steps": STEPS, "routing_threshold_deg": ROUTING_THRESHOLD_DEG,
                   "models": list(MODELS), "max_correction_deg": 3.0,
                   "note": "관측 TOA 거리로 39 global 보정을 거리적응화 (gated/interaction)"},
        "corrections": corrections,
        "summary": summarize(rows),
        "trials": rows,
    }
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / "ablation.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                       encoding="utf-8")
    print(json.dumps({"corrections": corrections, "summary": payload["summary"]},
                     indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
