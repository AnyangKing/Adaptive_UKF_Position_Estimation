"""신호 기반 얕은 바다 채널의 고정 설정."""

from dataclasses import dataclass
import numpy as np


def usb_array_global_m(receiver_depth_m: float = 30.0) -> np.ndarray:
    """기존 8센서 배열을 기하학적 중심 기준으로 옮겨 전역 좌표에 배치한다."""
    r, height = 0.033, 0.079
    s2 = np.sqrt(2.0)
    local = np.array([
        [r, 0, 0], [r/s2, r/s2, -height], [0, r, 0],
        [-r/s2, r/s2, -height], [-r, 0, 0],
        [-r/s2, -r/s2, -height], [0, -r, 0],
        [r/s2, -r/s2, -height],
    ], dtype=np.float64)
    local -= local.mean(axis=0)
    return local + np.array([0.0, 0.0, -receiver_depth_m])


@dataclass(frozen=True)
class ChannelConfig:
    seed: int = 20260703
    sound_speed_m_s: float = 1500.0
    water_depth_m: float = 100.0
    receiver_depth_m: float = 30.0
    sample_rate_hz: float = 192000.0
    carrier_hz: float = 32000.0
    chirp_bandwidth_hz: float = 12000.0
    pulse_duration_s: float = 0.010
    surface_reflection: float = -0.90
    bottom_reflection: float = 0.60
    snr_db: float = 20.0
    radial_velocity_m_s: float = 0.5
    guard_time_s: float = 0.015
    # --- ③ 채널 현실화 옵션 (기본 off = 기존 3경로 동일) ---
    second_order_multipath: bool = False   # 표면-해저·해저-표면 2차 반사 추가
    surface_roughness: float = 0.0         # 표면 반사경로 진폭·지연 랜덤 섭동 std(거친 표면 산란)
    sound_speed_gradient: float = 0.0      # 음속 깊이 gradient dc/d(depth) [s^-1]; 0이면 직선(등속)

