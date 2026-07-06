"""45번: CRLB 이론 하한 대비 추정기 효율과 계통 편향 floor를 정량화한다.

CRLB는 가정한 관측잡음 R에 의존한다. 채택 필터의 설계 R(DOA 2°)은 실제 SRP DOA 정확도
(37번 중앙값 ~0.9°)보다 보수적이라, 설계 R로 계산한 CRLB는 느슨해 실제 RMSE가 그보다 작아
보인다. 따라서 두 CRLB를 함께 보고한다:
  - CRLB(design R): 필터가 가정한 잡음 하한 (느슨).
  - CRLB(empirical R): test 잔차 z-h(참)의 실제 공분산(대각)로 계산한 현실적 하한.
실제 RMSE를 CRLB(empirical)과 비교해 효율을 보고, 그 초과분을 bias floor로 귀속한다. 경험적
잔차는 37~42의 array-intrinsic 계통 편향(기하마다 다른 상수)을 유효잡음으로 포함하므로,
CRLB(empirical) 자체가 이미 편향을 반영한 현실적 성취 한계다.
"""

from pathlib import Path
import json
import numpy as np

from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from crlb import position_crlb
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position
from nls import solve_position
from trajectory import DISTANCES, STEPS, collect_trajectory
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 16
ROUTING_THRESHOLD_DEG = 5.0
START = 3


def empirical_R(records, cfg):
    """test 잔차 z - h(참)의 대각 공분산. 관측 성분별 유효잡음(편향 포함)."""
    residuals = []
    for rec in records:
        for k in range(STEPS):
            r = rec["observations"][k] - ideal_measurement(rec["truth"][k], cfg)
            r[8:] = (r[8:] + np.pi) % (2 * np.pi) - np.pi
            residuals.append(r)
    residuals = np.asarray(residuals)
    return np.diag(np.var(residuals, axis=0) + 1e-12)


def _crlb_bound(record, cfg, R):
    bounds = [position_crlb(record["truth"][k], cfg, R)[1] for k in range(START, STEPS)]
    return float(np.sqrt(np.mean(np.square(bounds))))


def _nls_rmse(record, cfg):
    obs = record["observations"]; R = fixed_measurement_covariance()
    est = initialize_position(obs[0], cfg); errs = []
    for k in range(1, STEPS):
        est, _ = solve_position(obs[k], est, cfg, R)
        if k >= START:
            errs.append(np.linalg.norm(est - record["truth"][k]))
    return float(np.sqrt(np.mean(np.square(errs))))


def _routing_rmse(record, cfg):
    obs = record["observations"]; initial = initialize_position(obs[0], cfg)
    ukf = SignalObservationUKF(np.r_[initial, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    est = np.zeros((STEPS, 3)); est[0] = initial
    for k in range(1, STEPS):
        try:
            wrapper.step(obs[k], record["qualities"][k]); est[k] = ukf.x[:3]
        except Exception:
            est[k] = est[k-1]
    errs = np.linalg.norm(est[START:] - record["truth"][START:], axis=1)
    return float(np.sqrt(np.mean(errs**2)))


def _bias_floor(rmse, crlb):
    return float(np.sqrt(max(0.0, rmse**2 - crlb**2)))


def run():
    cfg = ChannelConfig()
    test = [collect_trajectory(d, t, "test") for d in DISTANCES for t in range(TRIALS)]
    R_design = fixed_measurement_covariance()
    R_emp = empirical_R(test, cfg)

    rows = []
    for rec in test:
        rows.append({"distance": rec["distance"],
                     "crlb_design_m": _crlb_bound(rec, cfg, R_design),
                     "crlb_emp_m": _crlb_bound(rec, cfg, R_emp),
                     "nls_rmse_m": _nls_rmse(rec, cfg),
                     "routing_rmse_m": _routing_rmse(rec, cfg)})
    summary = {}
    for d in list(DISTANCES) + ["overall"]:
        sub = rows if d == "overall" else [r for r in rows if r["distance"] == d]
        cd = float(np.mean([r["crlb_design_m"] for r in sub]))
        ce = float(np.mean([r["crlb_emp_m"] for r in sub]))
        nls = float(np.mean([r["nls_rmse_m"] for r in sub]))
        rt = float(np.mean([r["routing_rmse_m"] for r in sub]))
        summary[str(d)] = {
            "crlb_design_m": cd, "crlb_empirical_m": ce,
            "nls_rmse_m": nls, "routing_rmse_m": rt,
            "routing_efficiency_vs_emp": float((ce / rt) ** 2) if rt > 0 else float("nan"),
            "routing_bias_floor_vs_emp_m": _bias_floor(rt, ce),
            "n": len(sub),
        }
    payload = {"config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                          "steps": STEPS, "start_ping": START,
                          "empirical_R_diag_note": "z-h(참) 대각 분산, 편향 포함 유효잡음",
                          "note": "CRLB(design R 느슨) vs CRLB(empirical R 현실적) vs 실제 RMSE"},
               "empirical_R_std": {"range_m": float(np.sqrt(R_emp[0, 0])),
                                   "doa_az_deg": float(np.degrees(np.sqrt(R_emp[8, 8]))),
                                   "doa_el_deg": float(np.degrees(np.sqrt(R_emp[9, 9])))},
               "summary": summary, "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "crlb.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"config": payload["config"], "empirical_R_std": payload["empirical_R_std"],
                      "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
