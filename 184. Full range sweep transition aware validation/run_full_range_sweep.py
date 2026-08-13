"""Full horizontal-range sweep from 0 m to 1000 m."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
F183 = next(ROOT.glob("183. *"))
sys.path.insert(0, str(F183))


import run_extended_transition_aware_validation as base  # noqa: E402


DISTANCES = tuple(float(v) for v in range(0, 1001, 100))
GEOMS = 6
STEPS = base.STEPS
SETTLE_START = base.SETTLE_START
FIXED_CARRIER_HZ = base.FIXED_CARRIER_HZ
HOP_CARRIERS_HZ = base.HOP_CARRIERS_HZ
GEOM_ROOT = 1_840_000
PING_ROOT = 1_843_000


def geometry(distance: float, index: int) -> tuple[np.ndarray, dict[str, float]]:
    rng = np.random.default_rng(GEOM_ROOT + int(distance) * 50 + index)
    azimuth = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    position = np.array([distance * np.cos(azimuth), distance * np.sin(azimuth), -depth])
    environment = {
        "snr_db": float(rng.choice([10.0, 20.0, 30.0])),
        "surface_reflection": float(-rng.uniform(0.72, 0.97)),
        "bottom_reflection": float(rng.uniform(0.32, 0.78)),
        "radial_velocity_m_s": 0.0,
    }
    return position, environment


def collect(position: np.ndarray, environment: dict[str, float], distance: float, index: int, carriers: np.ndarray):
    observations: list[np.ndarray] = []
    qualities: list[dict] = []
    max_jump = 0.0
    previous = None
    for ping_index, carrier_hz in enumerate(carriers):
        cfg = replace(
            base.ChannelConfig(),
            seed=PING_ROOT + int(distance) * 1000 + index * 40 + ping_index,
            carrier_hz=float(carrier_hz),
            **environment,
        )
        _, received, _ = base.synthesize_received(position, cfg)
        observation, quality = base.extract_measurement(received, cfg)
        if previous is not None:
            max_jump = max(max_jump, abs(float(observation[0]) - previous))
        previous = float(observation[0])
        observations.append(observation)
        qualities.append(quality)
    return np.asarray(observations), qualities, float(max_jump)


def run_case(distance: float, index: int) -> dict[str, Any]:
    position, environment = geometry(distance, index)
    fixed_carriers = np.full(STEPS, FIXED_CARRIER_HZ)
    obs_fixed, q_fixed, fixed_max_jump = collect(position, environment, distance, index, fixed_carriers)
    obs_hop, q_hop, hop_max_jump = collect(position, environment, distance, index, HOP_CARRIERS_HZ)
    return {
        "distance_m": distance,
        "index": index,
        "environment": environment,
        "fixed_max_adjacent_range_jump_m": fixed_max_jump,
        "hop_max_adjacent_range_jump_m": hop_max_jump,
        "fixed_baseline": base.run_filter(obs_fixed, q_fixed, position, fixed_carriers, "fixed_baseline"),
        "hop_baseline": base.run_filter(obs_hop, q_hop, position, HOP_CARRIERS_HZ, "hop_baseline"),
        "hop_transition_softR": base.run_filter(obs_hop, q_hop, position, HOP_CARRIERS_HZ, "hop_transition_softR"),
    }


def bootstrap_ci(values: np.ndarray, seed: int = 184, n: int = 3000) -> list[float]:
    rng = np.random.default_rng(seed)
    means = [np.mean(rng.choice(values, len(values), replace=True)) for _ in range(n)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def compare(subset: list[dict[str, Any]], ref_policy: str, target_policy: str) -> dict[str, Any]:
    gains = np.array([r[ref_policy]["settled_rmse_m"] - r[target_policy]["settled_rmse_m"] for r in subset])
    try:
        p = float(wilcoxon(gains, alternative="greater").pvalue) if np.any(gains != 0) else 1.0
    except ValueError:
        p = 1.0
    return {
        "mean_gain_m": float(np.mean(gains)),
        "median_gain_m": float(np.median(gains)),
        "gain_ci95": bootstrap_ci(gains),
        "wilcoxon_gain_gt0_p": p,
        "improved_fraction": float(np.mean(gains > 0.0)),
        "tail_worsened_fraction": float(np.mean(gains < -1.0)),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    policies = ("fixed_baseline", "hop_baseline", "hop_transition_softR")
    for distance in list(DISTANCES) + ["overall"]:
        subset = rows if distance == "overall" else [r for r in rows if r["distance_m"] == distance]
        entry: dict[str, Any] = {"policies": {}, "comparisons": {}}
        for policy in policies:
            rmse = np.array([r[policy]["settled_rmse_m"] for r in subset])
            entry["policies"][policy] = {
                "mean_rmse_m": float(np.mean(rmse)),
                "median_rmse_m": float(np.median(rmse)),
                "mean_p90_error_m": float(np.mean([r[policy]["p90_settled_error_m"] for r in subset])),
                "divergence_rate": float(np.mean([r[policy]["diverged"] for r in subset])),
                "total_transition_risks": int(sum(r[policy].get("transition_risk_count", 0) for r in subset)),
                "n": len(subset),
            }
        entry["comparisons"]["hop_vs_fixed"] = compare(subset, "fixed_baseline", "hop_baseline")
        entry["comparisons"]["softR_vs_hop"] = compare(subset, "hop_baseline", "hop_transition_softR")
        entry["comparisons"]["softR_vs_fixed"] = compare(subset, "fixed_baseline", "hop_transition_softR")
        summary[str(distance)] = entry
    return summary


def make_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Full range sweep result summary",
        "",
        "거리당 n=6 diagnostic sweep이다. 강한 성능 claim에는 추가 독립검증이 필요하다.",
        "",
        "| distance | fixed mean | hop mean | softR mean | hop gain vs fixed | softR gain vs fixed | hop div | softR div | softR triggers |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for d in DISTANCES:
        s = payload["summary"][str(d)]
        lines.append(
            "| {d:.0f} | {fx:.3f} | {hp:.3f} | {sr:.3f} | {hg:.3f} | {sg:.3f} | {hd:.3f} | {sd:.3f} | {trig} |".format(
                d=d,
                fx=s["policies"]["fixed_baseline"]["mean_rmse_m"],
                hp=s["policies"]["hop_baseline"]["mean_rmse_m"],
                sr=s["policies"]["hop_transition_softR"]["mean_rmse_m"],
                hg=s["comparisons"]["hop_vs_fixed"]["mean_gain_m"],
                sg=s["comparisons"]["softR_vs_fixed"]["mean_gain_m"],
                hd=s["policies"]["hop_baseline"]["divergence_rate"],
                sd=s["policies"]["hop_transition_softR"]["divergence_rate"],
                trig=s["policies"]["hop_transition_softR"]["total_transition_risks"],
            )
        )
    lines.extend([
        "",
        "## 해석 경계",
        "",
        "- 0 m는 horizontal distance 0 m 특수 near-vertical case다.",
        "- 거리당 n=6이므로 통계적 trend map으로만 사용한다.",
        "- 평균 이득과 divergence/tail을 반드시 함께 본다.",
    ])
    return "\n".join(lines) + "\n"


def run(max_workers: int = 6) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    cases = [(d, i) for d in DISTANCES for i in range(GEOMS)]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_case, *case): case for case in cases}
        for future in as_completed(futures):
            d, i = futures[future]
            rows.append(future.result())
            print(f"completed {int(d)} m #{i}", flush=True)
    rows.sort(key=lambda r: (r["distance_m"], r["index"]))
    summary = summarize(rows)
    payload = {
        "config": {
            "stage": "range_sweep_diagnostic",
            "distances_m": list(DISTANCES),
            "geometries_per_distance": GEOMS,
            "steps": STEPS,
            "settle_start": SETTLE_START,
            "geometry_seed_root": GEOM_ROOT,
            "ping_seed_root": PING_ROOT,
            "range_jump_threshold_m": base.RANGE_JUMP_THRESHOLD_M,
            "max_toa_scale": base.MAX_TOA_SCALE,
            "truth_usage": "truth is used for signal synthesis and final error computation only.",
            "manuscript_claim_allowed": False,
        },
        "summary": summary,
        "trials": rows,
    }
    out = HERE / "full_range_sweep.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (HERE / "result_summary.md").write_text(make_markdown(payload), encoding="utf-8")
    print(json.dumps({"overall": summary["overall"]}, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    run()
