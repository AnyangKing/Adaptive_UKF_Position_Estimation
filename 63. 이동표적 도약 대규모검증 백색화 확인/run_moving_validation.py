"""63번 (기둥 B의 이동 확장 판정): 이동표적 정착추적에서 도약 이득의 대규모 독립검증 +
백색화 기전 직접확인.

62번은 이동 조건 전부에서 평균 이득 양수(단 n=8 소표본)와 백색화 가설 — 도약의 본질은 상관
드리프트 편향을 ping간 백색 오차로 바꿔 필터가 잡음평균하게 만드는 것 — 을 도출했다. 여기서는
정책 완전 동결(도약 집합·필터·정착창 61/62와 동일), 완전 신규 seed, 조건당 16기하로:

사전등록 가설:
  M1) 이동 4조건 pooled 도약 이득 > 0 (Wilcoxon 단측) — "이동 정착추적에도 유효" 주판정.
  M2) 백색화: 고도각 오차 시퀀스의 lag-1 자기상관이 hop < fixed (paired 단측) — 기전 직접증거.
  M3) 조건별 이득 방향 기록(62 방향과 비교).

GT는 평가·오차 label에만. 실행 python run_moving_validation.py.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.stats import spearmanr, wilcoxon

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance

DISTANCE = 600.0
GEOMS = 16
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0
HOP_CARRIERS_HZ = np.linspace(30000.0, 34000.0, STEPS)   # 61/62 동결 정책
FIXED_CARRIER_HZ = 32000.0
GEOM_ROOT = 690000                                        # 60/61/62와 겹침 없는 신규 계열
PING_ROOT = 1300000

CONDITIONS = (
    ("radial_0.05",    0.05, "radial",     0.00),
    ("radial_1.0",     1.00, "radial",     0.00),
    ("tangential_1.0", 1.00, "tangential", 0.00),
    ("tang_1.0_vz",    1.00, "tangential", 0.08),
)


def geometry(cond_idx, index):
    rng = np.random.default_rng(GEOM_ROOT + cond_idx * 1000 + index)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    pos = np.array([DISTANCE * np.cos(az), DISTANCE * np.sin(az), -depth])
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=0.0)
    sign = 1.0 if rng.uniform() < 0.5 else -1.0
    return pos, env, az, sign


def truth_trajectory(pos, az, sign, speed, mode, vz):
    radial = np.array([np.cos(az), np.sin(az), 0.0])
    tangential = np.array([-np.sin(az), np.cos(az), 0.0])
    v = (sign * speed * radial) if mode == "radial" else (speed * tangential)
    v = v + np.array([0.0, 0.0, sign * vz])
    return pos + np.arange(STEPS)[:, None] * v


def collect(truth, env, cond_idx, index, carriers):
    obs, quals, el_err = [], [], []
    for k, pos in enumerate(truth):
        cfg = replace(ChannelConfig(), seed=PING_ROOT + cond_idx * 4000 + index * 60 + k,
                      carrier_hz=float(carriers[k]), **env)
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        truth_z = ideal_measurement(pos, cfg)
        el_err.append(float(z[9] - truth_z[9]))    # 고도각 오차 시퀀스 (백색화 검증용)
        obs.append(z); quals.append(q)
    return np.asarray(obs), quals, np.asarray(el_err)


def lag1_autocorr(x):
    x = np.asarray(x, float)
    a, b = x[:-1] - x[:-1].mean(), x[1:] - x[1:].mean()
    denom = np.sqrt(np.sum(a*a) * np.sum(b*b))
    return float(np.sum(a*b) / denom) if denom > 1e-12 else 0.0


def run_filter(obs, quals, truth, cfg):
    init = initialize_position(obs[0], cfg)
    ukf = SignalObservationUKF(np.r_[init, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    est = np.zeros((STEPS, 3)); est[0] = init
    for k in range(1, STEPS):
        try:
            wrapper.step(obs[k], quals[k]); est[k] = ukf.x[:3]
        except Exception:
            est[k] = est[k-1]
    err = np.linalg.norm(est - truth, axis=1)
    return float(np.sqrt(np.mean(err[SETTLE_START:]**2)))


def _bootstrap_ci(diffs, seed=630, n=5000):
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(diffs, len(diffs), replace=True)) for _ in range(n)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def run():
    cfg = ChannelConfig()
    fixed = np.full(STEPS, FIXED_CARRIER_HZ)
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    partial_path = out / "moving_validation_partial.json"
    if partial_path.exists():
        rows = json.loads(partial_path.read_text(encoding="utf-8"))["runs"]
    else:
        rows = []
    done = {(r["condition"], int(r["index"])) for r in rows}
    for ci, (name, speed, mode, vz) in enumerate(CONDITIONS):
        for i in range(GEOMS):
            if (name, i) in done:
                continue
            pos, env, az, sign = geometry(ci, i)
            truth = truth_trajectory(pos, az, sign, speed, mode, vz)
            obs_f, q_f, el_f = collect(truth, env, ci, i, fixed)
            obs_h, q_h, el_h = collect(truth, env, ci, i, HOP_CARRIERS_HZ)
            rows.append({"condition": name, "index": i,
                         "fixed_rmse_m": run_filter(obs_f, q_f, truth, cfg),
                         "hop_rmse_m": run_filter(obs_h, q_h, truth, cfg),
                         "lag1_fixed": lag1_autocorr(el_f), "lag1_hop": lag1_autocorr(el_h)})
            rows[-1]["gain_m"] = rows[-1]["fixed_rmse_m"] - rows[-1]["hop_rmse_m"]
            partial_path.write_text(json.dumps({"runs": rows}, indent=2, ensure_ascii=False),
                                    encoding="utf-8")
            print(f"completed {len(rows)}/{len(CONDITIONS) * GEOMS}: {name} #{i}", flush=True)
    gains = np.array([r["gain_m"] for r in rows])
    lag_f = np.array([r["lag1_fixed"] for r in rows])
    lag_h = np.array([r["lag1_hop"] for r in rows])
    lag_reduction = lag_f - lag_h
    lag_gain_rho, lag_gain_p = spearmanr(lag_reduction, gains)
    lo, hi = _bootstrap_ci(gains)
    m1_p = float(wilcoxon(gains, alternative="greater").pvalue)
    m2_p = float(wilcoxon(lag_f - lag_h, alternative="greater").pvalue)
    summary = {"M1_pooled_moving": {
                   "mean_gain_m": float(np.mean(gains)), "median_gain_m": float(np.median(gains)),
                   "gain_ci95": [lo, hi], "wilcoxon_greater_p": m1_p,
                   "improved_fraction": float(np.mean(gains > 0)), "n": len(rows)},
               "M2_whitening": {
                   "mean_lag1_fixed": float(np.mean(lag_f)), "mean_lag1_hop": float(np.mean(lag_h)),
                   "median_lag1_fixed": float(np.median(lag_f)), "median_lag1_hop": float(np.median(lag_h)),
                   "wilcoxon_fixed_gt_hop_p": m2_p,
                   "reduced_fraction": float(np.mean(lag_f > lag_h))},
               "M2b_lag_reduction_vs_gain": {
                   "spearman_rho": float(lag_gain_rho),
                   "p": float(lag_gain_p)},
               "M3_by_condition": {}}
    for name, *_ in CONDITIONS:
        sub = [r for r in rows if r["condition"] == name]
        g = np.array([r["gain_m"] for r in sub])
        try:
            wp = float(wilcoxon(g, alternative="greater").pvalue) if np.any(g != 0) else 1.0
        except ValueError:
            wp = 1.0
        summary["M3_by_condition"][name] = {
            "fixed_mean_rmse_m": float(np.mean([r["fixed_rmse_m"] for r in sub])),
            "hop_mean_rmse_m": float(np.mean([r["hop_rmse_m"] for r in sub])),
            "mean_gain_m": float(np.mean(g)), "median_gain_m": float(np.median(g)),
            "improved_fraction": float(np.mean(g > 0)), "wilcoxon_greater_p": wp, "n": len(sub)}
    payload = {"config": {"distance_m": DISTANCE, "geoms_per_condition": GEOMS, "steps": STEPS,
                          "conditions": [c[0] for c in CONDITIONS],
                          "note": "정책동결(61/62)·신규 seed. M1 pooled 이득, M2 lag-1 백색화, M3 조건별"},
               "summary": summary, "runs": rows}
    (out / "moving_validation.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                                encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
