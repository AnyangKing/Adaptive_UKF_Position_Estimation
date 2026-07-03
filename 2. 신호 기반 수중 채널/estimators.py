"""원시 8채널 신호에서 TOA와 배열 DOA를 추정한다."""

from __future__ import annotations

import numpy as np
from scipy.signal import correlate, correlation_lags, find_peaks

from channel import make_probe
from config import ChannelConfig, usb_array_global_m


def _parabolic_peak(values: np.ndarray, index: int) -> float:
    """상관 peak를 3점 포물선으로 보간한 fractional index."""
    if index <= 0 or index >= len(values) - 1:
        return float(index)
    left, center, right = values[index - 1:index + 2]
    denominator = left - 2.0 * center + right
    if abs(denominator) < 1.0e-20:
        return float(index)
    offset = 0.5 * (left - right) / denominator
    return float(index + np.clip(offset, -0.5, 0.5))


def estimate_toa_matched_filter(received: np.ndarray, cfg: ChannelConfig) -> tuple[np.ndarray, np.ndarray]:
    """LOS가 존재하는 기준판에서 가장 강한 상관 peak의 TOA와 quality를 반환한다."""
    probe = make_probe(cfg)
    toas = np.empty(received.shape[0])
    qualities = np.empty(received.shape[0])
    minimum_spacing = max(1, len(probe) // 4)
    for i, signal in enumerate(received):
        correlation = correlate(signal, probe, mode="full", method="fft")
        lags = correlation_lags(len(signal), len(probe), mode="full")
        valid = lags >= 0
        envelope = np.abs(correlation[valid])
        valid_lags = lags[valid]
        peaks, _ = find_peaks(
            envelope,
            height=0.22 * np.max(envelope),
            distance=minimum_spacing,
        )
        if len(peaks) == 0:
            peak = int(np.argmax(envelope))
        else:
            peak = int(peaks[np.argmax(envelope[peaks])])
        fractional_peak = _parabolic_peak(envelope, peak)
        # valid_lags는 연속적인 정수이므로 첫 lag에 보간 index를 더할 수 있다.
        fractional_lag = valid_lags[0] + fractional_peak
        toas[i] = fractional_lag / cfg.sample_rate_hz
        qualities[i] = envelope[peak] / (np.median(envelope) + 1.0e-12)
    return toas, qualities


def estimate_array_doa(toas_s: np.ndarray, cfg: ChannelConfig) -> tuple[float, float, np.ndarray]:
    """센서간 TOA 차이를 평면파 최소제곱으로 결합해 배열 DOA 한 쌍을 구한다."""
    sensors = usb_array_global_m(cfg.receiver_depth_m)
    centered = sensors - sensors.mean(axis=0)
    relative_delays = toas_s - np.mean(toas_s)
    # source 방향 u에 대해 tau_i - mean(tau) ~= -r_i dot u / c
    direction, *_ = np.linalg.lstsq(centered, -cfg.sound_speed_m_s * relative_delays, rcond=None)
    norm = np.linalg.norm(direction)
    if norm < 1.0e-12:
        raise ValueError("DOA direction is unobservable")
    direction /= norm
    azimuth = float(np.arctan2(direction[1], direction[0]))
    elevation = float(np.arctan2(direction[2], np.hypot(direction[0], direction[1])))
    return azimuth, elevation, direction
