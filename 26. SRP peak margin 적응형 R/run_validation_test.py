"""Peak-margin 정책을 validation에서 선택하고 별도 test 궤적에 고정 적용."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.stats import spearmanr

from channel import synthesize_received
from config import ChannelConfig, usb_array_global_m
from measurement import fixed_measurement_covariance, initialize_position
from peak_adaptive import PeakMarginAdaptiveRUKF
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


DISTANCES = (100, 200, 400, 600); STEPS = 10


def trajectory(distance, split):
    rng = np.random.default_rng((261000 if split == "validation" else 262000) + distance)
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    start = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
    tangent = np.array([-np.sin(az), np.cos(az), 0.0]); radial = np.array([np.cos(az), np.sin(az), 0.0])
    t = np.arange(STEPS, dtype=float)
    truth = start + t[:, None] * (0.72 * tangent + rng.uniform(-0.2, 0.2) * radial)
    meta = {
        "snr_db": float(rng.choice([10.0, 20.0, 30.0])),
        "surface_reflection": float(-rng.uniform(0.72, 0.97)),
        "bottom_reflection": float(rng.uniform(0.32, 0.78)),
        "radial_velocity_m_s": float(rng.uniform(-1.3, 1.3)),
    }
    return truth, meta


def collect(split):
    base = ChannelConfig(); data = {}; center = usb_array_global_m().mean(axis=0)
    seed_root = 263000 if split == "validation" else 264000
    for distance in DISTANCES:
        truth, meta = trajectory(distance, split); observations = []; qualities = []; angular_errors = []
        for k, position in enumerate(truth):
            cfg = replace(base, seed=seed_root + distance * 10 + k, **meta)
            _, received, _ = synthesize_received(position, cfg); z, q = extract_measurement(received, cfg)
            observations.append(z); qualities.append(q)
            estimate = np.array([np.cos(z[9]) * np.cos(z[8]), np.cos(z[9]) * np.sin(z[8]), np.sin(z[9])])
            actual = position - center; actual /= np.linalg.norm(actual)
            angular_errors.append(float(np.degrees(np.arccos(np.clip(estimate @ actual, -1.0, 1.0)))))
        data[distance] = (truth, np.asarray(observations), qualities, np.asarray(angular_errors))
    return base, data


def make_filter(initial, cfg):
    return SignalObservationUKF(
        np.r_[initial, np.zeros(3)], np.diag([8.0**2] * 3 + [1.5**2] * 3),
        acceleration_process_covariance(1.0, 0.20), fixed_measurement_covariance(), cfg
    )


def evaluate(dataset, cfg, threshold=None, scale=1.0):
    truth, observations, qualities, _ = dataset; initial = initialize_position(observations[0], cfg)
    wrapper = PeakMarginAdaptiveRUKF(make_filter(initial, cfg), threshold, scale)
    estimate = np.zeros_like(truth); estimate[0] = initial
    for k in range(1, len(truth)):
        estimate[k] = wrapper.step(observations[k], qualities[k])[:3]
    error = np.linalg.norm(estimate - truth, axis=1)
    return {
        "rmse_after_3_m": float(np.sqrt(np.mean(error[3:]**2))),
        "max_error_m": float(np.max(error)),
        "final_error_m": float(error[-1]),
        "diverged_over_50m": bool(np.any(error > 50.0)),
        "low_margin_rate": float(np.mean([h["low_margin"] for h in wrapper.history])),
    }


def validate():
    cfg, data = collect("validation")
    margins = np.array([q["peak_margin"] for d in DISTANCES for q in data[d][2]])
    errors = np.concatenate([data[d][3] for d in DISTANCES])
    quantiles = {"q25": float(np.percentile(margins, 25)), "q50": float(np.percentile(margins, 50))}
    policies = [("baseline", None, 1.0)]
    for label, threshold in quantiles.items():
        for scale in (4.0, 16.0):
            policies.append((f"{label}_x{int(scale)}", threshold, scale))
    scores = {}
    for name, threshold, scale in policies:
        records = {str(d): evaluate(data[d], cfg, threshold, scale) for d in DISTANCES}
        values = [r["rmse_after_3_m"] for r in records.values()]
        robust = float(np.mean(values) + 0.25 * np.max(values) + 100 * sum(r["diverged_over_50m"] for r in records.values()))
        scores[name] = {"threshold": threshold, "scale": scale, "robust_score": robust,
                        "mean_rmse_m": float(np.mean(values)), "worst_rmse_m": float(np.max(values)), "records": records}
    selected = min(scores, key=lambda name: scores[name]["robust_score"])
    correlation = spearmanr(margins, errors)
    return selected, scores, quantiles, {"spearman_rho": float(correlation.statistic), "pvalue": float(correlation.pvalue)}


def run():
    selected, scores, quantiles, correlation = validate(); cfg, test_data = collect("test")
    chosen = scores[selected]
    test = {str(d): {
        "baseline": evaluate(test_data[d], cfg),
        "selected": evaluate(test_data[d], cfg, chosen["threshold"], chosen["scale"]),
    } for d in DISTANCES}
    payload = {"selection": {"selected": selected, "quantiles": quantiles,
        "margin_error_correlation": correlation, "validation": scores}, "test": test}
    output = Path(__file__).resolve().parent / "results"; output.mkdir(exist_ok=True)
    (output / "peak_margin_policy.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2)); return payload


if __name__ == "__main__":
    run()
