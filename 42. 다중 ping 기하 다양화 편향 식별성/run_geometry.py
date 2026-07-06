"""42번 러너: 기하 다양화가 계통 고도각 편향을 관측가능하게 만드는지 두 진단으로 요약.

Part A: 한 궤적 안에서 편향이 얼마나 상수인가(=다중 ping 평균으로 소거 가능한가).
Part B: 큰 방위 회전에 따라 편향이 탈상관되는가(=다중 시점 융합이 편향을 줄일 수 있는가).
Ground Truth는 편향 label 산출에만 쓴다.
"""

from pathlib import Path
import json
import numpy as np

from bias_geometry import (AZIMUTH_OFFSETS_DEG, DISTANCES, collect_within,
                           collect_rotation)


def summarize_within(records):
    out = {}
    for d in DISTANCES:
        sub = [r for r in records if r["distance"] == d]
        out[str(d)] = {
            "median_mean_abs_bias_deg": float(np.median([r["mean_abs_bias_deg"] for r in sub])),
            "median_within_track_std_deg": float(np.median([r["within_track_std_deg"] for r in sub])),
            "median_averaging_retention": float(np.median([r["averaging_retention"] for r in sub])),
            "median_bearing_change_deg": float(np.median([r["bearing_change_deg"] for r in sub])),
            "n_tracks": len(sub),
        }
    return out


def summarize_rotation(rotation):
    """Δ=0 편향과 Δ 편향의 점간 상관, Δ별 평균 |편향|을 낸다."""
    out = {}
    for d in DISTANCES:
        points = rotation[d]
        base = np.array([p[0.0] for p in points])
        per_offset = {}
        for offset in AZIMUTH_OFFSETS_DEG:
            vals = np.array([p[offset] for p in points])
            if offset == 0.0:
                corr = 1.0
            else:
                corr = float(np.corrcoef(base, vals)[0, 1]) if np.std(vals) > 1e-9 else float("nan")
            per_offset[str(offset)] = {
                "corr_with_0deg": corr,
                "mean_abs_bias_deg": float(np.mean(np.abs(vals))),
            }
        out[str(d)] = {"n_points": len(points), "by_offset": per_offset}
    return out


def run():
    within = collect_within()
    rotation = collect_rotation()
    payload = {
        "config": {"distances_m": list(DISTANCES),
                   "azimuth_offsets_deg": list(AZIMUTH_OFFSETS_DEG),
                   "note": "A=궤적내 편향 지속성(평균소거), B=방위회전 탈상관(다중시점 융합 가능성)"},
        "part_A_within_track": summarize_within(within),
        "part_B_azimuth_rotation": summarize_rotation(rotation),
    }
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / "geometry_diversity.json").write_text(
        json.dumps({**payload, "raw_within": within}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
