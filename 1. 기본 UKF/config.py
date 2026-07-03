"""기본 UKF 실험의 고정 설정 (모든 내부 단위: m, s, rad)."""

from dataclasses import dataclass
import numpy as np


def sensor_positions_m() -> np.ndarray:
    """기존 500만 시퀀스 프로젝트의 45도 엇갈린 2단 8센서 배열."""
    r = 0.033
    height = 0.079
    s2 = np.sqrt(2.0)
    return np.array(
        [
            [r, 0.0, 0.0],
            [r / s2, r / s2, -height],
            [0.0, r, 0.0],
            [-r / s2, r / s2, -height],
            [-r, 0.0, 0.0],
            [-r / s2, -r / s2, -height],
            [0.0, -r, 0.0],
            [r / s2, -r / s2, -height],
        ],
        dtype=np.float64,
    )


@dataclass(frozen=True)
class Config:
    seed: int = 20260703
    dt_s: float = 1.0
    num_steps: int = 200
    step_length_m: float = 1.0
    start_distance_m: float = 100.0
    sound_speed_m_s: float = 1500.0
    direction_memory: float = 0.8
    acceleration_std_m_s2: float = 0.35
    # 무잡음 시험에서도 혁신 공분산의 특이행렬화를 막기 위한 수치 바닥값이다.
    range_std_m: float = 1.0e-3
    angle_std_rad: float = 1.0e-5

