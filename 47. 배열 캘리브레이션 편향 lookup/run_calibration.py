"""47번: 배열 캘리브레이션(관측 도래각 색인 편향 lookup)이 위치 RMSE, 특히 600m bias floor를
회복하는지 판정한다.

validation 궤적에서만 lookup을 적합하고(GT는 편향 label에만), 독립 test 궤적에서 baseline 라우팅
UKF와 캘리브레이션(z[9]에서 예측 편향 차감) 라우팅 UKF를 같은 초기화·라우팅으로 비교한다. test로
lookup을 재적합하지 않는다.
"""

from pathlib import Path
import json
import numpy as np
from scipy.stats import wilcoxon

from calibration import ElevationBiasLookup, corrected_observations
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from consistency import nees
from measurement import fixed_measurement_covariance, initialize_position
from trajectory import DISTANCES, STEPS, collect_trajectory
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 40
ROUTING_THRESHOLD_DEG = 5.0
K_NEIGHBORS = 15


def _run_routing(observations, qualities, truth, cfg):
    initial = initialize_position(observations[0], cfg)
    ukf = SignalObservationUKF(np.r_[initial, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    est = np.zeros((STEPS, 3)); est[0] = initial; nv = []
    for k in range(1, STEPS):
        try:
            wrapper.step(observations[k], qualities[k]); est[k] = ukf.x[:3]
            nv.append(nees(ukf.x[:3], truth[k], ukf.P[:3, :3]))
        except Exception:
            est[k] = est[k-1]
    err = np.linalg.norm(est[3:] - truth[3:], axis=1)
    return float(np.sqrt(np.mean(err**2))), float(np.nanmean(nv)) if nv else float("nan")


def _bootstrap_ci(diffs, seed=470, n=5000):
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(diffs, len(diffs), replace=True)) for _ in range(n)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def run():
    cfg = ChannelConfig()
    validation = [collect_trajectory(d, t, "validation") for d in DISTANCES for t in range(TRIALS)]
    lookup = ElevationBiasLookup.fit(validation, cfg, k=K_NEIGHBORS)

    test = [collect_trajectory(d, t, "test") for d in DISTANCES for t in range(TRIALS)]
    rows = []
    for rec in test:
        base_rmse, base_nees = _run_routing(rec["observations"], rec["qualities"], rec["truth"], cfg)
        corr_obs = corrected_observations(rec, lookup)
        cal_rmse, cal_nees = _run_routing(corr_obs, rec["qualities"], rec["truth"], cfg)
        rows.append({"distance": rec["distance"], "baseline_rmse_m": base_rmse,
                     "calibrated_rmse_m": cal_rmse, "improvement_m": base_rmse - cal_rmse,
                     "baseline_nees": base_nees, "calibrated_nees": cal_nees})

    summary = {}
    for d in list(DISTANCES) + ["overall"]:
        sub = rows if d == "overall" else [r for r in rows if r["distance"] == d]
        diffs = np.array([r["improvement_m"] for r in sub])
        lo, hi = _bootstrap_ci(diffs)
        try:
            w_p = float(wilcoxon(diffs, alternative="greater").pvalue) if np.any(diffs != 0) else 1.0
        except ValueError:
            w_p = 1.0
        summary[str(d)] = {
            "baseline_mean_rmse_m": float(np.mean([r["baseline_rmse_m"] for r in sub])),
            "calibrated_mean_rmse_m": float(np.mean([r["calibrated_rmse_m"] for r in sub])),
            "mean_improvement_m": float(np.mean(diffs)), "improvement_ci95": [lo, hi],
            "wilcoxon_greater_p": w_p, "improved_fraction": float(np.mean(diffs > 0)),
            "baseline_mean_nees": float(np.nanmean([r["baseline_nees"] for r in sub])),
            "calibrated_mean_nees": float(np.nanmean([r["calibrated_nees"] for r in sub])),
            "n": len(sub),
        }
    payload = {"config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                          "steps": STEPS, "k_neighbors": K_NEIGHBORS,
                          "note": "관측 도래각 색인 편향 lookup(비모수 kNN) non-blind 보정 vs baseline"},
               "summary": summary, "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "calibration.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                          encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
