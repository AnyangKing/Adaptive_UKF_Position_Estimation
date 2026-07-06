"""이동 소스의 다중 ping 궤적을 만들고 ping별 채택 관측(peak_margin 포함)을 수집한다.

23번 강건성 시험과 같은 등속 궤적 구조를 쓰되, validation/test 궤적을 seed로 완전히 분리한다.
관측 z는 채택 알고리즘과 동일한 gated-SRP 기반이고, 여기에 고도각 편향 보정을 위한 peak_margin과
참고도(GT, calibration residual 용도)를 함께 저장한다.
"""

from __future__ import annotations

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from measurement import ideal_measurement
from peak_measurement import extract_measurement

DISTANCES = (100, 200, 400, 600)
STEPS = 10
# validation(계수 적합)과 test(평가)의 궤적 seed 계열을 분리한다.
SPLIT_ROOT = {"validation": 390000, "test": 395000}
PING_ROOT = {"validation": 391000, "test": 396000}


def scenario(distance: int, trial: int, split: str):
    """등속 이동 궤적과 고정 환경을 독립 seed로 만든다."""
    rng = np.random.default_rng(SPLIT_ROOT[split] + distance * 100 + trial)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(10.0, 80.0)
    start = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
    tangent = np.array([-np.sin(az), np.cos(az), 0.0])
    radial = np.array([np.cos(az), np.sin(az), 0.0])
    speed = rng.uniform(0.4, 1.2)
    heading = rng.uniform(-0.5, 0.5)
    horizontal = speed * (np.cos(heading) * tangent + np.sin(heading) * radial)
    vz = rng.uniform(-0.08, 0.08)
    t = np.arange(STEPS, dtype=float)
    truth = start + t[:, None] * np.r_[horizontal[:2], vz]
    meta = dict(
        snr_db=float(rng.choice([10.0, 20.0, 30.0])),
        surface_reflection=float(-rng.uniform(0.70, 0.98)),
        bottom_reflection=float(rng.uniform(0.30, 0.80)),
        radial_velocity_m_s=float(rng.uniform(-1.5, 1.5)),
    )
    return truth, meta


def collect_trajectory(distance: int, trial: int, split: str):
    """궤적을 따라 ping별 관측 z, 품질(peak_margin 포함), 참고도각을 수집한다."""
    cfg = ChannelConfig()
    truth, meta = scenario(distance, trial, split)
    observations, qualities, true_elevations = [], [], []
    for k, position in enumerate(truth):
        ping_cfg = replace(cfg, seed=PING_ROOT[split] + distance * 100 + trial * STEPS + k,
                           snr_db=meta["snr_db"], surface_reflection=meta["surface_reflection"],
                           bottom_reflection=meta["bottom_reflection"],
                           radial_velocity_m_s=meta["radial_velocity_m_s"])
        _, received, _ = synthesize_received(position, ping_cfg)
        z, q = extract_measurement(received, ping_cfg)
        observations.append(z)
        qualities.append(q)
        true_elevations.append(float(ideal_measurement(position, ping_cfg)[9]))
    return {
        "distance": distance, "trial": trial, "split": split,
        "truth": np.asarray(truth), "observations": np.asarray(observations),
        "qualities": qualities, "true_elevation_rad": np.asarray(true_elevations),
        "meta": meta,
    }
