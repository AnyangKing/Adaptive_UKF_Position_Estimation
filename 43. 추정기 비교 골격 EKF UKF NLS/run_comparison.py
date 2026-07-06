"""43번: 동일 조건에서 EKF·UKF·NLS의 위치 RMSE·일관성(NEES/NIS)·계산량을 비교한다.

세 추정기는 같은 관측모델(TOA/TDOA/DOA)·같은 고정 R·같은 CV 동력학(NLS는 동력학 없음)을 쓴다.
adaptive-R 라우팅 같은 개선은 넣지 않아 필터 메커니즘 자체를 공정 비교한다(라우팅 이득은 별도).
독립 test 궤적에서만 평가하며 튜닝하지 않는다.
"""

from pathlib import Path
from time import perf_counter
import json
import numpy as np

from config import ChannelConfig
from consistency import nees, nis, summarize_consistency
from ekf import ExtendedKalmanFilter
from measurement import fixed_measurement_covariance, initialize_position
from nls import solve_position
from trajectory import DISTANCES, STEPS, collect_trajectory
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 16
INIT_COV = np.diag([8.0**2] * 3 + [1.5**2] * 3)


def _run_recursive(kind, record, cfg):
    obs = record["observations"]; truth = record["truth"]
    R = fixed_measurement_covariance()
    initial = initialize_position(obs[0], cfg)
    state = np.r_[initial, np.zeros(3)]
    Q = acceleration_process_covariance(1.0, 0.20)
    if kind == "EKF":
        flt = ExtendedKalmanFilter(state, INIT_COV.copy(), Q, R, cfg)
    else:
        flt = SignalObservationUKF(state, INIT_COV.copy(), Q, R, cfg)
    estimate = np.zeros((STEPS, 3)); estimate[0] = initial
    nees_vals, nis_vals = [], []
    diverged = False; t0 = perf_counter()
    for k in range(1, STEPS):
        try:
            if kind == "EKF":
                flt.predict()
                innovation, S = flt.update(obs[k])
            else:
                flt.predict()
                _, _, mean, _, S = flt.measurement_statistics()
                innovation = flt._z_residual(obs[k].copy(), mean)
                flt.update(obs[k])
            estimate[k] = flt.x[:3]
            nees_vals.append(nees(flt.x[:3], truth[k], flt.P[:3, :3]))
            nis_vals.append(nis(innovation, S))
        except Exception:
            diverged = True; estimate[k] = estimate[k - 1]
    runtime_ms = (perf_counter() - t0) / (STEPS - 1) * 1000.0
    return estimate, nees_vals, nis_vals, diverged, runtime_ms


def _run_nls(record, cfg):
    obs = record["observations"]; truth = record["truth"]
    R = fixed_measurement_covariance()
    initial = initialize_position(obs[0], cfg)
    estimate = np.zeros((STEPS, 3)); estimate[0] = initial
    nees_vals = []; diverged = False; t0 = perf_counter()
    for k in range(1, STEPS):
        try:
            pos, cov = solve_position(obs[k], estimate[k - 1], cfg, R)
            estimate[k] = pos
            nees_vals.append(nees(pos, truth[k], cov))
        except Exception:
            diverged = True; estimate[k] = estimate[k - 1]
    runtime_ms = (perf_counter() - t0) / (STEPS - 1) * 1000.0
    return estimate, nees_vals, [], diverged, runtime_ms


def _rmse_after(estimate, truth, start=3):
    error = np.linalg.norm(estimate - truth, axis=1)
    return float(np.sqrt(np.mean(error[start:] ** 2))), bool(np.any(error > 50))


def evaluate(test_records):
    cfg = ChannelConfig()
    rows = []
    for rec in test_records:
        entry = {"distance": rec["distance"], "trial": rec["trial"]}
        for kind in ("NLS", "EKF", "UKF"):
            runner = _run_nls if kind == "NLS" else _run_recursive
            est, nv, iv, div, ms = (runner(rec, cfg) if kind == "NLS"
                                    else runner(kind, rec, cfg))
            rmse, div50 = _rmse_after(est, rec["truth"])
            cons = summarize_consistency(nv, iv)
            entry[kind] = {"rmse_m": rmse, "div50": div50 or div, "runtime_ms": ms,
                           "mean_nees": cons["mean_nees"], "mean_nis": cons["mean_nis"]}
        rows.append(entry)
    return rows


def summarize(rows):
    out = {}
    for distance in list(DISTANCES) + ["overall"]:
        sub = rows if distance == "overall" else [r for r in rows if r["distance"] == distance]
        cell = {"n": len(sub)}
        for kind in ("NLS", "EKF", "UKF"):
            rmse = np.array([r[kind]["rmse_m"] for r in sub])
            cell[kind] = {
                "mean_rmse_m": float(np.mean(rmse)),
                "median_rmse_m": float(np.median(rmse)),
                "div50_rate": float(np.mean([r[kind]["div50"] for r in sub])),
                "mean_runtime_ms": float(np.mean([r[kind]["runtime_ms"] for r in sub])),
                "mean_nees": float(np.nanmean([r[kind]["mean_nees"] for r in sub])),
                "mean_nis": float(np.nanmean([r[kind]["mean_nis"] for r in sub])),
            }
        out[str(distance)] = cell
    return out


def run():
    test = [collect_trajectory(d, t, "test") for d in DISTANCES for t in range(TRIALS)]
    rows = evaluate(test)
    payload = {
        "config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                   "steps": STEPS, "estimators": ["NLS", "EKF", "UKF"],
                   "nees_dof": 3, "nis_dof": 10,
                   "note": "동일 R·Q·관측모델, 라우팅 없음. 필터 메커니즘 공정 비교"},
        "summary": summarize(rows),
        "trials": rows,
    }
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / "comparison.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                         encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": payload["summary"]},
                     indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
