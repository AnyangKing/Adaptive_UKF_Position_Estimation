"""무잡음 기본 UKF 실행 및 결과 저장."""

from pathlib import Path
import json

import numpy as np

from config import Config
from simulator import generate_observations, generate_trajectory, initialize_position_from_observation
from ukf import UKF, constant_acceleration_process_covariance


def run() -> dict[str, float]:
    cfg = Config()
    truth = generate_trajectory(cfg)
    observations = generate_observations(truth)
    initial_position = initialize_position_from_observation(observations[0])
    initial_state = np.r_[initial_position, np.zeros(3)]
    initial_covariance = np.diag([0.05**2] * 3 + [1.0**2] * 3)
    process_covariance = constant_acceleration_process_covariance(
        cfg.dt_s, cfg.acceleration_std_m_s2
    )
    measurement_covariance = np.diag(
        [cfg.range_std_m**2] * 8 + [cfg.angle_std_rad**2] * 16
    )
    ukf = UKF(
        initial_state,
        initial_covariance,
        process_covariance,
        measurement_covariance,
        cfg.dt_s,
    )

    estimates = np.zeros_like(truth)
    estimates[0] = initial_position
    for k in range(1, cfg.num_steps):
        estimates[k] = ukf.step(observations[k])[:3]

    errors = np.linalg.norm(estimates - truth, axis=1)
    metrics = {
        "rmse_m": float(np.sqrt(np.mean(errors**2))),
        "mean_error_m": float(np.mean(errors)),
        "max_error_m": float(np.max(errors)),
        "final_error_m": float(errors[-1]),
    }
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    np.savez(output / "noiseless_smoke.npz", truth=truth, estimates=estimates, errors=errors)
    (output / "noiseless_smoke.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    run()

