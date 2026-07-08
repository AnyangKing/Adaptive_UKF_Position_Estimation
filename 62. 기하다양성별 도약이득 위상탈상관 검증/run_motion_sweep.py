"""62번: 도약 이득의 지배 변수가 "정지/이동"이 아니라 "관측 창 내 멀티패스 위상 탈상관"인지 검증.

재프레임 가설: frequency agility는 정지 전용이 아니라 **기하 다양성이 부족할 때 주파수 다양성으로
멀티패스 간섭 위상을 탈상관시키는 관측 설계**다. 간섭 위상 φ=2πf·δ(δ=표면-직접 지연차)는
δ≈2·d_s·d_r/(c·X)라서 방위(접선) 운동으로는 거의 안 돌고, 수평거리(radial)·깊이(vz) 변화로 돈다
(600 m 기준 1사이클에 radial ~7 m vs 깊이 ~0.47 m — vz가 15배 민감).

사전등록 가설 (조건별 예측 위상 스윙과 함께):
  H1) 도약 이득은 관측 창의 예측 위상 스윙(cycles = f·(δ_max−δ_min))과 반비례한다.
  H2) 접선 1.0 m/s(vz=0, 등거리 선회)는 빨라도 cycles≈0 → 정지처럼 큰 이득 (속도≠기하다양성 입증).
  H3) 같은 1.0 m/s라도 vz=0.08을 더하면(59 유사) cycles≫1 → 이득 소멸 (59 null의 원인 규명).
  H4) radial 저속(0.05)은 이득 유지, radial 고속(1.0)은 이득 소멸.

600 m(효과 최대 거리), 조건 6종 × 8기하, 20 ping, fixed 32 kHz vs 30~34 kHz 도약(정책 61 동결).
GT는 평가·δ 계산(사후 설명변수)에만. 실행 python run_motion_sweep.py.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.stats import spearmanr, wilcoxon

from channel import paths_for_sensor, synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig, usb_array_global_m
from measurement import fixed_measurement_covariance, initialize_position
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance

DISTANCE = 600.0
GEOMS = 8
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0
HOP_CARRIERS_HZ = np.linspace(30000.0, 34000.0, STEPS)
FIXED_CARRIER_HZ = 32000.0
GEOM_ROOT = 680000
PING_ROOT = 683000

# 조건: (이름, 속력 m/s, 방향 모드, vz m/s)
CONDITIONS = (
    ("static",        0.00, "none",       0.00),
    ("radial_0.05",   0.05, "radial",     0.00),
    ("radial_0.2",    0.20, "radial",     0.00),
    ("radial_1.0",    1.00, "radial",     0.00),
    ("tangential_1.0",1.00, "tangential", 0.00),   # 등거리 선회, 빠르지만 δ 불변 예측
    ("tang_1.0_vz",   1.00, "tangential", 0.08),   # 59 유사: vz가 위상을 돌림 예측
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
    sign = 1.0 if rng.uniform() < 0.5 else -1.0     # radial 안/밖, vz 상/하 부호 랜덤
    return pos, env, az, sign


def truth_trajectory(pos, az, sign, speed, mode, vz):
    radial = np.array([np.cos(az), np.sin(az), 0.0])
    tangential = np.array([-np.sin(az), np.cos(az), 0.0])
    if mode == "radial":
        v = sign * speed * radial
    elif mode == "tangential":
        v = speed * tangential
    else:
        v = np.zeros(3)
    v = v + np.array([0.0, 0.0, sign * vz])
    return pos + np.arange(STEPS)[:, None] * v


def phase_swing_cycles(truth, env, f_hz=FIXED_CARRIER_HZ):
    """관측 창의 예측 위상 스윙: f·(max δ − min δ), δ=표면-직접 지연차(기준 센서)."""
    cfg = replace(ChannelConfig(), **env)
    sensor0 = usb_array_global_m(cfg.receiver_depth_m)[0]
    deltas = []
    for pos in truth:
        d = {p.name: p.delay_s for p in paths_for_sensor(pos, sensor0, cfg)}
        deltas.append(d["surface"] - d["direct"])
    deltas = np.asarray(deltas)
    return float(f_hz * (deltas.max() - deltas.min()))


def collect(truth, env, cond_idx, index, carriers):
    obs, quals = [], []
    for k, pos in enumerate(truth):
        cfg = replace(ChannelConfig(), seed=PING_ROOT + cond_idx * 4000 + index * 60 + k,
                      carrier_hz=float(carriers[k]), **env)
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        obs.append(z); quals.append(q)
    return np.asarray(obs), quals


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


def run():
    cfg = ChannelConfig()
    fixed = np.full(STEPS, FIXED_CARRIER_HZ)
    rows = []
    for ci, (name, speed, mode, vz) in enumerate(CONDITIONS):
        for i in range(GEOMS):
            pos, env, az, sign = geometry(ci, i)
            truth = truth_trajectory(pos, az, sign, speed, mode, vz)
            cycles = phase_swing_cycles(truth, env)
            obs_f, q_f = collect(truth, env, ci, i, fixed)
            obs_h, q_h = collect(truth, env, ci, i, HOP_CARRIERS_HZ)
            rmse_f = run_filter(obs_f, q_f, truth, cfg)
            rmse_h = run_filter(obs_h, q_h, truth, cfg)
            rows.append({"condition": name, "index": i, "phase_swing_cycles": cycles,
                         "fixed_rmse_m": rmse_f, "hop_rmse_m": rmse_h,
                         "gain_m": rmse_f - rmse_h})
    summary = {}
    for name, *_ in CONDITIONS:
        sub = [r for r in rows if r["condition"] == name]
        gains = np.array([r["gain_m"] for r in sub])
        try:
            w_p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
        except ValueError:
            w_p = 1.0
        summary[name] = {
            "mean_cycles": float(np.mean([r["phase_swing_cycles"] for r in sub])),
            "fixed_mean_rmse_m": float(np.mean([r["fixed_rmse_m"] for r in sub])),
            "hop_mean_rmse_m": float(np.mean([r["hop_rmse_m"] for r in sub])),
            "mean_gain_m": float(np.mean(gains)),
            "median_gain_m": float(np.median(gains)),
            "improved_fraction": float(np.mean(gains > 0)),
            "wilcoxon_greater_p": w_p, "n": len(sub)}
    cyc = np.array([r["phase_swing_cycles"] for r in rows])
    gain = np.array([r["gain_m"] for r in rows])
    rho, p = spearmanr(cyc, gain)
    payload = {"config": {"distance_m": DISTANCE, "geoms_per_condition": GEOMS, "steps": STEPS,
                          "conditions": [c[0] for c in CONDITIONS],
                          "hop_carriers_khz": [c/1000 for c in HOP_CARRIERS_HZ],
                          "note": "H1 gain~1/cycles, H2 접선=정지급 이득, H3 vz가 이득 소멸, H4 radial 속도의존"},
               "H1_gain_vs_cycles": {"spearman_rho": float(rho), "p": float(p)},
               "by_condition": summary, "runs": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "motion_sweep.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                           encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "runs"}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
