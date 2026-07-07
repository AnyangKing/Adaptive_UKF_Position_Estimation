"""53번 (방향 A 핵심): 굴절 궤적에서 위치+gradient joint UKF가 (1) gradient를 식별하고
(2) 위치 RMSE를 baseline(굴절 무시) 대비 개선하는지 판정한다.

각 궤적은 상수 음속 gradient를 갖고 소스가 이동한다(거리 변화). baseline 6차원 UKF는 굴절을
모델에 없이 돌리고, joint 7차원 UKF는 gradient를 상태로 추정한다. gradient 추정이 참값으로
수렴하고 위치가 개선되면 방향 A가 성립한다. Ground Truth는 평가에만.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from joint_ukf import JointPositionGradientUKF
from measurement import fixed_measurement_covariance, initialize_position
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 24
STEPS = 10
GRAD_ROOT = 530000
NOISE_ROOT = 533000
INIT_POS_COV = [8.0**2]*3 + [1.5**2]*3


def trajectory(trial):
    rng = np.random.default_rng(GRAD_ROOT + trial)
    distance = rng.uniform(150.0, 550.0); az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(15.0, 75.0)
    start = np.array([distance*np.cos(az), distance*np.sin(az), -depth])
    tangent = np.array([-np.sin(az), np.cos(az), 0.0]); radial = np.array([np.cos(az), np.sin(az), 0.0])
    speed = rng.uniform(0.4, 1.2); heading = rng.uniform(-0.5, 0.5)
    horiz = speed*(np.cos(heading)*tangent + np.sin(heading)*radial); vz = rng.uniform(-0.08, 0.08)
    truth = start + np.arange(STEPS)[:, None]*np.r_[horiz[:2], vz]
    gradient = float(rng.uniform(-0.1, 0.1))
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)))
    return truth, gradient, env


def observe(truth, gradient, env, trial):
    obs = []
    for k, pos in enumerate(truth):
        cfg = replace(ChannelConfig(), seed=NOISE_ROOT + trial*STEPS + k, second_order_multipath=True,
                      surface_roughness=0.3, sound_speed_gradient=gradient, **env)
        _, received, _ = synthesize_received(pos, cfg)
        z, _ = extract_measurement(received, cfg)
        obs.append(z)
    return np.asarray(obs)


def run_baseline(obs, truth, cfg):
    init = initialize_position(obs[0], cfg)
    ukf = SignalObservationUKF(np.r_[init, np.zeros(3)], np.diag(INIT_POS_COV),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    est = np.zeros((STEPS, 3)); est[0] = init
    for k in range(1, STEPS):
        try: est[k] = ukf.step(obs[k])[:3]
        except Exception: est[k] = est[k-1]
    return est


def run_joint(obs, truth, cfg):
    init = initialize_position(obs[0], cfg)
    Q = np.zeros((7, 7)); Q[:6, :6] = acceleration_process_covariance(1.0, 0.20)
    Q[6, 6] = 0.005**2   # gradient 랜덤워크(거의 상수)
    P0 = np.diag(INIT_POS_COV + [0.1**2])
    ukf = JointPositionGradientUKF(np.r_[init, np.zeros(3), 0.0], P0, Q,
                                   fixed_measurement_covariance(), cfg)
    est = np.zeros((STEPS, 3)); est[0] = init; g_hist = [0.0]
    for k in range(1, STEPS):
        try:
            x = ukf.step(obs[k]); est[k] = x[:3]; g_hist.append(float(x[6]))
        except Exception:
            est[k] = est[k-1]; g_hist.append(g_hist[-1])
    return est, g_hist[-1]


def _rmse(est, truth, start=3):
    e = np.linalg.norm(est[start:] - truth[start:], axis=1)
    return float(np.sqrt(np.mean(e**2)))


def run():
    cfg = ChannelConfig()
    rows = []
    for t in range(TRIALS):
        truth, g_true, env = trajectory(t)
        obs = observe(truth, g_true, env, t)
        base = run_baseline(obs, truth, cfg)
        joint, g_est = run_joint(obs, truth, cfg)
        rows.append({"trial": t, "g_true": g_true, "g_est": g_est,
                     "baseline_rmse_m": _rmse(base, truth), "joint_rmse_m": _rmse(joint, truth)})
    g_true = np.array([r["g_true"] for r in rows]); g_est = np.array([r["g_est"] for r in rows])
    base = np.array([r["baseline_rmse_m"] for r in rows]); joint = np.array([r["joint_rmse_m"] for r in rows])
    from scipy.stats import spearmanr, wilcoxon
    diffs = base - joint
    try: w_p = float(wilcoxon(diffs, alternative="greater").pvalue) if np.any(diffs != 0) else 1.0
    except ValueError: w_p = 1.0
    payload = {"config": {"trials": TRIALS, "steps": STEPS, "gradient_range": [-0.1, 0.1],
                          "refraction_K": 3.21e-4,
                          "note": "굴절 궤적서 위치+gradient joint UKF vs baseline(굴절 무시)"},
               "gradient_identifiability": {
                   "g_est_vs_g_true_rho": float(spearmanr(g_true, g_est)[0]),
                   "g_est_vs_g_true_p": float(spearmanr(g_true, g_est)[1]),
                   "g_rmse_joint": float(np.sqrt(np.mean((g_est-g_true)**2))),
                   "g_rmse_prior0": float(np.sqrt(np.mean(g_true**2)))},
               "position": {"baseline_mean_rmse_m": float(np.mean(base)),
                            "joint_mean_rmse_m": float(np.mean(joint)),
                            "mean_improvement_m": float(np.mean(diffs)),
                            "improved_fraction": float(np.mean(diffs > 0)),
                            "wilcoxon_greater_p": w_p},
               "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "joint.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "trials"}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
