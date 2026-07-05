"""진단 A: 채택 관측(gated SRP) DOA 오차를 계통 편향과 랜덤 성분으로 분해한다.

36번은 DOA 오차가 전 거리 5° 미만이라 게이팅할 이상 관측이 없고, 장거리 병목이
기하로 증폭되는 '작은 계통적 각도 편향'이라고 재정의했다. 이 진단은 그 계통 편향이
실제로 존재하는지(=noise 평균 후에도 남는지)를 Ground Truth를 label로만 써서 확인한다.

방법: 하나의 고정 기하(거리·방위·깊이·환경)에 대해 관측 noise seed만 R회 바꿔 채택
관측을 반복 합성한다. 반복평균 방향과 참방향의 각도차가 계통 편향(bias), 각 반복이
반복평균 주위로 흩어지는 정도가 랜덤 성분(random)이다. 계통 편향은 다중 ping 평균으로
사라지지 않고 랜덤은 1/sqrt(N)로 준다. bias/random 비가 1 이상이면 계통 편향이 실재한다.

blind 식별성(진단 C)에서 재사용하도록 관측 feature도 함께 저장한다.
"""

from __future__ import annotations

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from estimators import estimate_srp_phat_doa
from measurement import ideal_measurement
from peak_measurement import extract_measurement

DISTANCES = (100, 200, 400, 600)
GEOMETRIES_PER_DISTANCE = 6      # 거리당 고정 기하(방위·깊이·환경) 수
REPEATS = 10                     # 기하당 독립 noise seed 반복 수
GEOMETRY_ROOT = 370000
NOISE_ROOT = 371000


def _unit(azimuth: float, elevation: float) -> np.ndarray:
    return np.array([
        np.cos(elevation) * np.cos(azimuth),
        np.cos(elevation) * np.sin(azimuth),
        np.sin(elevation),
    ])


def wrap(value: float) -> float:
    return float((value + np.pi) % (2.0 * np.pi) - np.pi)


def geometry(distance: int, index: int, split: str) -> tuple[np.ndarray, dict]:
    """거리·방위·깊이·환경이 고정된 하나의 기하를 만든다. noise seed는 여기서 정하지 않는다."""
    offset = 0 if split == "validation" else 900000
    rng = np.random.default_rng(GEOMETRY_ROOT + offset + distance * 20 + index)
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


def repeated_directions(position, env, distance, index, split):
    """고정 기하에서 noise seed만 바꿔 채택 관측 DOA 방향과 feature를 R회 수집한다."""
    offset = 0 if split == "validation" else 900000
    directions, features = [], []
    for repeat in range(REPEATS):
        seed = NOISE_ROOT + offset + distance * 1000 + index * 50 + repeat
        cfg = replace(ChannelConfig(), seed=seed, **env)
        _, received, _ = synthesize_received(position, cfg)
        z, quality = extract_measurement(received, cfg)
        srp_direction = _unit(z[8], z[9])
        # 반사 에너지가 도래각을 당기는 정도: 전체창 SRP vs 직접파창 gated SRP 방향차.
        full_az, full_el, full_direction, _ = estimate_srp_phat_doa(received, cfg)
        gated_full_gap_deg = float(np.degrees(
            np.arccos(np.clip(srp_direction @ full_direction, -1.0, 1.0))))
        directions.append(srp_direction)
        features.append({
            "doa_disagreement_deg": float(quality["doa_disagreement_deg"]),
            "gated_full_gap_deg": gated_full_gap_deg,
            "peak_margin": float(quality["peak_margin"]),
            "neg_min_peak_quality": float(-quality["minimum_peak_quality"]),
        })
    return np.asarray(directions), features


def decompose_geometry(position, cfg_env, distance, index, split):
    """한 기하의 계통 편향/랜덤 성분과 위치 증폭을 계산한다."""
    cfg = replace(ChannelConfig(), **cfg_env)
    truth = ideal_measurement(position, cfg)
    true_direction = _unit(truth[8], truth[9])

    directions, features = repeated_directions(position, cfg_env, distance, index, split)
    mean_direction = directions.mean(axis=0)
    mean_direction /= np.linalg.norm(mean_direction)

    bias_angle = float(np.degrees(
        np.arccos(np.clip(mean_direction @ true_direction, -1.0, 1.0))))
    per_repeat_scatter = np.degrees(np.arccos(
        np.clip(directions @ mean_direction, -1.0, 1.0)))
    random_angle = float(np.mean(per_repeat_scatter))

    # azimuth/elevation 성분 분해 (과거 고도각 bias 병목 확인용).
    az_errors = np.array([wrap(np.arctan2(d[1], d[0]) - truth[8]) for d in directions])
    el_errors = np.array([np.arctan2(d[2], np.hypot(d[0], d[1])) - truth[9] for d in directions])
    az_bias_deg = float(np.degrees(np.mean(az_errors)))
    el_bias_deg = float(np.degrees(np.mean(el_errors)))
    az_random_deg = float(np.degrees(np.std(az_errors)))
    el_random_deg = float(np.degrees(np.std(el_errors)))

    # DOA만의 횡방향 위치 영향: 위치오차 ~ range * sin(angle).
    pos_bias_m = float(distance * np.sin(np.radians(bias_angle)))
    pos_random_m = float(distance * np.sin(np.radians(random_angle)))

    mean_features = {name: float(np.mean([f[name] for f in features]))
                     for name in features[0]}
    return {
        "distance": distance,
        "index": index,
        "true_azimuth_deg": float(np.degrees(truth[8])),
        "true_elevation_deg": float(np.degrees(truth[9])),
        "bias_angle_deg": bias_angle,
        "random_angle_deg": random_angle,
        "bias_over_random": float(bias_angle / random_angle) if random_angle > 1e-9 else float("inf"),
        "az_bias_deg": az_bias_deg,
        "el_bias_deg": el_bias_deg,
        "az_random_deg": az_random_deg,
        "el_random_deg": el_random_deg,
        "pos_bias_m": pos_bias_m,
        "pos_random_m": pos_random_m,
        "features": mean_features,
    }


def collect(split: str) -> list[dict]:
    records = []
    for distance in DISTANCES:
        for index in range(GEOMETRIES_PER_DISTANCE):
            position, env = geometry(distance, index, split)
            records.append(decompose_geometry(position, env, distance, index, split))
    return records
