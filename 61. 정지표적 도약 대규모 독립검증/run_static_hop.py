"""61번 (60의 대규모 독립 검증): 정지표적 반송파 도약 이득이 새 기하에서 재현되는가.

사전등록 원칙: 도약 정책(30~34 kHz 균등 20개)·필터·정착 창 등 모든 구성은 60번에서 동결했고
여기서 어떤 것도 재선택하지 않는다. 완전히 새로운 seed 계열로 거리당 기하를 8→20개(2.5배)로
늘려, 60번의 발견 — 600 m 정착 RMSE -30%(p=0.0039, 8/8) — 이 소표본 낙관(31→32, 39→40 전례)이
아닌지 판정한다. 사전등록 가설: (1) 600 m 개선>0 유의 재현, (2) 전체 개선>0, (3) 100/200 m 무효
예상(게이트 밖), (4) 400 m는 기록만(60에서 불확정). GT는 평가에만.
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
GEOMS = 20                            # 60번 8 → 20 (2.5배), 정책은 동결
STEPS = 20
SETTLE_START = 10                     # 후반 10 ping을 정착 구간으로 (60과 동일)
ROUTING_THRESHOLD_DEG = 5.0
HOP_CARRIERS_HZ = np.linspace(30000.0, 34000.0, STEPS)   # 60에서 동결한 정책
FIXED_CARRIER_HZ = 32000.0
GEOM_ROOT = 640000                    # 완전 독립 신규 seed 계열 (60의 최대 기하seed 630007 초과)
PING_ROOT = 613000


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
                          "note": "60 정책 동결·신규 독립 seed 대규모 재현 (사전등록: 600m 유의 재현 여부)"},
               "summary": summary, "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "static_hop_validation.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                                    encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
