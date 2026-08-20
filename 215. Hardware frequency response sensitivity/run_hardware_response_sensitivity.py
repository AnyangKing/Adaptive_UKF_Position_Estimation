"""Carrier-dependent hardware-response sensitivity for moving validation.

This script reuses the frozen folder-191 estimator/protocol and adds only an
idealized carrier-dependent effective-SNR profile. It is a sensitivity check,
not a hardware validation.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
F191 = next(ROOT.glob("191. Moving full range transition aware independent validation"))
M191_PATH = F191 / "run_moving_full_range_independent_validation.py"

spec = importlib.util.spec_from_file_location("moving191", M191_PATH)
moving191 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(moving191)


DISTANCES = tuple(float(d) for d in range(0, 1001, 200))
GEOMS = 8
CONDITIONS = moving191.CONDITIONS
STEPS = moving191.STEPS
FIXED_CARRIER_HZ = moving191.FIXED_CARRIER_HZ
HOP_CARRIERS_HZ = moving191.HOP_CARRIERS_HZ
GEOM_ROOT = 2_150_000
PING_ROOT = 2_153_000


RESPONSE_PROFILES: dict[str, dict[str, float]] = {
    "flat_reference": {"edge_loss_db": 0.0},
    "edge_loss_3db": {"edge_loss_db": 3.0},
    "edge_loss_6db": {"edge_loss_db": 6.0},
}


def response_delta_snr_db(carrier_hz: float, profile: str) -> float:
    """Return idealized response-induced SNR delta in dB.

    The response is normalized to 0 dB at 32 kHz and penalizes carriers toward
    30 and 34 kHz. A 6 dB edge-loss profile means 30/34 kHz are 6 dB lower than
    32 kHz.
    """

    if profile not in RESPONSE_PROFILES:
        raise ValueError(f"unknown response profile: {profile}")
    edge_loss_db = RESPONSE_PROFILES[profile]["edge_loss_db"]
    normalized_offset = abs(float(carrier_hz) - 32_000.0) / 2_000.0
    normalized_offset = min(1.0, max(0.0, normalized_offset))
    return -edge_loss_db * normalized_offset


def collect_with_response(
    truth: np.ndarray,
    env: dict[str, float],
    distance: float,
    cond_idx: int,
    index: int,
    carriers: np.ndarray,
    profile: str,
):
    observations: list[np.ndarray] = []
    qualities: list[dict] = []
    for k, pos in enumerate(truth):
        carrier = float(carriers[k])
        env_with_response = dict(env)
        env_with_response["snr_db"] = float(env["snr_db"] + response_delta_snr_db(carrier, profile))
        cfg = replace(
            moving191.ChannelConfig(),
            seed=PING_ROOT + int(distance) * 5000 + cond_idx * 4000 + index * 60 + k,
            carrier_hz=carrier,
            **env_with_response,
        )
        _, received, _ = moving191.synthesize_received(pos, cfg)
        observation, quality = moving191.extract_measurement(received, cfg)
        observations.append(observation)
        qualities.append(quality)
    return np.asarray(observations), qualities


def geometry(distance: float, cond_idx: int, index: int):
    old_root = moving191.GEOM_ROOT
    try:
        moving191.GEOM_ROOT = GEOM_ROOT
        return moving191.geometry(distance, cond_idx, index)
    finally:
        moving191.GEOM_ROOT = old_root


def run_case(profile: str, distance: float, cond_idx: int, cond: tuple[str, float, str, float], index: int):
    name, speed, mode, vz = cond
    pos, env, az, sign = geometry(distance, cond_idx, index)
    truth = moving191.truth_trajectory(pos, az, sign, speed, mode, vz)
    fixed_carriers = np.full(STEPS, FIXED_CARRIER_HZ)
    obs_fixed, q_fixed = collect_with_response(truth, env, distance, cond_idx, index, fixed_carriers, profile)
    obs_hop, q_hop = collect_with_response(truth, env, distance, cond_idx, index, HOP_CARRIERS_HZ, profile)
    return [
        {
            "profile": profile,
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "fixed_baseline",
            **moving191.run_filter(obs_fixed, q_fixed, truth, fixed_carriers, "fixed_baseline"),
        },
        {
            "profile": profile,
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "hop_baseline",
            **moving191.run_filter(obs_hop, q_hop, truth, HOP_CARRIERS_HZ, "hop_baseline"),
        },
        {
            "profile": profile,
            "distance_m": distance,
            "condition": name,
            "index": index,
            "policy": "hop_transition_softR",
            **moving191.run_filter(obs_hop, q_hop, truth, HOP_CARRIERS_HZ, "hop_transition_softR"),
        },
    ]


def _compare(keys: list[tuple[str, float, str, int]], ref: dict, test: dict) -> dict[str, Any]:
    gains = np.array([ref[k]["settled_rmse_m"] - test[k]["settled_rmse_m"] for k in keys])
    try:
        p = float(moving191.wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
    except ValueError:
        p = 1.0
    return {
        "mean_gain_m": float(np.mean(gains)),
        "median_gain_m": float(np.median(gains)),
        "gain_ci95": moving191.bootstrap_ci(gains, seed=215),
        "wilcoxon_gain_gt0_p": p,
        "improved_fraction": float(np.mean(gains > 0)),
        "tail_worsened_fraction": float(np.mean(gains < -1.0)),
        "n": int(len(keys)),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"by_profile": {}, "comparisons": {}}
    policies = ("fixed_baseline", "hop_baseline", "hop_transition_softR")
    for profile in RESPONSE_PROFILES:
        subset = [r for r in rows if r["profile"] == profile]
        summary["by_profile"][profile] = {}
        for policy in policies:
            p_rows = [r for r in subset if r["policy"] == policy]
            summary["by_profile"][profile][policy] = {
                "mean_rmse_m": float(np.mean([r["settled_rmse_m"] for r in p_rows])),
                "median_rmse_m": float(np.median([r["settled_rmse_m"] for r in p_rows])),
                "mean_p90_error_m": float(np.mean([r["p90_settled_error_m"] for r in p_rows])),
                "divergence_rate": float(np.mean([r["diverged"] for r in p_rows])),
                "n": int(len(p_rows)),
            }
        fixed = {(r["profile"], r["distance_m"], r["condition"], r["index"]): r for r in subset if r["policy"] == "fixed_baseline"}
        hop = {(r["profile"], r["distance_m"], r["condition"], r["index"]): r for r in subset if r["policy"] == "hop_baseline"}
        soft = {(r["profile"], r["distance_m"], r["condition"], r["index"]): r for r in subset if r["policy"] == "hop_transition_softR"}
        keys = sorted(soft)
        summary["comparisons"][profile] = {
            "softR_vs_hop": _compare(keys, hop, soft),
            "softR_vs_fixed": _compare(keys, fixed, soft),
            "hop_vs_fixed": _compare(keys, fixed, hop),
        }
    return summary


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Hardware frequency-response sensitivity result summary",
        "",
        "## Overall policy metrics by response profile",
        "",
        "| profile | policy | mean RMSE | median RMSE | mean P90 | divergence | n |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for profile, by_policy in payload["summary"]["by_profile"].items():
        for policy, s in by_policy.items():
            lines.append(
                f"| {profile} | {policy} | {s['mean_rmse_m']:.3f} | {s['median_rmse_m']:.3f} | "
                f"{s['mean_p90_error_m']:.3f} | {s['divergence_rate']:.3f} | {s['n']} |"
            )
    lines.extend([
        "",
        "## Paired comparisons",
        "",
        "| profile | comparison | mean gain | p | improved frac | tail worsened | n |",
        "|---|---|---:|---:|---:|---:|---:|",
    ])
    for profile, comps in payload["summary"]["comparisons"].items():
        for name, comp in comps.items():
            lines.append(
                f"| {profile} | {name} | {comp['mean_gain_m']:.3f} | {comp['wilcoxon_gain_gt0_p']:.4g} | "
                f"{comp['improved_fraction']:.3f} | {comp['tail_worsened_fraction']:.3f} | {comp['n']} |"
            )
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "This is an idealized response-mismatch sensitivity simulation. It reduces, but does not eliminate, the hardware-response weakness. Real transducer/hydrophone response must still be measured in a later field or bench-validation study.",
    ])
    return "\n".join(lines) + "\n"


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [
        (profile, distance, ci, cond, i)
        for profile in RESPONSE_PROFILES
        for distance in DISTANCES
        for ci, cond in enumerate(CONDITIONS)
        for i in range(GEOMS)
    ]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for future in as_completed(futures):
            profile, distance, _, cond, i = futures[future]
            rows.extend(future.result())
            print(f"completed response {profile} {int(distance)} m {cond[0]} #{i}", flush=True)

    rows.sort(key=lambda r: (r["profile"], r["distance_m"], r["condition"], r["index"], r["policy"]))
    payload = {
        "config": {
            "stage": "hardware_frequency_response_sensitivity",
            "distances_m": list(DISTANCES),
            "geoms_per_distance_condition": GEOMS,
            "conditions": [
                {"name": c[0], "speed_m_s": c[1], "mode": c[2], "vertical_speed_m_s": c[3]}
                for c in CONDITIONS
            ],
            "response_profiles": RESPONSE_PROFILES,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "truth_usage": "truth is used for signal synthesis and final error computation only; response profile is a preset carrier-dependent SNR perturbation.",
            "claim_boundary": "idealized simulation sensitivity; not measured hardware response validation",
        },
        "summary": summarize(rows),
        "trials": rows,
    }
    (HERE / "hardware_response_sensitivity.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (HERE / "result_summary.md").write_text(markdown(payload), encoding="utf-8")
    print(markdown(payload))
    return payload


if __name__ == "__main__":
    run()
