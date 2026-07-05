"""물리 경로 지연과 관측 가능한 matched-filter peak의 대응을 평가한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.signal import correlate, correlation_lags, find_peaks, hilbert

from channel import make_probe, synthesize_received
from config import ChannelConfig


def observed_peaks(signal, cfg, maximum=8):
    probe = make_probe(cfg)
    values = np.abs(hilbert(correlate(signal, probe, mode="full", method="fft")))
    lags = correlation_lags(len(signal), len(probe), mode="full")
    valid = lags >= 0; values = values[valid]; lags = lags[valid]
    # LFM 압축 main lobe 중복 검출을 막고 약한 반사도 남긴다.
    minimum = max(1, int(0.00012 * cfg.sample_rate_hz))
    indices, _ = find_peaks(values, height=0.08 * np.max(values), distance=minimum)
    if not len(indices): indices = np.array([int(np.argmax(values))])
    order = indices[np.argsort(values[indices])[::-1][:maximum]]
    return lags[order] / cfg.sample_rate_hz, values[order] / np.max(values)


def match_paths(paths, peak_times, tolerance_s):
    result = {}
    for path in paths:
        errors = np.abs(peak_times - path.delay_s)
        best = int(np.argmin(errors))
        result[path.name] = {"found": bool(errors[best] <= tolerance_s),
                             "error_us": float(errors[best] * 1e6)}
    return result


def evaluate_scene(position, cfg, tolerance_s=None):
    if tolerance_s is None: tolerance_s = 2.0 / cfg.chirp_bandwidth_hz
    _, received, all_paths = synthesize_received(position, cfg)
    sensor_records = []
    for signal, paths in zip(received, all_paths):
        times, strengths = observed_peaks(signal, cfg)
        matched = match_paths(paths, times, tolerance_s)
        delays = {p.name: p.delay_s for p in paths}
        sensor_records.append({"matched": matched, "peak_times_s": times.tolist(),
                               "peak_strengths": strengths.tolist(),
                               "surface_separation_us": (delays["surface"] - delays["direct"]) * 1e6,
                               "bottom_separation_us": (delays["bottom"] - delays["direct"]) * 1e6})
    return sensor_records


def run():
    base = ChannelConfig(); distances = (100, 200, 400, 600)
    depths = (15.0, 45.0, 75.0); snrs = (10.0, 20.0, 30.0); repeats = 5
    totals = {(d, s, p): [0, 0, []] for d in distances for s in snrs for p in ("direct", "surface", "bottom")}
    separations = {"surface": [], "bottom": []}; scene_count = 0
    for distance in distances:
        for depth in depths:
            for snr in snrs:
                for repeat in range(repeats):
                    az = np.random.default_rng(280000 + distance * 100 + int(depth) * 10 + int(snr) + repeat).uniform(-np.pi, np.pi)
                    position = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
                    cfg = replace(base, snr_db=snr, seed=281000 + distance * 100 + int(depth) * 10 + int(snr) + repeat,
                                  surface_reflection=-0.75 - 0.05 * repeat, bottom_reflection=0.35 + 0.08 * repeat)
                    records = evaluate_scene(position, cfg); scene_count += 1
                    for record in records:
                        separations["surface"].append(record["surface_separation_us"])
                        separations["bottom"].append(record["bottom_separation_us"])
                        for path in ("direct", "surface", "bottom"):
                            bucket = totals[(distance, snr, path)]; bucket[0] += int(record["matched"][path]["found"])
                            bucket[1] += 1; bucket[2].append(record["matched"][path]["error_us"])
    summary = {}
    for distance in distances:
        summary[str(distance)] = {}
        for snr in snrs:
            summary[str(distance)][str(int(snr))] = {path: {
                "recall": totals[(distance, snr, path)][0] / totals[(distance, snr, path)][1],
                "median_error_us": float(np.median(totals[(distance, snr, path)][2])),
                "p90_error_us": float(np.percentile(totals[(distance, snr, path)][2], 90)),
            } for path in ("direct", "surface", "bottom")}
    payload = {"scene_count": scene_count, "sensor_observations": scene_count * 8,
               "tolerance_us": 2e6 / base.chirp_bandwidth_hz,
               "separation_us": {key: {"minimum": float(np.min(value)), "median": float(np.median(value))}
                                  for key, value in separations.items()}, "summary": summary}
    output = Path(__file__).resolve().parent / "results"; output.mkdir(exist_ok=True)
    (output / "path_identifiability.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2)); return payload


if __name__ == "__main__": run()
