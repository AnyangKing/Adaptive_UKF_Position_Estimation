"""동일 원시 신호 관측에서 fixed R과 adaptive R UKF를 비교한다."""

from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position, signal_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


def trajectory(steps=30):
    t = np.arange(steps, dtype=float)
    return np.column_stack((100.0 + 0.75*t, 20.0 + 0.35*t,
                            -20.0 - 0.10*t + 0.4*np.sin(t/8.0)))


def make_filter(initial_position, cfg):
    return SignalObservationUKF(
        np.r_[initial_position, np.zeros(3)],
        np.diag([5.0**2]*3 + [1.0**2]*3),
        acceleration_process_covariance(1.0, 0.20),
        fixed_measurement_covariance(), cfg,
    )


def metrics(estimates, truth):
    errors = np.linalg.norm(estimates - truth, axis=1)
    return {
        "rmse_all_m": float(np.sqrt(np.mean(errors**2))),
        "rmse_after_5_m": float(np.sqrt(np.mean(errors[5:]**2))),
        "max_error_m": float(np.max(errors)),
        "final_error_m": float(errors[-1]),
    }, errors


def run():
    cfg = ChannelConfig(); truth = trajectory()
    observations, qualities = [], []
    for position in truth:
        _, received, _ = synthesize_received(position, cfg)
        z, quality = signal_measurement(received, cfg)
        observations.append(z); qualities.append(quality)
    observations = np.asarray(observations)
    initial = initialize_position(observations[0], cfg)
    fixed = make_filter(initial, cfg)
    adaptive = AdaptiveRUKF(make_filter(initial, cfg))
    fixed_est = np.zeros_like(truth); adaptive_est = np.zeros_like(truth)
    fixed_est[0] = adaptive_est[0] = initial
    for k in range(1, len(truth)):
        fixed_est[k] = fixed.step(observations[k])[:3]
        adaptive_est[k] = adaptive.step(observations[k], qualities[k])[:3]
    fixed_metrics, fixed_errors = metrics(fixed_est, truth)
    adaptive_metrics, adaptive_errors = metrics(adaptive_est, truth)
    history = adaptive.history
    result = {
        "fixed": fixed_metrics,
        "adaptive": adaptive_metrics,
        "improvement_after_5_percent": 100.0 * (
            fixed_metrics["rmse_after_5_m"] - adaptive_metrics["rmse_after_5_m"]
        ) / fixed_metrics["rmse_after_5_m"],
        "mean_doa_disagreement_deg": float(np.mean([h["doa_disagreement_deg"] for h in history])),
        "mean_doa_quality_scale": float(np.mean([h["doa_quality_scale"] for h in history])),
        "maximum_doa_nis": float(np.max([h["doa_nis"] for h in history])),
        "maximum_tdoa_nis": float(np.max([h["tdoa_nis"] for h in history])),
        "doa_gate_activation_rate": float(np.mean([h["doa_gate_scale"] > 1 for h in history])),
        "tdoa_gate_activation_rate": float(np.mean([h["tdoa_gate_scale"] > 1 for h in history])),
    }
    output = Path(__file__).resolve().parent / "results"; output.mkdir(exist_ok=True)
    (output / "adaptive_comparison.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    np.savez(output / "adaptive_comparison.npz", truth=truth, fixed=fixed_est,
             adaptive=adaptive_est, fixed_errors=fixed_errors, adaptive_errors=adaptive_errors)
    print(json.dumps(result, indent=2)); return result


if __name__ == "__main__":
    run()
