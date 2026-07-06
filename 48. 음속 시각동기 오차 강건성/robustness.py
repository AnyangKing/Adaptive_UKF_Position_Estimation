"""음속 불일치와 시각동기(클럭) 오차 하에서 채택 라우팅 UKF의 강건성 평가.

실전 수중측위는 (1) 가정 음속과 실제 음속이 다르고(수온·염분·깊이 변화로 ±수십 m/s), (2) 절대
TOA에 송수신 클럭 오프셋이 낀다. 여기서는 신호를 실제 음속 c_true로 합성하고, 관측 추출·필터는
가정 음속 c_assumed(=1500)로 처리해 불일치를 만든다. 클럭 오프셋은 절대 TOA(z[0])에 더한다.

Ground Truth는 RMSE 평가에만 쓴다. 필터·관측 처리는 오직 가정 파라미터만 안다.
"""

from __future__ import annotations

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from conditional_adaptive import ConditionalAdaptiveRUKF
from measurement import fixed_measurement_covariance, initialize_position
from peak_measurement import extract_measurement
from trajectory import DISTANCES, STEPS, PING_ROOT, scenario
from ukf import SignalObservationUKF, acceleration_process_covariance

ROUTING_THRESHOLD_DEG = 5.0
ASSUMED_C = 1500.0


def collect_mismatched(distance, trial, split, c_true, clock_offset_s=0.0):
    """신호는 c_true로 합성, 관측 추출·필터는 가정 음속(1500)으로. z[0]에 클럭 오프셋 추가."""
    truth, meta = scenario(distance, trial, split)
    cfg_assumed = replace(ChannelConfig(), sound_speed_m_s=ASSUMED_C)
    observations, qualities = [], []
    for k, position in enumerate(truth):
        cfg_true = replace(ChannelConfig(), sound_speed_m_s=c_true,
                           seed=PING_ROOT[split] + distance * 100 + trial * STEPS + k,
                           snr_db=meta["snr_db"], surface_reflection=meta["surface_reflection"],
                           bottom_reflection=meta["bottom_reflection"],
                           radial_velocity_m_s=meta["radial_velocity_m_s"])
        _, received, _ = synthesize_received(position, cfg_true)
        z, q = extract_measurement(received, cfg_assumed)   # 가정 음속으로 처리
        z = z.copy(); z[0] += ASSUMED_C * clock_offset_s     # 절대 TOA에 클럭 오프셋
        observations.append(z); qualities.append(q)
    return {"distance": distance, "truth": truth, "observations": np.asarray(observations),
            "qualities": qualities}


def run_routing_rmse(record):
    cfg = replace(ChannelConfig(), sound_speed_m_s=ASSUMED_C)
    obs = record["observations"]
    initial = initialize_position(obs[0], cfg)
    ukf = SignalObservationUKF(np.r_[initial, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    est = np.zeros((STEPS, 3)); est[0] = initial; diverged = False
    for k in range(1, STEPS):
        try:
            wrapper.step(obs[k], record["qualities"][k]); est[k] = ukf.x[:3]
        except Exception:
            diverged = True; est[k] = est[k-1]
    err = np.linalg.norm(est[3:] - record["truth"][3:], axis=1)
    return float(np.sqrt(np.mean(err**2))), bool(diverged or np.any(
        np.linalg.norm(est - record["truth"], axis=1) > 50))
