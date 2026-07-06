"""다중 ping/다중 시점 기하가 계통 고도각 편향을 더 관측가능하게 만드는지 진단한다.

37~41은 단일 ping peak_margin 신호가 약해 measurement 처리로 장거리 오차를 못 고침을 보였다.
남은 갈래는 '기하 다양화'다: 소스가 이동하면 배열-소스 기하가 바뀌는데, 그때 계통 편향이
(A) 한 궤적 안에서 ping마다 얼마나 변하는지(=평균으로 지워지는지), (B) 큰 기하 변화(방위 회전)로
얼마나 탈상관되는지를 GT를 label로만 써서 측정한다.

- 편향이 궤적 안에서 거의 상수면(A) 다중 ping 평균이 무력하다.
- 큰 방위 회전에도 편향이 강하게 상관돼 있으면(B) 어떤 기동으로도 blind 평균이 편향을 못 지운다.
- 반대로 회전으로 탈상관되면 다중 시점(다중 트랙) 융합이 원리상 편향을 줄일 수 있다.
"""

from __future__ import annotations

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from measurement import ideal_measurement
from peak_measurement import extract_measurement

DISTANCES = (100, 200, 400, 600)
AZIMUTH_OFFSETS_DEG = (0.0, 10.0, 30.0, 60.0, 90.0, 120.0, 180.0)
POINTS_PER_DISTANCE = 10     # part B: 거리당 소스 점 수
REPEATS = 4                  # noise 평균 반복 (37에서 random≈0이라 소수로 충분)
TRACK_STEPS = 10             # part A: 한 궤적의 ping 수
TRACKS_PER_DISTANCE = 8
GEOM_ROOT = 420000
NOISE_ROOT = 423000


def _el_bias_rad(position, env, seed):
    """한 관측(고정 위치·환경·noise seed)의 고도각 편향 = 측정 - 참."""
    cfg = replace(ChannelConfig(), seed=seed, **env)
    _, received, _ = synthesize_received(position, cfg)
    z, _ = extract_measurement(received, cfg)
    true_el = float(ideal_measurement(position, cfg)[9])
    return float(z[9] - true_el)


def _env(rng):
    return dict(
        snr_db=float(rng.choice([10.0, 20.0, 30.0])),
        surface_reflection=float(-rng.uniform(0.72, 0.97)),
        bottom_reflection=float(rng.uniform(0.32, 0.78)),
        radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)),
    )


def _mean_bias(position, env, seed0):
    return float(np.mean([_el_bias_rad(position, env, seed0 + r) for r in range(REPEATS)]))


# -------- Part A: 한 궤적 안에서 편향의 지속성(평균 소거 가능성) --------

def within_track(distance, track):
    """등속 궤적을 따라 ping별 noise-평균 편향을 모아 within-track 통계를 낸다."""
    rng = np.random.default_rng(GEOM_ROOT + distance * 100 + track)
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    start = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
    tangent = np.array([-np.sin(az), np.cos(az), 0.0])
    speed = rng.uniform(0.4, 1.2); vz = rng.uniform(-0.08, 0.08)
    env = _env(rng)
    velocity = np.r_[speed * tangent[:2], vz]
    biases = []
    for k in range(TRACK_STEPS):
        pos = start + k * velocity
        seed = NOISE_ROOT + distance * 1000 + track * 50 + k * 5
        biases.append(np.degrees(_mean_bias(pos, env, seed)))
    biases = np.asarray(biases)
    signed_mean = float(np.mean(biases))
    end = start + (TRACK_STEPS - 1) * velocity
    bearing_change = float(np.degrees(abs((np.arctan2(end[1], end[0])
                                           - np.arctan2(start[1], start[0]) + np.pi)
                                          % (2 * np.pi) - np.pi)))
    return {
        "distance": distance,
        "mean_abs_bias_deg": float(np.mean(np.abs(biases))),
        "signed_mean_bias_deg": signed_mean,
        "within_track_std_deg": float(np.std(biases)),
        # 평균 소거 지표: |ping 평균| / 평균|ping| ~ 1이면 같은 부호로 상수(평균 무력)
        "averaging_retention": float(abs(signed_mean) / (np.mean(np.abs(biases)) + 1e-9)),
        "bearing_change_deg": bearing_change,
    }


# -------- Part B: 큰 방위 회전에 따른 편향 탈상관 --------

def azimuth_rotation(distance, point):
    """같은 거리·깊이의 소스를 방위만 Δ 회전시켜 관측한 noise-평균 편향들을 낸다."""
    rng = np.random.default_rng(GEOM_ROOT + 500000 + distance * 100 + point)
    base_az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    env = _env(rng)
    biases = {}
    for j, offset in enumerate(AZIMUTH_OFFSETS_DEG):
        az = base_az + np.radians(offset)
        pos = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
        seed = NOISE_ROOT + 600000 + distance * 1000 + point * 50 + j * 5
        biases[offset] = np.degrees(_mean_bias(pos, env, seed))
    return biases


def collect_within(distances=DISTANCES):
    return [within_track(d, t) for d in distances for t in range(TRACKS_PER_DISTANCE)]


def collect_rotation(distances=DISTANCES):
    return {d: [azimuth_rotation(d, p) for p in range(POINTS_PER_DISTANCE)] for d in distances}
