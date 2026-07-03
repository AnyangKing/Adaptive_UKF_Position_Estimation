"""신호 생성과 TOA/DOA 복원의 단일 시나리오 smoke test."""

from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig, usb_array_global_m
from estimators import estimate_array_doa, estimate_toa_matched_filter


def angle_error_deg(a: float, b: float) -> float:
    return float(np.degrees(abs((a - b + np.pi) % (2 * np.pi) - np.pi)))


def run() -> dict[str, float]:
    cfg = ChannelConfig()
    source = np.array([100.0, 20.0, -20.0])
    time, received, paths = synthesize_received(source, cfg)
    estimated_toa, quality = estimate_toa_matched_filter(received, cfg)
    true_toa = np.array([sensor_paths[0].delay_s for sensor_paths in paths])
    azimuth, elevation, direction = estimate_array_doa(estimated_toa, cfg)
    center = usb_array_global_m(cfg.receiver_depth_m).mean(axis=0)
    true_direction = source - center
    true_direction /= np.linalg.norm(true_direction)
    true_azimuth = float(np.arctan2(true_direction[1], true_direction[0]))
    true_elevation = float(np.arctan2(true_direction[2], np.hypot(true_direction[0], true_direction[1])))
    toa_error = estimated_toa - true_toa
    metrics = {
        "toa_rmse_us": float(np.sqrt(np.mean(toa_error**2)) * 1e6),
        "tdoa_rmse_us": float(np.sqrt(np.mean(((toa_error - toa_error[0]))**2)) * 1e6),
        "azimuth_error_deg": angle_error_deg(azimuth, true_azimuth),
        "elevation_error_deg": angle_error_deg(elevation, true_elevation),
        "minimum_peak_quality": float(np.min(quality)),
    }
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    np.savez(output / "channel_smoke.npz", time=time, received=received,
             estimated_toa=estimated_toa, true_toa=true_toa, direction=direction)
    (output / "channel_smoke.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    run()

