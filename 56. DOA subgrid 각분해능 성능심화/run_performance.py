"""56번 (성능 심화): DOA sub-grid 보간이 각 오차와 위치 RMSE를 줄이는가, 특히 근거리서 1m에
얼마나 가까워지는가.

같은 궤적·같은 채택 라우팅 UKF에서 관측 DOA만 baseline(0.2° argmax) vs sub-grid 보간으로 바꿔
비교한다. novelty가 아니라 순수 성능 최적화. GT는 평가에만.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from improved_doa import extract_measurement_subgrid
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position
from peak_measurement import extract_measurement
from trajectory import DISTANCES, STEPS, PING_ROOT, scenario
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 12
ROUTING_THRESHOLD_DEG = 5.0


def _unit(az, el):
    return np.array([np.cos(el)*np.cos(az), np.cos(el)*np.sin(az), np.sin(el)])


def collect(distance, trial):
    truth, meta = scenario(distance, trial, "test")
    base_obs, sub_obs, base_q, sub_q = [], [], [], []
    doa_err_base, doa_err_sub = [], []
    for k, pos in enumerate(truth):
        cfg = replace(ChannelConfig(), seed=PING_ROOT["test"] + distance*100 + trial*STEPS + k,
                      snr_db=meta["snr_db"], surface_reflection=meta["surface_reflection"],
                      bottom_reflection=meta["bottom_reflection"],
                      radial_velocity_m_s=meta["radial_velocity_m_s"])
        _, received, _ = synthesize_received(pos, cfg)
        zb, qb = extract_measurement(received, cfg)
        zs, qs = extract_measurement_subgrid(received, cfg)
        truth_z = ideal_measurement(pos, cfg)
        td = _unit(truth_z[8], truth_z[9])
        doa_err_base.append(np.degrees(np.arccos(np.clip(_unit(zb[8], zb[9]) @ td, -1, 1))))
        doa_err_sub.append(np.degrees(np.arccos(np.clip(_unit(zs[8], zs[9]) @ td, -1, 1))))
        base_obs.append(zb); sub_obs.append(zs); base_q.append(qb); sub_q.append(qs)
    return (truth, np.asarray(base_obs), np.asarray(sub_obs), base_q, sub_q,
            float(np.median(doa_err_base)), float(np.median(doa_err_sub)))


def run_filter(obs, quals, truth, cfg):
    init = initialize_position(obs[0], cfg)
    ukf = SignalObservationUKF(np.r_[init, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    est = np.zeros((STEPS, 3)); est[0] = init
    for k in range(1, STEPS):
        try: wrapper.step(obs[k], quals[k]); est[k] = ukf.x[:3]
        except Exception: est[k] = est[k-1]
    e = np.linalg.norm(est[3:] - truth[3:], axis=1)
    return float(np.sqrt(np.mean(e**2)))


def run():
    cfg = ChannelConfig()
    rows = []
    for d in DISTANCES:
        for t in range(TRIALS):
            truth, bobs, sobs, bq, sq, deb, des = collect(d, t)
            rows.append({"distance": d,
                         "doa_err_base": deb, "doa_err_sub": des,
                         "rmse_base": run_filter(bobs, bq, truth, cfg),
                         "rmse_sub": run_filter(sobs, sq, truth, cfg)})
    summary = {}
    for d in list(DISTANCES) + ["overall"]:
        sub = rows if d == "overall" else [r for r in rows if r["distance"] == d]
        summary[str(d)] = {
            "median_doa_err_base_deg": float(np.median([r["doa_err_base"] for r in sub])),
            "median_doa_err_sub_deg": float(np.median([r["doa_err_sub"] for r in sub])),
            "mean_rmse_base_m": float(np.mean([r["rmse_base"] for r in sub])),
            "mean_rmse_sub_m": float(np.mean([r["rmse_sub"] for r in sub])),
            "rmse_improvement_m": float(np.mean([r["rmse_base"]-r["rmse_sub"] for r in sub])),
            "sub_under_1m_fraction": float(np.mean([r["rmse_sub"] < 1.0 for r in sub])),
            "n": len(sub)}
    payload = {"config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                          "steps": STEPS, "note": "DOA 0.2° argmax vs sub-grid 보간, 위치 RMSE 비교"},
               "summary": summary, "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "performance.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
