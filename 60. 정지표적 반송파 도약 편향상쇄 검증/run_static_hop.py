"""60번 (58·59 종합의 결정 실험): 정지 표적에서 반송파 도약이 멀티패스 편향 floor를 깎는가.

59번이 규명한 기전 — 간섭 위상 φ=2π·f·δ는 반송파(f)와 기하(δ) 어느 쪽으로도 돌릴 수 있고, 이동
소스는 기하 변화가 이미 편향을 자연 평균한다 — 에 따르면, 도약의 진짜 적용처는 **정지/준정지
표적**이다: δ가 고정이라 편향이 ping 축적으로 절대 안 없어지는 상수 floor(42·57)가 되고, 반송파
도약이 위상을 돌릴 유일한 수단이 된다. 58의 고정-기하 상쇄(600 m 편향 0.632°→0.053°)가 곧 기대
이득이다.

정지 표적, 20 ping 정착 시나리오에서 전 ping 32 kHz 고정 vs ping별 30~34 kHz 순환(20개)을 같은
seed·같은 채택 라우팅 UKF로 paired 비교한다. 지표는 정착 구간(후반 10 ping) RMSE. GT는 평가에만.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.stats import wilcoxon

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance

DISTANCES = (100, 200, 400, 600)
GEOMS = 8
STEPS = 20
SETTLE_START = 10                     # 후반 10 ping을 정착 구간으로
ROUTING_THRESHOLD_DEG = 5.0
HOP_CARRIERS_HZ = np.linspace(30000.0, 34000.0, STEPS)
FIXED_CARRIER_HZ = 32000.0
GEOM_ROOT = 600000
PING_ROOT = 603000


def geometry(distance, index):
    rng = np.random.default_rng(GEOM_ROOT + distance * 50 + index)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    pos = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=0.0)      # 정지 표적
    return pos, env


def collect(pos, env, distance, index, carriers):
    obs, quals = [], []
    for k in range(STEPS):
        cfg = replace(ChannelConfig(), seed=PING_ROOT + distance * 1000 + index * 40 + k,
                      carrier_hz=float(carriers[k]), **env)
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        obs.append(z); quals.append(q)
    return np.asarray(obs), quals


def run_filter(obs, quals, pos, cfg):
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
    err = np.linalg.norm(est - pos, axis=1)
    settled = float(np.sqrt(np.mean(err[SETTLE_START:]**2)))
    return settled, bool(np.any(err > 50))


def _bootstrap_ci(diffs, seed=600, n=5000):
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(diffs, len(diffs), replace=True)) for _ in range(n)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def run():
    cfg = ChannelConfig()
    fixed = np.full(STEPS, FIXED_CARRIER_HZ)
    rows = []
    for d in DISTANCES:
        for i in range(GEOMS):
            pos, env = geometry(d, i)
            obs_f, q_f = collect(pos, env, d, i, fixed)
            rmse_f, div_f = run_filter(obs_f, q_f, pos, cfg)
            obs_h, q_h = collect(pos, env, d, i, HOP_CARRIERS_HZ)
            rmse_h, div_h = run_filter(obs_h, q_h, pos, cfg)
            rows.append({"distance": d, "index": i,
                         "fixed_settled_rmse_m": rmse_f, "hop_settled_rmse_m": rmse_h,
                         "improvement_m": rmse_f - rmse_h,
                         "fixed_div": div_f, "hop_div": div_h})
    summary = {}
    for d in list(DISTANCES) + ["overall"]:
        sub = rows if d == "overall" else [r for r in rows if r["distance"] == d]
        diffs = np.array([r["improvement_m"] for r in sub])
        lo, hi = _bootstrap_ci(diffs)
        try:
            w_p = float(wilcoxon(diffs, alternative="greater").pvalue) if np.any(diffs != 0) else 1.0
        except ValueError:
            w_p = 1.0
        fx = np.array([r["fixed_settled_rmse_m"] for r in sub])
        hp = np.array([r["hop_settled_rmse_m"] for r in sub])
        summary[str(d)] = {
            "fixed_mean_rmse_m": float(np.mean(fx)), "hop_mean_rmse_m": float(np.mean(hp)),
            "fixed_median_rmse_m": float(np.median(fx)), "hop_median_rmse_m": float(np.median(hp)),
            "mean_improvement_m": float(np.mean(diffs)), "improvement_ci95": [lo, hi],
            "wilcoxon_greater_p": w_p, "improved_fraction": float(np.mean(diffs > 0)),
            "hop_under_1m_fraction": float(np.mean(hp < 1.0)),
            "fixed_div_rate": float(np.mean([r["fixed_div"] for r in sub])),
            "hop_div_rate": float(np.mean([r["hop_div"] for r in sub])),
            "n": len(sub)}
    payload = {"config": {"distances_m": list(DISTANCES), "geoms_per_distance": GEOMS,
                          "steps": STEPS, "settle_start": SETTLE_START,
                          "hop_carriers_khz": [c/1000 for c in HOP_CARRIERS_HZ],
                          "fixed_carrier_khz": FIXED_CARRIER_HZ/1000,
                          "note": "정지 표적 20 ping 정착: 32kHz 고정 vs ping별 도약, 동일 라우팅 UKF"},
               "summary": summary, "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "static_hop.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                         encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
