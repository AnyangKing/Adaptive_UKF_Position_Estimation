"""59번 (58 후속, 필터 수준 검증): ping마다 반송파를 순환(30~34 kHz)하면 기존 라우팅 UKF의
위치 RMSE(특히 400/600 m)가 32 kHz 고정 대비 실제로 떨어지는가.

58번은 장거리 계통 편향의 78~92%가 반송파-진동 성분이라 도약 평균으로 상쇄됨을 관측 수준에서
보였다. 여기서는 같은 궤적·같은 채택 라우팅 UKF에서 송신 반송파만 (a) 전 ping 32 kHz 고정 vs
(b) ping마다 30~34 kHz 10개 순환으로 바꿔, 필터가 자연히 편향을 평균하는지 paired 비교한다.
필터·R·라우팅은 전혀 수정하지 않는다(순수 송신 다양성). GT는 평가에만.
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
from trajectory import DISTANCES, STEPS, PING_ROOT, scenario
from ukf import SignalObservationUKF, acceleration_process_covariance

TRIALS = 12
ROUTING_THRESHOLD_DEG = 5.0
HOP_CARRIERS_HZ = np.linspace(30000.0, 34000.0, STEPS)   # ping k → k번째 반송파
FIXED_CARRIER_HZ = 32000.0


def collect(distance, trial, carriers):
    """궤적을 합성하되 ping k의 반송파를 carriers[k]로 둔다."""
    truth, meta = scenario(distance, trial, "test")
    obs, quals = [], []
    for k, pos in enumerate(truth):
        cfg = replace(ChannelConfig(), seed=PING_ROOT["test"] + distance*100 + trial*STEPS + k,
                      carrier_hz=float(carriers[k]), snr_db=meta["snr_db"],
                      surface_reflection=meta["surface_reflection"],
                      bottom_reflection=meta["bottom_reflection"],
                      radial_velocity_m_s=meta["radial_velocity_m_s"])
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        obs.append(z); quals.append(q)
    return truth, np.asarray(obs), quals


def run_filter(obs, quals, truth, cfg):
    init = initialize_position(obs[0], cfg)
    ukf = SignalObservationUKF(np.r_[init, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    est = np.zeros((STEPS, 3)); est[0] = init; diverged = False
    for k in range(1, STEPS):
        try:
            wrapper.step(obs[k], quals[k]); est[k] = ukf.x[:3]
        except Exception:
            diverged = True; est[k] = est[k-1]
    e = np.linalg.norm(est[3:] - truth[3:], axis=1)
    div50 = bool(diverged or np.any(np.linalg.norm(est - truth, axis=1) > 50))
    return float(np.sqrt(np.mean(e**2))), div50


def _bootstrap_ci(diffs, seed=590, n=5000):
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(diffs, len(diffs), replace=True)) for _ in range(n)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def run():
    cfg = ChannelConfig()
    fixed = np.full(STEPS, FIXED_CARRIER_HZ)
    rows = []
    for d in DISTANCES:
        for t in range(TRIALS):
            truth, obs_f, q_f = collect(d, t, fixed)
            rmse_f, div_f = run_filter(obs_f, q_f, truth, cfg)
            truth2, obs_h, q_h = collect(d, t, HOP_CARRIERS_HZ)
            rmse_h, div_h = run_filter(obs_h, q_h, truth2, cfg)
            rows.append({"distance": d, "trial": t,
                         "fixed_rmse_m": rmse_f, "hop_rmse_m": rmse_h,
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
        summary[str(d)] = {
            "fixed_mean_rmse_m": float(np.mean([r["fixed_rmse_m"] for r in sub])),
            "hop_mean_rmse_m": float(np.mean([r["hop_rmse_m"] for r in sub])),
            "fixed_median_rmse_m": float(np.median([r["fixed_rmse_m"] for r in sub])),
            "hop_median_rmse_m": float(np.median([r["hop_rmse_m"] for r in sub])),
            "mean_improvement_m": float(np.mean(diffs)),
            "improvement_ci95": [lo, hi], "wilcoxon_greater_p": w_p,
            "improved_fraction": float(np.mean(diffs > 0)),
            "fixed_div_rate": float(np.mean([r["fixed_div"] for r in sub])),
            "hop_div_rate": float(np.mean([r["hop_div"] for r in sub])),
            "n": len(sub)}
    payload = {"config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                          "steps": STEPS, "hop_carriers_khz": [c/1000 for c in HOP_CARRIERS_HZ],
                          "fixed_carrier_khz": FIXED_CARRIER_HZ/1000,
                          "note": "ping별 반송파 순환 vs 32kHz 고정, 동일 라우팅 UKF paired 비교"},
               "summary": summary, "trials": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "hopping.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                      encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
