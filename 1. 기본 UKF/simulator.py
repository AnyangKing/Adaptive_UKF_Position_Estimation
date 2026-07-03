"""기존 실험 조건을 SI 단위로 재작성한 독립 시뮬레이터."""

from __future__ import annotations

import numpy as np

from config import Config, sensor_positions_m


def wrap_angle(angle: np.ndarray) -> np.ndarray:
    return (angle + np.pi) % (2.0 * np.pi) - np.pi


def generate_trajectory(cfg: Config) -> np.ndarray:
    """기존 코드와 같은 200시점/1 m step의 완만한 무작위 3D 궤적."""
    rng = np.random.default_rng(cfg.seed)
    trajectory = np.zeros((cfg.num_steps, 3), dtype=np.float64)
    radial = rng.normal(size=3)
    radial /= np.linalg.norm(radial)
    # 과거 비교 조건 재현: 배열 중심이 아니라 좌표 원점 기준 거리이다.
    trajectory[0] = radial * cfg.start_distance_m

    direction = rng.normal(size=3)
    direction /= np.linalg.norm(direction)
    for k in range(1, cfg.num_steps):
        random_direction = rng.normal(size=3)
        random_direction /= np.linalg.norm(random_direction)
        direction = (
            cfg.direction_memory * direction
            + (1.0 - cfg.direction_memory) * random_direction
        )
        direction /= np.linalg.norm(direction)
        trajectory[k] = trajectory[k - 1] + cfg.step_length_m * direction
    return trajectory


def observation_from_position(
    position_m: np.ndarray, sensors_m: np.ndarray | None = None
) -> np.ndarray:
    """[거리 8, 방위각 8, 고도각 8] 관측을 반환한다."""
    sensors = sensor_positions_m() if sensors_m is None else sensors_m
    delta = np.asarray(position_m, dtype=np.float64) - sensors
    ranges = np.linalg.norm(delta, axis=1)
    azimuth = np.arctan2(delta[:, 1], delta[:, 0])
    elevation = np.arctan2(delta[:, 2], np.hypot(delta[:, 0], delta[:, 1]))
    return np.concatenate((ranges, azimuth, elevation))


def generate_observations(
    trajectory_m: np.ndarray,
    range_noise_std_m: float = 0.0,
    angle_noise_std_rad: float = 0.0,
    seed: int = 0,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    observations = np.vstack([observation_from_position(p) for p in trajectory_m])
    if range_noise_std_m > 0.0:
        observations[:, :8] += rng.normal(0.0, range_noise_std_m, (len(observations), 8))
    if angle_noise_std_rad > 0.0:
        observations[:, 8:] += rng.normal(0.0, angle_noise_std_rad, (len(observations), 16))
        observations[:, 8:] = wrap_angle(observations[:, 8:])
    return observations


def initialize_position_from_observation(
    observation: np.ndarray, sensors_m: np.ndarray | None = None
) -> np.ndarray:
    """S0의 절대거리와 두 각만 이용하는 측정 기반 초기 위치."""
    sensors = sensor_positions_m() if sensors_m is None else sensors_m
    distance = observation[0]
    azimuth = observation[8]
    elevation = observation[16]
    direction = np.array(
        [
            np.cos(elevation) * np.cos(azimuth),
            np.cos(elevation) * np.sin(azimuth),
            np.sin(elevation),
        ]
    )
    return sensors[0] + distance * direction

