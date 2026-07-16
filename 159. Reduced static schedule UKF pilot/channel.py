"""직접파와 1회 경계 반사를 포함한 8채널 수중 음향 신호 생성기."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.signal import chirp, windows

from config import ChannelConfig, usb_array_global_m


@dataclass(frozen=True)
class Path:
    name: str
    distance_m: float
    delay_s: float
    amplitude: float


def make_probe(cfg: ChannelConfig) -> np.ndarray:
    count = int(round(cfg.pulse_duration_s * cfg.sample_rate_hz))
    t = np.arange(count) / cfg.sample_rate_hz
    f0 = cfg.carrier_hz - cfg.chirp_bandwidth_hz / 2.0
    f1 = cfg.carrier_hz + cfg.chirp_bandwidth_hz / 2.0
    signal = chirp(t, f0=f0, f1=f1, t1=cfg.pulse_duration_s, method="linear")
    signal *= windows.tukey(count, alpha=0.2)
    return signal / np.sqrt(np.mean(signal**2))


def thorp_absorption_db_per_km(frequency_hz: float) -> float:
    """Thorp 근사식. 주파수 범위 확인을 쉽게 하려고 독립 함수로 둔다."""
    f = frequency_hz / 1000.0
    return (
        0.11 * f**2 / (1.0 + f**2)
        + 44.0 * f**2 / (4100.0 + f**2)
        + 2.75e-4 * f**2
        + 0.003
    )


def _path_amplitude(distance_m: float, reflection: float, cfg: ChannelConfig) -> float:
    absorption_db = thorp_absorption_db_per_km(cfg.carrier_hz) * distance_m / 1000.0
    return reflection * (1.0 / max(distance_m, 1.0)) * 10.0 ** (-absorption_db / 20.0)


def paths_for_sensor(source_m: np.ndarray, sensor_m: np.ndarray, cfg: ChannelConfig) -> list[Path]:
    """직접파, 평면 해수면 반사, 평면 해저 반사의 image-source 경로."""
    source = np.asarray(source_m, dtype=np.float64)
    surface_image = source.copy()
    surface_image[2] = -source[2]
    bottom_image = source.copy()
    bottom_image[2] = -2.0 * cfg.water_depth_m - source[2]
    specifications = [
        ("direct", source, 1.0),
        ("surface", surface_image, cfg.surface_reflection),
        ("bottom", bottom_image, cfg.bottom_reflection),
    ]
    result = []
    for name, image, reflection in specifications:
        distance = float(np.linalg.norm(image - sensor_m))
        result.append(Path(name, distance, distance / cfg.sound_speed_m_s,
                           _path_amplitude(distance, reflection, cfg)))
    return result


def _colored_noise(count: int, cfg: ChannelConfig, rng: np.random.Generator) -> np.ndarray:
    """Wenz 계열 성분의 주파수 경향을 흉내 낸 정규화 유색잡음."""
    frequencies = np.fft.rfftfreq(count, 1.0 / cfg.sample_rate_hz)
    fk = np.maximum(frequencies / 1000.0, 0.01)
    # 저주파 선박/파랑 성분과 고주파 열잡음 성분의 합성 상대 PSD.
    shipping = fk ** -3.4 / (1.0 + (fk / 0.5) ** 4)
    wind = fk ** -1.7 / (1.0 + (fk / 30.0) ** 2)
    thermal = 1.0e-5 * fk**2
    psd = shipping + wind + thermal
    spectrum = (rng.normal(size=len(frequencies)) + 1j * rng.normal(size=len(frequencies)))
    spectrum *= np.sqrt(psd)
    spectrum[0] = 0.0
    noise = np.fft.irfft(spectrum, n=count)
    return noise / (np.std(noise) + 1.0e-15)


def synthesize_received(
    source_m: np.ndarray,
    cfg: ChannelConfig,
    include_multipath: bool = True,
    include_noise: bool = True,
) -> tuple[np.ndarray, np.ndarray, list[list[Path]]]:
    """(시간, [8, samples] 수신 신호, 센서별 경로)를 반환한다."""
    source = np.asarray(source_m, dtype=np.float64)
    if not (-cfg.water_depth_m < source[2] < 0.0):
        raise ValueError("source z must lie between seabed and surface")
    sensors = usb_array_global_m(cfg.receiver_depth_m)
    all_paths = [paths_for_sensor(source, sensor, cfg) for sensor in sensors]
    maximum_delay = max(path.delay_s for paths in all_paths for path in paths)
    duration = maximum_delay + cfg.pulse_duration_s + cfg.guard_time_s
    count = int(np.ceil(duration * cfg.sample_rate_hz))
    time = np.arange(count) / cfg.sample_rate_hz
    probe = make_probe(cfg)
    probe_time = np.arange(len(probe)) / cfg.sample_rate_hz
    received = np.zeros((8, count), dtype=np.float64)
    doppler = cfg.radial_velocity_m_s / cfg.sound_speed_m_s

    for sensor_index, paths in enumerate(all_paths):
        active = paths if include_multipath else paths[:1]
        for path in active:
            warped_time = (time - path.delay_s) * (1.0 + doppler)
            received[sensor_index] += path.amplitude * np.interp(
                warped_time, probe_time, probe, left=0.0, right=0.0
            )

    if include_noise:
        rng = np.random.default_rng(cfg.seed)
        direct_power = np.mean([
            (paths[0].amplitude**2) * np.mean(probe**2) for paths in all_paths
        ])
        target_noise_std = np.sqrt(direct_power / (10.0 ** (cfg.snr_db / 10.0)))
        for i in range(8):
            received[i] += target_noise_std * _colored_noise(count, cfg, rng)
    return time, received, all_paths

