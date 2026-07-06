"""44번: 채택한 조건부 adaptive-R 라우팅이 라우팅 없는 UKF 대비 개선하는지 ablation.

제안법(19·22번)은 GCC-SRP 불일치가 작으면 DOA R를, 크면 TDOA R를 키우고 블록 NIS로 soft
gating한다. 같은 UKF·같은 base R·같은 test 궤적에서 라우팅 유무만 바꿔 위치 RMSE·일관성
(NEES/NIS)·발산을 비교해 제안법의 순수 이득을 정량화한다. test로 튜닝하지 않는다.
"""

from pathlib import Path
import json
import numpy as np

from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from consistency import nees, nis, summarize_consistency
from measurement import fixed_measurement_covariance, initialize_position
from trajectory import DISTANCES, STEPS, collect_trajectory
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 16
ROUTING_THRESHOLD_DEG = 5.0
INIT_COV = np.diag([8.0**2] * 3 + [1.5**2] * 3)


def _make_ukf(obs0, cfg):
    initial = initialize_position(obs0, cfg)
    ukf = SignalObservationUKF(np.r_[initial, np.zeros(3)], INIT_COV.copy(),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    return ukf, initial


def _run_plain(record, cfg):
    obs = record["observations"]; truth = record["truth"]
    ukf, initial = _make_ukf(obs[0], cfg)
    estimate = np.zeros((STEPS, 3)); estimate[0] = initial
    nv, iv = [], []; diverged = False
    for k in range(1, STEPS):
        try:
            ukf.predict()
            _, _, mean, _, S = ukf.measurement_statistics()
            innovation = ukf._z_residual(obs[k].copy(), mean)
            ukf.update(obs[k])
            estimate[k] = ukf.x[:3]
            nv.append(nees(ukf.x[:3], truth[k], ukf.P[:3, :3])); iv.append(nis(innovation, S))
        except Exception:
            diverged = True; estimate[k] = estimate[k - 1]
    return estimate, nv, iv, diverged


def _run_routing(record, cfg):
    obs = record["observations"]; truth = record["truth"]
    ukf, initial = _make_ukf(obs[0], cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    estimate = np.zeros((STEPS, 3)); estimate[0] = initial
    nv, iv = [], []; diverged = False
    for k in range(1, STEPS):
        try:
            wrapper.step(obs[k], record["qualities"][k])
            estimate[k] = ukf.x[:3]
            nv.append(nees(ukf.x[:3], truth[k], ukf.P[:3, :3]))
            iv.append(wrapper.history[-1]["nis"])
        except Exception:
            diverged = True; estimate[k] = estimate[k - 1]
    routed_rate = float(np.mean([h["routed"] for h in wrapper.history])) if wrapper.history else 0.0
    return estimate, nv, iv, diverged, routed_rate


def _rmse_after(estimate, truth, start=3):
    error = np.linalg.norm(estimate - truth, axis=1)
    return float(np.sqrt(np.mean(error[start:] ** 2))), bool(np.any(error > 50))


def evaluate(test_records):
    cfg = ChannelConfig()
    rows = []
    for rec in test_records:
        p_est, p_nv, p_iv, p_div = _run_plain(rec, cfg)
        r_est, r_nv, r_iv, r_div, routed = _run_routing(rec, cfg)
        p_rmse, p_d50 = _rmse_after(p_est, rec["truth"])
        r_rmse, r_d50 = _rmse_after(r_est, rec["truth"])
        pc = summarize_consistency(p_nv, p_iv); rc = summarize_consistency(r_nv, r_iv)
        rows.append({"distance": rec["distance"], "trial": rec["trial"],
                     "plain_rmse_m": p_rmse, "routing_rmse_m": r_rmse,
                     "plain_div50": p_d50 or p_div, "routing_div50": r_d50 or r_div,
                     "plain_nees": pc["mean_nees"], "routing_nees": rc["mean_nees"],
                     "plain_nis": pc["mean_nis"], "routing_nis": rc["mean_nis"],
                     "routed_rate": routed})
    return rows


def summarize(rows):
    out = {}
    for distance in list(DISTANCES) + ["overall"]:
        sub = rows if distance == "overall" else [r for r in rows if r["distance"] == distance]
        p = np.array([r["plain_rmse_m"] for r in sub]); r = np.array([r["routing_rmse_m"] for r in sub])
        diff = p - r
        out[str(distance)] = {
            "plain_mean_rmse_m": float(np.mean(p)), "routing_mean_rmse_m": float(np.mean(r)),
            "mean_improvement_m": float(np.mean(diff)), "improved_fraction": float(np.mean(diff > 0)),
            "plain_div50_rate": float(np.mean([x["plain_div50"] for x in sub])),
            "routing_div50_rate": float(np.mean([x["routing_div50"] for x in sub])),
            "plain_mean_nees": float(np.nanmean([x["plain_nees"] for x in sub])),
            "routing_mean_nees": float(np.nanmean([x["routing_nees"] for x in sub])),
            "plain_mean_nis": float(np.nanmean([x["plain_nis"] for x in sub])),
            "routing_mean_nis": float(np.nanmean([x["routing_nis"] for x in sub])),
            "mean_routed_rate": float(np.mean([x["routed_rate"] for x in sub])),
            "n": len(sub),
        }
    return out


def run():
    test = [collect_trajectory(d, t, "test") for d in DISTANCES for t in range(TRIALS)]
    rows = evaluate(test)
    payload = {
        "config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                   "steps": STEPS, "routing_threshold_deg": ROUTING_THRESHOLD_DEG,
                   "note": "라우팅 없는 UKF vs 조건부 adaptive-R 라우팅 UKF, 동일 base R·궤적"},
        "summary": summarize(rows), "trials": rows,
    }
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "routing_ablation.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                               encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": payload["summary"]},
                     indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
