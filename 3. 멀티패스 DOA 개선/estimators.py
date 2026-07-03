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


def _gcc_phat_correlation(
    signal_i: np.ndarray, signal_j: np.ndarray, cfg: ChannelConfig
) -> tuple[np.ndarray, np.ndarray]:
    """송신 chirp 대역만 사용하는 PHAT 정규화 상호상관."""
    required = len(signal_i) + len(signal_j) - 1
    nfft = 1 << (required - 1).bit_length()
    spectrum_i = np.fft.rfft(signal_i, n=nfft)
    spectrum_j = np.fft.rfft(signal_j, n=nfft)
    frequencies = np.fft.rfftfreq(nfft, 1.0 / cfg.sample_rate_hz)
    low = cfg.carrier_hz - cfg.chirp_bandwidth_hz / 2.0
    high = cfg.carrier_hz + cfg.chirp_bandwidth_hz / 2.0
    band = (frequencies >= low) & (frequencies <= high)
    cross = spectrum_i * np.conj(spectrum_j)
    phat = np.zeros_like(cross)
    phat[band] = cross[band] / (np.abs(cross[band]) + 1.0e-15)
    correlation = np.fft.fftshift(np.fft.irfft(phat, n=nfft))
    lags_s = (np.arange(nfft) - nfft // 2) / cfg.sample_rate_hz
    return lags_s, correlation


def estimate_gcc_phat_doa(
    received: np.ndarray, cfg: ChannelConfig
) -> tuple[float, float, np.ndarray, np.ndarray]:
    """모든 28개 센서쌍 GCC-PHAT 지연의 최소제곱 DOA."""
    sensors = usb_array_global_m(cfg.receiver_depth_m)
    rows, values, pair_delays = [], [], []
    maximum_lag_s = np.max(
        np.linalg.norm(sensors[:, None, :] - sensors[None, :, :], axis=2)
    ) / cfg.sound_speed_m_s
    for i in range(8):
        for j in range(i + 1, 8):
            lags, correlation = _gcc_phat_correlation(received[i], received[j], cfg)
            valid = np.abs(lags) <= 1.15 * maximum_lag_s
            local_lags = lags[valid]
            local_values = correlation[valid]
            peak = int(np.argmax(local_values))
            fractional = _parabolic_peak(local_values, peak)
            delay = local_lags[0] + fractional / cfg.sample_rate_hz
            rows.append(sensors[i] - sensors[j])
            values.append(-cfg.sound_speed_m_s * delay)
            pair_delays.append(delay)
    direction, *_ = np.linalg.lstsq(np.asarray(rows), np.asarray(values), rcond=None)
    direction /= np.linalg.norm(direction)
    azimuth = float(np.arctan2(direction[1], direction[0]))
    elevation = float(np.arctan2(direction[2], np.hypot(direction[0], direction[1])))
    return azimuth, elevation, direction, np.asarray(pair_delays)


def _direction_grid(azimuth_deg: np.ndarray, elevation_deg: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    azimuth, elevation = np.meshgrid(np.radians(azimuth_deg), np.radians(elevation_deg))
    directions = np.column_stack((
        np.cos(elevation).ravel() * np.cos(azimuth).ravel(),
        np.cos(elevation).ravel() * np.sin(azimuth).ravel(),
        np.sin(elevation).ravel(),
    ))
    return directions, azimuth.ravel(), elevation.ravel()


def _srp_scores(received: np.ndarray, directions: np.ndarray, cfg: ChannelConfig) -> np.ndarray:
    sensors = usb_array_global_m(cfg.receiver_depth_m)
    scores = np.zeros(len(directions))
    for i in range(8):
        for j in range(i + 1, 8):
            lags, correlation = _gcc_phat_correlation(received[i], received[j], cfg)
            predicted = -(directions @ (sensors[i] - sensors[j])) / cfg.sound_speed_m_s
            scores += np.interp(predicted, lags, correlation, left=0.0, right=0.0)
    return scores


def estimate_srp_phat_doa(
    received: np.ndarray, cfg: ChannelConfig
) -> tuple[float, float, np.ndarray, float]:
    """2도 전역 탐색 후 0.2도 국소 탐색하는 3D broadband SRP-PHAT."""
    coarse_directions, coarse_az, coarse_el = _direction_grid(
        np.arange(-180.0, 180.0, 2.0), np.arange(-80.0, 82.0, 2.0)
    )
    coarse_scores = _srp_scores(received, coarse_directions, cfg)
    coarse_best = int(np.argmax(coarse_scores))
    center_az = np.degrees(coarse_az[coarse_best])
    center_el = np.degrees(coarse_el[coarse_best])
    fine_directions, fine_az, fine_el = _direction_grid(
        np.arange(center_az - 2.0, center_az + 2.01, 0.2),
        np.arange(max(-89.0, center_el - 2.0), min(89.0, center_el + 2.0) + 0.01, 0.2),
    )
    fine_scores = _srp_scores(received, fine_directions, cfg)
    best = int(np.argmax(fine_scores))
    return float(fine_az[best]), float(fine_el[best]), fine_directions[best], float(fine_scores[best])
