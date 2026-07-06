"""41번 ablation: 고도각 R 팽창이 baseline 대비 위치 RMSE를 개선하고 발산 없이 안전한지 판정.

절차 (데이터 분리 엄수):
1. validation 궤적에서만 el_bias ≈ a + b·peak_margin을 적합한다.
2. validation 궤적에서 R 팽창 gain을 사전 grid {0.5,1,2,4}에서 평균 RMSE 최소로 하나 고른다
   (gain 선택도 validation에서만). test로는 재선택하지 않는다.
3. 독립 test 궤적에서 baseline과 선택 gain의 R 팽창을 같은 관측·초기화·라우팅으로 돌려 거리별
   위치 RMSE와 발산율을 비교한다.
"""

from pathlib import Path
import json
import numpy as np

from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from r_adjust import ElevationRInflateUKF, fit_bias_model
from trajectory import DISTANCES, STEPS, collect_trajectory
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 16
ROUTING_THRESHOLD_DEG = 5.0
GAIN_GRID = (0.0, 0.5, 1.0, 2.0, 4.0)   # 0.0 = baseline


def _make_wrapper(observations, cfg, bias_model, gain):
    initial = initialize_position(observations[0], cfg)
    ukf = SignalObservationUKF(np.r_[initial, np.zeros(3)],
                               np.diag([8.0**2] * 3 + [1.5**2] * 3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    return ElevationRInflateUKF(ukf, ROUTING_THRESHOLD_DEG, bias_model, gain), initial


def _run(record, cfg, bias_model, gain):
    obs = record["observations"]
    wrapper, initial = _make_wrapper(obs, cfg, bias_model, gain)
    estimate = np.zeros((STEPS, 3)); estimate[0] = initial
    diverged = False
    for k in range(1, STEPS):
        try:
            estimate[k] = wrapper.step(obs[k], record["qualities"][k])[:3]
        except Exception:
            diverged = True; estimate[k] = estimate[k - 1]
    error = np.linalg.norm(estimate - record["truth"], axis=1)
    return float(np.sqrt(np.mean(error[3:] ** 2))), bool(diverged or np.any(error > 50))


def _mean_rmse(records, cfg, bias_model, gain):
    return float(np.mean([_run(r, cfg, bias_model, gain)[0] for r in records]))


def run():
    cfg = ChannelConfig()
    validation = [collect_trajectory(d, t, "validation")
                  for d in DISTANCES for t in range(TRIALS)]
    bias_model = fit_bias_model(validation)

    # gain 선택은 validation 평균 RMSE로만 한다.
    val_rmse = {g: _mean_rmse(validation, cfg, bias_model, g) for g in GAIN_GRID}
    selected_gain = min(GAIN_GRID, key=lambda g: val_rmse[g])

    test = [collect_trajectory(d, t, "test") for d in DISTANCES for t in range(TRIALS)]
    rows = []
    for rec in test:
        base_rmse, base_div = _run(rec, cfg, bias_model, 0.0)
        adj_rmse, adj_div = _run(rec, cfg, bias_model, selected_gain)
        rows.append({"distance": rec["distance"], "trial": rec["trial"],
                     "baseline_rmse_m": base_rmse, "adjusted_rmse_m": adj_rmse,
                     "baseline_div50": base_div, "adjusted_div50": adj_div})

    summary = {}
    for distance in list(DISTANCES) + ["overall"]:
        sub = rows if distance == "overall" else [r for r in rows if r["distance"] == distance]
        base = np.array([r["baseline_rmse_m"] for r in sub])
        adj = np.array([r["adjusted_rmse_m"] for r in sub])
        diff = base - adj
        summary[str(distance)] = {
            "baseline_mean_rmse_m": float(np.mean(base)),
            "adjusted_mean_rmse_m": float(np.mean(adj)),
            "mean_improvement_m": float(np.mean(diff)),
            "improved_fraction": float(np.mean(diff > 0)),
            "baseline_div50_rate": float(np.mean([r["baseline_div50"] for r in sub])),
            "adjusted_div50_rate": float(np.mean([r["adjusted_div50"] for r in sub])),
            "n": len(sub),
        }

    payload = {
        "config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                   "steps": STEPS, "routing_threshold_deg": ROUTING_THRESHOLD_DEG,
                   "gain_grid": list(GAIN_GRID), "max_add_deg": 4.0,
                   "note": "peak_margin 예측 고도각 편향을 R 팽창(분산 추가)으로 완화, 차감(39/40) 대안"},
        "bias_model": bias_model,
        "validation_rmse_by_gain": val_rmse,
        "selected_gain": selected_gain,
        "summary": summary,
        "trials": rows,
    }
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / "ablation.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                       encoding="utf-8")
    print(json.dumps({"bias_model": bias_model, "validation_rmse_by_gain": val_rmse,
                      "selected_gain": selected_gain, "summary": summary},
                     indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
