"""사전 위치오차에 따른 blind multipath association 일반화 검증."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from blind_association import associate_array, PATH_NAMES
from channel import synthesize_received
from config import ChannelConfig
from path_identifiability import observed_peaks


DISTANCES = (100, 200, 400, 600); PRIOR_STDS = (0.0, 5.0, 15.0, 30.0)


def scene(distance, index, split):
    root = 291000 if split == "validation" else 292000
    rng = np.random.default_rng(root + distance * 100 + index)
    depth = rng.uniform(12.0, 82.0); azimuth = rng.uniform(-np.pi, np.pi)
    position = np.array([distance * np.cos(azimuth), distance * np.sin(azimuth), -depth])
    cfg = replace(ChannelConfig(), seed=root + 50000 + distance * 100 + index,
                  snr_db=float(rng.choice([5.0, 10.0, 20.0, 30.0])),
                  surface_reflection=float(-rng.uniform(0.65, 0.98)),
                  bottom_reflection=float(rng.uniform(0.25, 0.80)))
    return position, cfg, rng


def extract_records(position, cfg):
    _, received, all_paths = synthesize_received(position, cfg); records = []
    for signal, paths in zip(received, all_paths):
        times, strengths = observed_peaks(signal, cfg, maximum=8)
        records.append({"peak_times_s": times, "peak_strengths": strengths, "true_paths": paths})
    return records


def perturb(position, std, rng, cfg):
    estimate = position + rng.normal(0.0, std, 3)
    estimate[2] = np.clip(estimate[2], -cfg.water_depth_m + 1.0, -1.0)
    return estimate


def evaluate(split, scenes_per_distance=20, tolerance_s=2/12000):
    buckets = {(d, s): {"correct": 0, "total": 0, "all_three": 0, "sensors": 0,
                        "residual_us": []} for d in DISTANCES for s in PRIOR_STDS}
    for distance in DISTANCES:
        for index in range(scenes_per_distance):
            position, cfg, rng = scene(distance, index, split); records = extract_records(position, cfg)
            for std in PRIOR_STDS:
                estimate = perturb(position, std, rng, cfg); associations = associate_array(records, estimate, cfg)
                bucket = buckets[(distance, std)]
                for record, association in zip(records, associations):
                    selected = association["times_s"]
                    truths = np.array([p.delay_s for p in record["true_paths"]])
                    matched = np.abs(selected - truths) <= tolerance_s
                    bucket["correct"] += int(np.sum(matched)); bucket["total"] += 3
                    bucket["all_three"] += int(np.all(matched)); bucket["sensors"] += 1
                    bucket["residual_us"].extend(np.abs(association["relative_residual_s"][1:]) * 1e6)
    return {str(d): {str(int(s)): {"path_accuracy": b["correct"] / b["total"],
                                   "complete_triplet_rate": b["all_three"] / b["sensors"],
                                   "median_model_residual_us": float(np.median(b["residual_us"])),
                                   "p90_model_residual_us": float(np.percentile(b["residual_us"], 90))}
                            for s in PRIOR_STDS for b in [buckets[(d, s)]]} for d in DISTANCES}


def run():
    validation = evaluate("validation"); test = evaluate("test")
    payload = {"prior_position_std_m": PRIOR_STDS, "scenes_per_distance": 20,
               "validation": validation, "test": test}
    output = Path(__file__).resolve().parent / "results"; output.mkdir(exist_ok=True)
    (output / "blind_association.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2)); return payload


if __name__ == "__main__": run()
