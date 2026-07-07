"""57번 (성능 심화): 근거리(100·200 m)에서 ping을 늘려 위치오차가 정착하며 편향 하한(~0.9 m)까지
수렴해 sub-1m에 도달하는지 본다.

56번에서 근거리 RMSE(100 m 1.88 m)가 편향 하한(~0.9 m)보다 높아 비편향 오차(초기 과도·수직·랜덤)가
남아 있음을 확인했다. 여기서는 ping을 10→30으로 늘리고 정착 구간(후반 ping) RMSE를 보아, 비편향
성분이 줄어 sub-1m에 접근하는지 판정한다. novelty가 아니라 성능. GT는 평가에만.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance

DISTANCES = (100, 200)
TRIALS = 16
STEPS = 30
ROUTING_THRESHOLD_DEG = 5.0
GEOM_ROOT = 570000
PING_ROOT = 573000
WINDOWS = {"after3": 3, "after10": 10, "after20": 20, "steady_last5": STEPS-5}


def trajectory(distance, trial):
    rng = np.random.default_rng(GEOM_ROOT + distance*100 + trial)
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(15.0, 75.0)
    start = np.array([distance*np.cos(az), distance*np.sin(az), -depth])
    tangent = np.array([-np.sin(az), np.cos(az), 0.0]); radial = np.array([np.cos(az), np.sin(az), 0.0])
    speed = rng.uniform(0.4, 1.2); heading = rng.uniform(-0.5, 0.5)
    horiz = speed*(np.cos(heading)*tangent + np.sin(heading)*radial); vz = rng.uniform(-0.08, 0.08)
    truth = start + np.arange(STEPS)[:, None]*np.r_[horiz[:2], vz]
    meta = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
                surface_reflection=float(-rng.uniform(0.72, 0.97)),
                bottom_reflection=float(rng.uniform(0.32, 0.78)),
                radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)))
    return truth, meta


def run_trajectory(distance, trial, cfg):
    truth, meta = trajectory(distance, trial)
    obs, quals = [], []
    for k, pos in enumerate(truth):
        pc = replace(ChannelConfig(), seed=PING_ROOT + distance*100 + trial*STEPS + k,
                     snr_db=meta["snr_db"], surface_reflection=meta["surface_reflection"],
                     bottom_reflection=meta["bottom_reflection"],
                     radial_velocity_m_s=meta["radial_velocity_m_s"])
        _, received, _ = synthesize_received(pos, pc)
        z, q = extract_measurement(received, pc); obs.append(z); quals.append(q)
    obs = np.asarray(obs)
    init = initialize_position(obs[0], cfg)
    ukf = SignalObservationUKF(np.r_[init, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    est = np.zeros((STEPS, 3)); est[0] = init
    for k in range(1, STEPS):
        try: wrapper.step(obs[k], quals[k]); est[k] = ukf.x[:3]
        except Exception: est[k] = est[k-1]
    err = np.linalg.norm(est - truth, axis=1)
    return {name: float(np.sqrt(np.mean(err[start:]**2))) for name, start in WINDOWS.items()}


def run():
    cfg = ChannelConfig()
    rows = []
    for d in DISTANCES:
        for t in range(TRIALS):
            r = run_trajectory(d, t, cfg); r["distance"] = d; rows.append(r)
    summary = {}
    for d in DISTANCES:
        sub = [r for r in rows if r["distance"] == d]
        summary[str(d)] = {}
        for name in WINDOWS:
            vals = np.array([r[name] for r in sub])
            summary[str(d)][name] = {"mean_rmse_m": float(np.mean(vals)),
                                     "median_rmse_m": float(np.median(vals)),
                                     "under_1m_fraction": float(np.mean(vals < 1.0))}
    payload = {"config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                          "steps": STEPS, "windows": WINDOWS,
                          "note": "근거리 ping 30, 정착구간별 RMSE·<1m 비율. 편향하한 접근 여부"},
               "summary": summary, "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "settling.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
