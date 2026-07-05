"""원시 신호와 상태 위치 사이의 공통 10차원 관측 정의."""

from __future__ import annotations

import numpy as np

from config import ChannelConfig, usb_array_global_m
from estimators import (
    estimate_gcc_phat_doa,
    estimate_srp_phat_doa,
    estimate_toa_matched_filter,
    pair_delays_to_reference_tdoa,
)


def wrap_angle(value: np.ndarray | float) -> np.ndarray | float:
    return (value + np.pi) % (2.0 * np.pi) - np.pi


def ideal_measurement(position_m: np.ndarray, cfg: ChannelConfig) -> np.ndarray:
    sensors = usb_array_global_m(cfg.receiver_depth_m)
    ranges = np.linalg.norm(np.asarray(position_m) - sensors, axis=1)
    center = sensors.mean(axis=0)
    delta = np.asarray(position_m) - center
    azimuth = np.arctan2(delta[1], delta[0])
    elevation = np.arctan2(delta[2], np.hypot(delta[0], delta[1]))
    return np.r_[ranges[0], ranges[1:] - ranges[0], azimuth, elevation]


def signal_measurement(received: np.ndarray, cfg: ChannelConfig) -> tuple[np.ndarray, dict[str, float]]:
    absolute_toas, peak_quality = estimate_toa_matched_filter(received, cfg)
    azimuth, elevation, _, pair_delays = estimate_gcc_phat_doa(received, cfg)
    srp_azimuth, srp_elevation, srp_direction, _ = estimate_srp_phat_doa(received, cfg)
    gcc_direction = np.array([
        np.cos(elevation) * np.cos(azimuth),
        np.cos(elevation) * np.sin(azimuth),
        np.sin(elevation),
    ])
    disagreement_deg = np.degrees(
        np.arccos(np.clip(gcc_direction @ srp_direction, -1.0, 1.0))
    )
    reference_tdoa = pair_delays_to_reference_tdoa(pair_delays)
    z = np.r_[
        cfg.sound_speed_m_s * absolute_toas[0],
        cfg.sound_speed_m_s * reference_tdoa,
        azimuth,
        elevation,
    ]
    quality = {
        "reference_peak_quality": float(peak_quality[0]),
        "minimum_peak_quality": float(np.min(peak_quality)),
        "doa_disagreement_deg": float(disagreement_deg),
        "srp_azimuth_rad": float(srp_azimuth),
        "srp_elevation_rad": float(srp_elevation),
    }
    return z, quality


def initialize_position(measurement: np.ndarray, cfg: ChannelConfig) -> np.ndarray:
    """배열 DOA ray와 sensor 0 거리 sphere의 양의 교점을 사용한다."""
    sensors = usb_array_global_m(cfg.receiver_depth_m)
    center = sensors.mean(axis=0)
    azimuth, elevation = measurement[8], measurement[9]
    direction = np.array([
        np.cos(elevation) * np.cos(azimuth),
        np.cos(elevation) * np.sin(azimuth),
        np.sin(elevation),
    ])
    offset = center - sensors[0]
    radius = measurement[0]
    b = 2.0 * direction @ offset
    c = offset @ offset - radius**2
    discriminant = max(0.0, b**2 - 4.0 * c)
    roots = [(-b + np.sqrt(discriminant)) / 2.0, (-b - np.sqrt(discriminant)) / 2.0]
    distance = max(roots)
    return center + distance * direction


def fixed_measurement_covariance(
    toa_range_std_m: float = 0.03,
    tdoa_sensor_std_m: float = 0.025,
    doa_std_deg: float = 2.0,
) -> np.ndarray:
    """sensor 0 기준 TDOA의 공유오차를 포함한 기준 R."""
    covariance = np.zeros((10, 10))
    covariance[0, 0] = toa_range_std_m**2
    # d_i=e_i-e_0 이므로 diag=2 sigma^2, offdiag=sigma^2.
    covariance[1:8, 1:8] = tdoa_sensor_std_m**2 * (
        np.eye(7) + np.ones((7, 7))
    )
    angle_variance = np.radians(doa_std_deg) ** 2
    covariance[8, 8] = covariance[9, 9] = angle_variance
    return covariance
