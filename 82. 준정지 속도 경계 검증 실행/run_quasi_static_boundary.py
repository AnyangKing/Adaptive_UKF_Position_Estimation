"""82. Quasi-static speed boundary validation.

Purpose
-------
The paper's strongest positive claim is static 600 m localization:
frequency-agile pinging reduces a carrier-locked coherent multipath DOA
bias. Moving-target validation showed residual whitening, but not a
reproducible RMSE gain. This script measures the transition between those
two regimes.

The experiment is preregistered in folder 81. It reuses the 61/63 signal
pipeline without retuning:

* observations: TOA + TDOA + DOA
* estimator: conditional adaptive-R UKF
* baseline: fixed 32 kHz
* treatment: 30--34 kHz ping-to-ping frequency-agile schedule

Execution is resumable through results/quasi_static_partial.json.
"""

from __future__ import annotations

from dataclasses import replace
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from pathlib import Path
import csv
import json
import math

import numpy as np
from scipy.stats import spearmanr, wilcoxon

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


DISTANCE_M = 600.0
GEOMS_PER_CONDITION = 12
STEPS = 20
SETTLE_START = 10
ROUTING_THRESHOLD_DEG = 5.0

FIXED_CARRIER_HZ = 32000.0
HOP_CARRIERS_HZ = np.linspace(30000.0, 34000.0, STEPS)

SPEEDS_M_S = (0.0, 0.005, 0.010, 0.030, 0.050, 0.100)
MOTION_MODES = ("radial", "tangential")

GEOM_ROOT = 820000
PING_ROOT = 1820000
MAX_WORKERS = min(4, max(1, (os.cpu_count() or 2) - 1))


def conditions() -> list[dict[str, float | str]]:
    out: list[dict[str, float | str]] = [{"name": "static_0.000", "speed_m_s": 0.0, "mode": "static"}]
    for speed in SPEEDS_M_S:
        if speed == 0.0:
            continue
        for mode in MOTION_MODES:
            out.append({"name": f"{mode}_{speed:.3f}", "speed_m_s": speed, "mode": mode})
    return out


CONDITIONS = conditions()


def geometry(cond_idx: int, index: int):
    rng = np.random.default_rng(GEOM_ROOT + cond_idx * 1000 + index)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    pos = np.array([DISTANCE_M * np.cos(az), DISTANCE_M * np.sin(az), -depth])
    env = dict(
        snr_db=float(rng.choice([10.0, 20.0, 30.0])),
        surface_reflection=float(-rng.uniform(0.72, 0.97)),
        bottom_reflection=float(rng.uniform(0.32, 0.78)),
        radial_velocity_m_s=0.0,
    )
    sign = 1.0 if rng.uniform() < 0.5 else -1.0
    return pos, env, az, sign


def truth_trajectory(pos: np.ndarray, az: float, sign: float, speed: float, mode: str) -> np.ndarray:
    if mode == "static" or speed == 0.0:
        velocity = np.zeros(3)
    else:
        radial = np.array([np.cos(az), np.sin(az), 0.0])
        tangential = np.array([-np.sin(az), np.cos(az), 0.0])
        velocity = sign * speed * radial if mode == "radial" else sign * speed * tangential
    return pos + np.arange(STEPS)[:, None] * velocity


def collect(truth: np.ndarray, env: dict, cond_idx: int, index: int, carriers: np.ndarray):
    obs, quals, el_err = [], [], []
    for k, pos in enumerate(truth):
        cfg = replace(
            ChannelConfig(),
            seed=PING_ROOT + cond_idx * 4000 + index * 60 + k,
            carrier_hz=float(carriers[k]),
            **env,
        )
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        truth_z = ideal_measurement(pos, cfg)
        obs.append(z)
        quals.append(q)
        el_err.append(float(z[9] - truth_z[9]))
    return np.asarray(obs), quals, np.asarray(el_err)


def lag1_autocorr(x: np.ndarray) -> float:
    x = np.asarray(x, float)
    a = x[:-1] - x[:-1].mean()
    b = x[1:] - x[1:].mean()
    denom = math.sqrt(float(np.sum(a * a) * np.sum(b * b)))
    return float(np.sum(a * b) / denom) if denom > 1.0e-12 else 0.0


def run_filter(obs: np.ndarray, quals: list[dict[str, float]], truth: np.ndarray, cfg: ChannelConfig):
    init = initialize_position(obs[0], cfg)
    ukf = SignalObservationUKF(
        np.r_[init, np.zeros(3)],
        np.diag([8.0**2] * 3 + [1.5**2] * 3),
        acceleration_process_covariance(1.0, 0.20),
        fixed_measurement_covariance(),
        cfg,
    )
    wrapper = ConditionalAdaptiveRUKF(ukf, ROUTING_THRESHOLD_DEG)
    est = np.zeros((STEPS, 3))
    est[0] = init
    for k in range(1, STEPS):
        try:
            wrapper.step(obs[k], quals[k])
            est[k] = ukf.x[:3]
        except Exception:
            est[k] = est[k - 1]
    err = np.linalg.norm(est - truth, axis=1)
    settled = err[SETTLE_START:]
    return {
        "settled_rmse_m": float(np.sqrt(np.mean(settled**2))),
        "settled_p90_m": float(np.percentile(settled, 90)),
        "diverged": bool(np.any(err > 50.0)),
    }


def bootstrap_ci(values: np.ndarray, seed: int, n: int = 3000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [float(np.mean(rng.choice(values, len(values), replace=True))) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def one_sided_p(values: np.ndarray) -> float:
    try:
        return float(wilcoxon(values, alternative="greater").pvalue) if np.any(values != 0) else 1.0
    except ValueError:
        return 1.0


def summarize_group(rows: list[dict], seed_offset: int) -> dict:
    fixed = np.array([r["fixed_rmse_m"] for r in rows])
    hop = np.array([r["hop_rmse_m"] for r in rows])
    gains = np.array([r["gain_m"] for r in rows])
    lag_fixed = np.array([r["lag1_fixed"] for r in rows])
    lag_hop = np.array([r["lag1_hop"] for r in rows])
    lag_reduction = lag_fixed - lag_hop
    mean_gain = float(np.mean(gains))
    median_gain = float(np.median(gains))
    improved_fraction = float(np.mean(gains > 0))
    p_gain = one_sided_p(gains)
    p_lag = one_sided_p(lag_reduction)
    if mean_gain > 0.0 and median_gain > 0.0 and improved_fraction >= 0.60 and p_gain < 0.05:
        decision = "validated"
    elif mean_gain > 0.0 and median_gain > 0.0:
        decision = "positive_trend"
    else:
        decision = "not_supported"
    return {
        "fixed_mean_rmse_m": float(np.mean(fixed)),
        "hop_mean_rmse_m": float(np.mean(hop)),
        "fixed_median_rmse_m": float(np.median(fixed)),
        "hop_median_rmse_m": float(np.median(hop)),
        "fixed_p90_rmse_m": float(np.percentile(fixed, 90)),
        "hop_p90_rmse_m": float(np.percentile(hop, 90)),
        "mean_gain_m": mean_gain,
        "median_gain_m": median_gain,
        "gain_ci95_m": bootstrap_ci(gains, 8200 + seed_offset),
        "wilcoxon_gain_greater_p": p_gain,
        "improved_fraction": improved_fraction,
        "fixed_divergence_rate": float(np.mean([r["fixed_diverged"] for r in rows])),
        "hop_divergence_rate": float(np.mean([r["hop_diverged"] for r in rows])),
        "mean_lag1_fixed": float(np.mean(lag_fixed)),
        "mean_lag1_hop": float(np.mean(lag_hop)),
        "mean_lag1_reduction": float(np.mean(lag_reduction)),
        "wilcoxon_lag_reduction_greater_p": p_lag,
        "lag_reduced_fraction": float(np.mean(lag_reduction > 0)),
        "decision": decision,
        "n": len(rows),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = [
        "condition",
        "speed_m_s",
        "mode",
        "index",
        "fixed_rmse_m",
        "hop_rmse_m",
        "gain_m",
        "fixed_p90_m",
        "hop_p90_m",
        "lag1_fixed",
        "lag1_hop",
        "lag1_reduction",
        "fixed_diverged",
        "hop_diverged",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})


def write_speed_svg(path: Path, speed_summary: dict[str, dict]) -> None:
    speeds = sorted(float(k) for k in speed_summary)
    gains = [speed_summary[f"{s:.3f}"]["mean_gain_m"] for s in speeds]
    lag = [speed_summary[f"{s:.3f}"]["mean_lag1_reduction"] for s in speeds]
    width, height = 760, 420
    left, right, top, bottom = 80, 40, 40, 70
    plot_w, plot_h = width - left - right, height - top - bottom
    x_min, x_max = min(speeds), max(speeds)
    y_vals = gains + [0.0]
    y_min, y_max = min(y_vals), max(y_vals)
    pad = max(0.5, 0.12 * (y_max - y_min + 1.0e-9))
    y_min -= pad
    y_max += pad
    l_vals = lag + [0.0]
    l_min, l_max = min(l_vals), max(l_vals)
    l_pad = max(0.05, 0.12 * (l_max - l_min + 1.0e-9))
    l_min -= l_pad
    l_max += l_pad

    def x_of(speed):
        return left + (speed - x_min) / (x_max - x_min) * plot_w if x_max > x_min else left

    def y_gain(value):
        return top + (y_max - value) / (y_max - y_min) * plot_h

    def y_lag(value):
        return top + (l_max - value) / (l_max - l_min) * plot_h

    gain_points = " ".join(f"{x_of(s):.1f},{y_gain(g):.1f}" for s, g in zip(speeds, gains))
    lag_points = " ".join(f"{x_of(s):.1f},{y_lag(v):.1f}" for s, v in zip(speeds, lag))
    zero_y = y_gain(0.0)
    lag_zero_y = y_lag(0.0)
    labels = []
    for s in speeds:
        labels.append(
            f'<text x="{x_of(s):.1f}" y="{height - 38}" font-size="12" text-anchor="middle">{s:.3f}</text>'
        )
    circles = []
    for s, g, l in zip(speeds, gains, lag):
        circles.append(f'<circle cx="{x_of(s):.1f}" cy="{y_gain(g):.1f}" r="4" fill="#2563eb"/>')
        circles.append(f'<circle cx="{x_of(s):.1f}" cy="{y_lag(l):.1f}" r="4" fill="#dc2626"/>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  <text x="{width/2}" y="24" text-anchor="middle" font-size="18" font-family="Arial">Quasi-static speed boundary at 600 m</text>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#111827"/>
  <line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#111827"/>
  <line x1="{left}" y1="{zero_y:.1f}" x2="{width-right}" y2="{zero_y:.1f}" stroke="#94a3b8" stroke-dasharray="5 5"/>
  <line x1="{left}" y1="{lag_zero_y:.1f}" x2="{width-right}" y2="{lag_zero_y:.1f}" stroke="#fecaca" stroke-dasharray="5 5"/>
  <polyline points="{gain_points}" fill="none" stroke="#2563eb" stroke-width="3"/>
  <polyline points="{lag_points}" fill="none" stroke="#dc2626" stroke-width="3"/>
  {''.join(circles)}
  {''.join(labels)}
  <text x="{width/2}" y="{height-12}" text-anchor="middle" font-size="13" font-family="Arial">speed (m/s)</text>
  <text x="18" y="{height/2}" transform="rotate(-90, 18, {height/2})" text-anchor="middle" font-size="13" font-family="Arial">mean RMSE gain, fixed-hop (m)</text>
  <text x="{width-8}" y="{height/2}" transform="rotate(90, {width-8}, {height/2})" text-anchor="middle" font-size="13" fill="#dc2626" font-family="Arial">lag-1 reduction</text>
  <text x="{left+10}" y="{top+20}" font-size="13" fill="#2563eb" font-family="Arial">blue: RMSE gain</text>
  <text x="{left+10}" y="{top+40}" font-size="13" fill="#dc2626" font-family="Arial">red: DOA residual whitening</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def run_trial(task: tuple[int, dict, int]) -> dict:
    cond_idx, cond, index = task
    cfg = ChannelConfig()
    fixed_carriers = np.full(STEPS, FIXED_CARRIER_HZ)
    name = str(cond["name"])
    speed = float(cond["speed_m_s"])
    mode = str(cond["mode"])
    pos, env, az, sign = geometry(cond_idx, index)
    truth = truth_trajectory(pos, az, sign, speed, mode)

    obs_f, q_f, el_f = collect(truth, env, cond_idx, index, fixed_carriers)
    obs_h, q_h, el_h = collect(truth, env, cond_idx, index, HOP_CARRIERS_HZ)

    fixed = run_filter(obs_f, q_f, truth, cfg)
    hop = run_filter(obs_h, q_h, truth, cfg)
    lag1_fixed = lag1_autocorr(el_f)
    lag1_hop = lag1_autocorr(el_h)
    return {
        "condition": name,
        "speed_m_s": speed,
        "mode": mode,
        "index": index,
        "fixed_rmse_m": fixed["settled_rmse_m"],
        "hop_rmse_m": hop["settled_rmse_m"],
        "gain_m": fixed["settled_rmse_m"] - hop["settled_rmse_m"],
        "fixed_p90_m": fixed["settled_p90_m"],
        "hop_p90_m": hop["settled_p90_m"],
        "lag1_fixed": lag1_fixed,
        "lag1_hop": lag1_hop,
        "lag1_reduction": lag1_fixed - lag1_hop,
        "fixed_diverged": fixed["diverged"],
        "hop_diverged": hop["diverged"],
    }


def run():
    out_dir = Path(__file__).resolve().parent / "results"
    out_dir.mkdir(exist_ok=True)
    partial_path = out_dir / "quasi_static_partial.json"

    rows = []
    if partial_path.exists():
        rows = json.loads(partial_path.read_text(encoding="utf-8"))["runs"]
    done = {(r["condition"], int(r["index"])) for r in rows}

    tasks = []
    for ci, cond in enumerate(CONDITIONS):
        for index in range(GEOMS_PER_CONDITION):
            if (str(cond["name"]), index) not in done:
                tasks.append((ci, cond, index))

    if tasks:
        print(f"running {len(tasks)} remaining trials with {MAX_WORKERS} workers", flush=True)
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(run_trial, task) for task in tasks]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            rows.sort(key=lambda r: (str(r["condition"]), int(r["index"])))
            partial_path.write_text(json.dumps({"runs": rows}, indent=2, ensure_ascii=False), encoding="utf-8")
            print(
                f"completed {len(rows)}/{len(CONDITIONS) * GEOMS_PER_CONDITION}: "
                f"{row['condition']} #{row['index']}",
                flush=True,
            )

    by_condition = {
        str(cond["name"]): summarize_group([r for r in rows if r["condition"] == cond["name"]], i)
        for i, cond in enumerate(CONDITIONS)
    }
    by_speed = {}
    for speed in SPEEDS_M_S:
        sub = [r for r in rows if abs(r["speed_m_s"] - speed) < 1.0e-12]
        by_speed[f"{speed:.3f}"] = summarize_group(sub, int(round(speed * 10000)) + 100)

    gains = np.array([r["gain_m"] for r in rows])
    lag_reductions = np.array([r["lag1_reduction"] for r in rows])
    rho, rho_p = spearmanr(lag_reductions, gains)
    overall = summarize_group(rows, 999)
    overall["spearman_lag_reduction_vs_gain"] = {"rho": float(rho), "p": float(rho_p)}

    supported = [float(speed) for speed, summary in by_speed.items() if summary["decision"] == "validated"]
    largest_supported_speed = max(supported) if supported else None
    contiguous_supported: list[float] = []
    for speed in SPEEDS_M_S:
        if by_speed[f"{speed:.3f}"]["decision"] == "validated":
            contiguous_supported.append(speed)
        else:
            break
    largest_contiguous_speed = max(contiguous_supported) if contiguous_supported else None
    later_recoveries = [
        speed
        for speed in supported
        if largest_contiguous_speed is None or speed > largest_contiguous_speed
    ]
    if largest_contiguous_speed and largest_contiguous_speed > 0:
        manuscript_consequence = (
            f"continuous quasi-static boundary supported only up to {largest_contiguous_speed:.3f} m/s; "
            f"later positive speeds {later_recoveries} are non-monotonic geometry-dependent recoveries"
        )
    elif by_speed["0.000"]["decision"] == "validated":
        manuscript_consequence = (
            "static-only claim is validated; quasi-static extension is not continuously validated"
        )
    else:
        manuscript_consequence = "frequency-agile performance gain not validated even in this static rerun"

    payload = {
        "config": {
            "distance_m": DISTANCE_M,
            "geoms_per_condition": GEOMS_PER_CONDITION,
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "speeds_m_s": list(SPEEDS_M_S),
            "motion_modes": list(MOTION_MODES),
            "fixed_carrier_khz": FIXED_CARRIER_HZ / 1000.0,
            "hop_carriers_khz": [float(c / 1000.0) for c in HOP_CARRIERS_HZ],
            "seed_roots": {"geometry": GEOM_ROOT, "ping": PING_ROOT},
            "note": "Preregistered follow-up to folder 81; no schedule retuning after seeing results.",
        },
        "summary": {
            "overall": overall,
            "by_speed": by_speed,
            "by_condition": by_condition,
            "largest_validated_speed_m_s": largest_supported_speed,
            "largest_contiguous_validated_speed_m_s": largest_contiguous_speed,
            "nonmonotonic_later_validated_speeds_m_s": later_recoveries,
            "manuscript_consequence": manuscript_consequence,
        },
        "runs": rows,
    }
    (out_dir / "quasi_static_boundary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_csv(out_dir / "quasi_static_trials.csv", rows)
    write_speed_svg(out_dir / "quasi_static_speed_boundary.svg", by_speed)
    print(json.dumps(payload["summary"], indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
