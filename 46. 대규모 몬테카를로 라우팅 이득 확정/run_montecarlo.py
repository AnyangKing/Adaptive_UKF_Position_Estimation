"""46번: 대규모 Monte Carlo로 라우팅 이득(44번)을 통계적으로 확정한다.

44번은 거리당 16개로 라우팅이 plain UKF 대비 RMSE를 낮춤을 보였다. 여기서는 거리당 40개
(총 160)로 늘리고 궤적별 paired 개선(plain-routing)에 부트스트랩 95% CI와 Wilcoxon signed-rank를
적용해, 개선이 소표본 우연이 아님을 확정한다. 같은 UKF·base R·궤적, 라우팅 유무만 다르다.
"""

from pathlib import Path
import json
import numpy as np
from scipy.stats import wilcoxon

from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from consistency import nees, nis, summarize_consistency
from measurement import fixed_measurement_covariance, initialize_position
from trajectory import DISTANCES, STEPS, collect_trajectory
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 40
ROUTING_THRESHOLD_DEG = 5.0
INIT_COV = np.diag([8.0**2] * 3 + [1.5**2] * 3)
N_BOOTSTRAP = 5000


def _make_ukf(obs0, cfg):
    initial = initialize_position(obs0, cfg)
    return SignalObservationUKF(np.r_[initial, np.zeros(3)], INIT_COV.copy(),
                                acceleration_process_covariance(1.0, 0.20),
                                fixed_measurement_covariance(), cfg), initial


def _run(record, cfg, routing):
    obs = record["observations"]; truth = record["truth"]
    ukf, initial = _make_ukf(obs[0], cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG) if routing else None
    est = np.zeros((STEPS, 3)); est[0] = initial
    nv, iv = [], []; diverged = False
    for k in range(1, STEPS):
        try:
            if routing:
                wrapper.step(obs[k], record["qualities"][k]); S_nis = wrapper.history[-1]["nis"]
            else:
                ukf.predict()
                _, _, mean, _, S = ukf.measurement_statistics()
                innovation = ukf._z_residual(obs[k].copy(), mean)
                ukf.update(obs[k]); S_nis = nis(innovation, S)
            est[k] = ukf.x[:3]
            nv.append(nees(ukf.x[:3], truth[k], ukf.P[:3, :3])); iv.append(S_nis)
        except Exception:
            diverged = True; est[k] = est[k - 1]
    err = np.linalg.norm(est[3:] - truth[3:], axis=1)
    rmse = float(np.sqrt(np.mean(err ** 2)))
    return rmse, bool(diverged or np.any(np.linalg.norm(est - truth, axis=1) > 50)), \
        summarize_consistency(nv, iv)


def _bootstrap_ci(diffs, seed=460):
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(diffs, len(diffs), replace=True)) for _ in range(N_BOOTSTRAP)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def run():
    cfg = ChannelConfig()
    test = [collect_trajectory(d, t, "test") for d in DISTANCES for t in range(TRIALS)]
    rows = []
    for rec in test:
        p_rmse, p_div, p_c = _run(rec, cfg, routing=False)
        r_rmse, r_div, r_c = _run(rec, cfg, routing=True)
        rows.append({"distance": rec["distance"], "plain_rmse_m": p_rmse, "routing_rmse_m": r_rmse,
                     "improvement_m": p_rmse - r_rmse, "plain_div": p_div, "routing_div": r_div,
                     "plain_nees": p_c["mean_nees"], "routing_nees": r_c["mean_nees"]})
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
            "plain_mean_rmse_m": float(np.mean([r["plain_rmse_m"] for r in sub])),
            "routing_mean_rmse_m": float(np.mean([r["routing_rmse_m"] for r in sub])),
            "mean_improvement_m": float(np.mean(diffs)),
            "improvement_ci95": [lo, hi],
            "wilcoxon_greater_p": w_p,
            "improved_fraction": float(np.mean(diffs > 0)),
            "plain_div50_rate": float(np.mean([r["plain_div"] for r in sub])),
            "routing_div50_rate": float(np.mean([r["routing_div"] for r in sub])),
            "plain_mean_nees": float(np.nanmean([r["plain_nees"] for r in sub])),
            "routing_mean_nees": float(np.nanmean([r["routing_nees"] for r in sub])),
            "n": len(sub),
        }
    payload = {"config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                          "steps": STEPS, "n_bootstrap": N_BOOTSTRAP,
                          "note": "160궤적 paired plain vs routing, 부트스트랩 CI+Wilcoxon로 이득 확정"},
               "summary": summary, "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "montecarlo.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                         encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
