"""다중 SRP 가설 연관 정책을 validation 선택 후 독립 test에 고정 적용한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig, usb_array_global_m
from measurement import fixed_measurement_covariance, initialize_position
from multipeak_measurement import extract_measurement
from hypothesis_adaptive import HypothesisAdaptiveRUKF
from ukf import SignalObservationUKF, acceleration_process_covariance

DISTANCES = (100, 200, 400, 600); STEPS = 10


def trajectory(distance, split):
    rng = np.random.default_rng((271000 if split == "validation" else 272000) + distance)
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    start = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
    tangent = np.array([-np.sin(az), np.cos(az), 0.0]); radial = np.array([np.cos(az), np.sin(az), 0.0])
    t = np.arange(STEPS, dtype=float)
    truth = start + t[:, None] * (0.72 * tangent + rng.uniform(-0.2, 0.2) * radial)
    meta = {"snr_db": float(rng.choice([10.0, 20.0, 30.0])),
            "surface_reflection": float(-rng.uniform(0.72, 0.97)),
            "bottom_reflection": float(rng.uniform(0.32, 0.78)),
            "radial_velocity_m_s": float(rng.uniform(-1.3, 1.3))}
    return truth, meta


def collect(split):
    base = ChannelConfig(); data = {}; center = usb_array_global_m().mean(axis=0)
    seed_root = 273000 if split == "validation" else 274000
    for distance in DISTANCES:
        truth, meta = trajectory(distance, split); observations = []; qualities = []; coverage = []
        for k, position in enumerate(truth):
            cfg = replace(base, seed=seed_root + distance * 10 + k, **meta)
            _, received, _ = synthesize_received(position, cfg); z, q = extract_measurement(received, cfg)
            observations.append(z); qualities.append(q)
            actual = position - center; actual /= np.linalg.norm(actual)
            errors = [np.degrees(np.arccos(np.clip(actual @ c["direction"], -1., 1.))) for c in q["candidates"]]
            coverage.append({"top1_error_deg": errors[0], "best5_error_deg": min(errors)})
        data[distance] = (truth, np.asarray(observations), qualities, coverage)
    return base, data


def make_filter(initial, cfg):
    return SignalObservationUKF(np.r_[initial, np.zeros(3)], np.diag([8.0**2] * 3 + [1.5**2] * 3),
        acceleration_process_covariance(1.0, 0.20), fixed_measurement_covariance(), cfg)


def evaluate(dataset, cfg, count=1, ratio=1.0, weight=0.0):
    truth, observations, qualities, _ = dataset; initial = initialize_position(observations[0], cfg)
    wrapper = HypothesisAdaptiveRUKF(make_filter(initial, cfg), count, ratio, weight)
    estimate = np.zeros_like(truth); estimate[0] = initial
    for k in range(1, len(truth)): estimate[k] = wrapper.step(observations[k], qualities[k])[:3]
    error = np.linalg.norm(estimate - truth, axis=1)
    return {"rmse_after_3_m": float(np.sqrt(np.mean(error[3:]**2))), "max_error_m": float(np.max(error)),
            "final_error_m": float(error[-1]), "diverged_over_50m": bool(np.any(error > 50.0)),
            "switch_rate": float(np.mean([h["switched"] for h in wrapper.history]))}


def validate():
    cfg, data = collect("validation")
    policies = [("baseline", 1, 1.0, 0.0)]
    for count in (3, 5):
        for ratio in (0.50, 0.75):
            for weight in (0.0, 10.0): policies.append((f"k{count}_r{ratio:.2f}_w{int(weight)}", count, ratio, weight))
    scores = {}
    for name, count, ratio, weight in policies:
        records = {str(d): evaluate(data[d], cfg, count, ratio, weight) for d in DISTANCES}
        values = [r["rmse_after_3_m"] for r in records.values()]
        score = float(np.mean(values) + 0.25 * np.max(values) + 100 * sum(r["diverged_over_50m"] for r in records.values()))
        scores[name] = {"candidate_count": count, "minimum_score_ratio": ratio, "score_weight_deg": weight,
                        "robust_score": score, "mean_rmse_m": float(np.mean(values)),
                        "worst_rmse_m": float(np.max(values)), "records": records}
    selected = min(scores, key=lambda key: scores[key]["robust_score"])
    coverage = {str(d): {"top1_within_5deg_rate": float(np.mean([x["top1_error_deg"] <= 5 for x in data[d][3]])),
                         "best5_within_5deg_rate": float(np.mean([x["best5_error_deg"] <= 5 for x in data[d][3]])),
                         "mean_top1_error_deg": float(np.mean([x["top1_error_deg"] for x in data[d][3]])),
                         "mean_best5_error_deg": float(np.mean([x["best5_error_deg"] for x in data[d][3]]))} for d in DISTANCES}
    return selected, scores, coverage


def run():
    selected, scores, validation_coverage = validate(); cfg, test_data = collect("test"); chosen = scores[selected]
    args = (chosen["candidate_count"], chosen["minimum_score_ratio"], chosen["score_weight_deg"])
    test = {str(d): {"baseline": evaluate(test_data[d], cfg), "selected": evaluate(test_data[d], cfg, *args)} for d in DISTANCES}
    test_coverage = {str(d): {"top1_within_5deg_rate": float(np.mean([x["top1_error_deg"] <= 5 for x in test_data[d][3]])),
                              "best5_within_5deg_rate": float(np.mean([x["best5_error_deg"] <= 5 for x in test_data[d][3]]))} for d in DISTANCES}
    payload = {"selection": {"selected": selected, "validation": scores},
               "candidate_coverage": {"validation": validation_coverage, "test": test_coverage}, "test": test}
    output = Path(__file__).resolve().parent / "results"; output.mkdir(exist_ok=True)
    (output / "multihypothesis_policy.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2)); return payload


if __name__ == "__main__": run()
