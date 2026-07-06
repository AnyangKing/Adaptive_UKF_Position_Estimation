"""고정 기하에서 계통 DOA 편향(고도각/방위/전체)과 blind 관측 feature를 대규모로 뽑는다.

37번 C는 test 기하 24개라는 소표본에서 '고도각 계통 편향만 관측 신호 품질 feature로
부분 식별된다'는 양성 신호를 봤다. 38번은 완전히 새로운 seed로 거리당 훨씬 많은 고정 기하를
만들어 같은 관계가 재현되는지 확인한다. 37 C에서 유의했던 feature(GCC-SRP 불일치, peak
margin, 최소 peak 품질)는 모두 채택 관측(gated SRP) 추출에서 얻으므로 full-SRP가 필요한
비유의 feature(gated_full_gap)는 제거해 런타임을 줄인다.

Ground Truth는 오차/편향 label 산출에만 쓴다.
"""

from __future__ import annotations

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from measurement import ideal_measurement
from peak_measurement import extract_measurement

DISTANCES = (100, 200, 400, 600)
GEOMETRIES_PER_DISTANCE = 40     # 37번(6)의 약 7배
REPEATS = 8                      # 기하당 독립 noise seed 반복
GEOMETRY_ROOT = 380000           # 37번과 겹치지 않는 새 seed 계열
NOISE_ROOT = 383000

SIGNAL_FEATURES = ("doa_disagreement_deg", "peak_margin", "neg_min_peak_quality")


def _unit(azimuth: float, elevation: float) -> np.ndarray:
    return np.array([
        np.cos(elevation) * np.cos(azimuth),
        np.cos(elevation) * np.sin(azimuth),
        np.sin(elevation),
    ])


def wrap(value: float) -> float:
    return float((value + np.pi) % (2.0 * np.pi) - np.pi)


def geometry(distance: int, index: int) -> tuple[np.ndarray, dict]:
    """거리·방위·깊이·환경이 고정된 하나의 기하. 37번과 다른 seed 계열을 쓴다."""
    rng = np.random.default_rng(GEOMETRY_ROOT + distance * 50 + index)
    azimuth = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    position = np.array([distance * np.cos(azimuth), distance * np.sin(azimuth), -depth])
    env = dict(
        snr_db=float(rng.choice([10.0, 20.0, 30.0])),
        surface_reflection=float(-rng.uniform(0.72, 0.97)),
        bottom_reflection=float(rng.uniform(0.32, 0.78)),
        radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)),
    )
    return position, env


def decompose_geometry(distance: int, index: int) -> dict:
    """한 기하에서 계통 편향과 blind feature를 반복측정으로 계산한다."""
    position, env = geometry(distance, index)
    cfg0 = replace(ChannelConfig(), **env)
    truth = ideal_measurement(position, cfg0)
    true_direction = _unit(truth[8], truth[9])

    directions, feats = [], {name: [] for name in SIGNAL_FEATURES}
    for repeat in range(REPEATS):
        seed = NOISE_ROOT + distance * 1000 + index * 20 + repeat
        cfg = replace(ChannelConfig(), seed=seed, **env)
        _, received, _ = synthesize_received(position, cfg)
        z, quality = extract_measurement(received, cfg)
        directions.append(_unit(z[8], z[9]))
        feats["doa_disagreement_deg"].append(float(quality["doa_disagreement_deg"]))
        feats["peak_margin"].append(float(quality["peak_margin"]))
        feats["neg_min_peak_quality"].append(float(-quality["minimum_peak_quality"]))

    directions = np.asarray(directions)
    mean_direction = directions.mean(axis=0)
    mean_direction /= np.linalg.norm(mean_direction)

    bias_angle = float(np.degrees(np.arccos(np.clip(mean_direction @ true_direction, -1.0, 1.0))))
    az_errors = np.array([wrap(np.arctan2(d[1], d[0]) - truth[8]) for d in directions])
    el_errors = np.array([np.arctan2(d[2], np.hypot(d[0], d[1])) - truth[9] for d in directions])
    random_angle = float(np.mean(np.degrees(np.arccos(
        np.clip(directions @ mean_direction, -1.0, 1.0)))))

    return {
        "distance": distance,
        "index": index,
        "bias_angle_deg": bias_angle,
        "random_angle_deg": random_angle,
        "az_bias_deg": float(np.degrees(np.mean(az_errors))),
        "el_bias_deg": float(np.degrees(np.mean(el_errors))),
        "pos_bias_m": float(distance * np.sin(np.radians(bias_angle))),
        "features": {name: float(np.mean(values)) for name, values in feats.items()},
    }


def collect() -> list[dict]:
    records = []
    for distance in DISTANCES:
        for index in range(GEOMETRIES_PER_DISTANCE):
            records.append(decompose_geometry(distance, index))
    return records
