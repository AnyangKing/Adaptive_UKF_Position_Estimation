"""수중 이동 궤적의 원시 신호 생성부터 UKF까지 end-to-end 실행."""

from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position, signal_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


def trajectory(steps: int = 30) -> np.ndarray:
    t = np.arange(steps, dtype=float)
    return np.column_stack((100.0 + 0.75*t, 20.0 + 0.35*t,
                            -20.0 - 0.10*t + 0.4*np.sin(t/8.0)))


def run() -> dict[str, float]:
    cfg = ChannelConfig()
    truth = trajectory()
    observations = []
    for position in truth:
        _, received, _ = synthesize_received(position, cfg)
        z, _ = signal_measurement(received, cfg)
        observations.append(z)
    observations = np.asarray(observations)

    initial_position = initialize_position(observations[0], cfg)
    state = np.r_[initial_position, np.zeros(3)]
    ukf = SignalObservationUKF(
        state,
        np.diag([5.0**2]*3 + [1.0**2]*3),
        acceleration_process_covariance(1.0, 0.20),
        fixed_measurement_covariance(),
        cfg,
    )
    estimates = np.zeros_like(truth); estimates[0] = initial_position
    for k in range(1, len(truth)):
        estimates[k] = ukf.step(observations[k])[:3]
    errors = np.linalg.norm(estimates - truth, axis=1)
    metrics = {
        "initial_error_m": float(errors[0]),
        "rmse_all_m": float(np.sqrt(np.mean(errors**2))),
        "rmse_after_5_m": float(np.sqrt(np.mean(errors[5:]**2))),
        "maximum_error_m": float(np.max(errors)),
        "final_error_m": float(errors[-1]),
    }
    output = Path(__file__).resolve().parent / "results"; output.mkdir(exist_ok=True)
    np.savez(output / "signal_ukf_smoke.npz", truth=truth, observations=observations,
             estimates=estimates, errors=errors)
    (output / "signal_ukf_smoke.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2)); return metrics


if __name__ == "__main__":
    run()
