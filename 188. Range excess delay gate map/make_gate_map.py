"""Create a range--excess-delay--gate mechanism table."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent

SOUND_SPEED_M_S = 1500.0
WATER_DEPTH_M = 100.0
RECEIVER_DEPTH_M = 30.0
SOURCE_DEPTH_M = 40.0
DOA_GATE_MS = 5.0
DISTANCES_M = list(range(0, 1001, 100))


def path_length(horizontal_range_m: float, vertical_separation_m: float) -> float:
    return float(np.hypot(horizontal_range_m, vertical_separation_m))


def delay_ms(path_length_m: float) -> float:
    return 1000.0 * path_length_m / SOUND_SPEED_M_S


def load_gain_map() -> dict[int, float | None]:
    path = ROOT / "184. Full range sweep transition aware validation" / "full_range_sweep.json"
    if not path.exists():
        return {d: None for d in DISTANCES_M}
    payload = json.loads(path.read_text(encoding="utf-8"))
    gains: dict[int, float | None] = {}
    for distance in DISTANCES_M:
        row = payload["summary"].get(str(float(distance))) or payload["summary"].get(str(distance))
        gains[distance] = None if row is None else float(row["comparisons"]["hop_vs_fixed"]["mean_gain_m"])
    return gains


def make_rows() -> list[dict[str, Any]]:
    surface_vertical = SOURCE_DEPTH_M + RECEIVER_DEPTH_M
    bottom_image_depth = 2.0 * WATER_DEPTH_M - SOURCE_DEPTH_M
    bottom_vertical = abs(bottom_image_depth - RECEIVER_DEPTH_M)
    direct_vertical = abs(SOURCE_DEPTH_M - RECEIVER_DEPTH_M)
    gains = load_gain_map()
    rows: list[dict[str, Any]] = []
    for distance in DISTANCES_M:
        direct = path_length(distance, direct_vertical)
        surface = path_length(distance, surface_vertical)
        bottom = path_length(distance, bottom_vertical)
        surface_excess_ms = delay_ms(surface - direct)
        bottom_excess_ms = delay_ms(bottom - direct)
        rows.append({
            "horizontal_range_m": distance,
            "direct_travel_time_ms": delay_ms(direct),
            "surface_excess_delay_ms": surface_excess_ms,
            "surface_inside_5ms_gate": bool(surface_excess_ms <= DOA_GATE_MS),
            "bottom_excess_delay_ms": bottom_excess_ms,
            "bottom_inside_5ms_gate": bool(bottom_excess_ms <= DOA_GATE_MS),
            "folder184_hop_gain_m": gains.get(distance),
        })
    return rows


def markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Range--excess-delay--gate result summary",
        "",
        "| range m | direct ms | surface excess ms | surface in 5 ms gate | bottom excess ms | bottom in 5 ms gate | 184 hop gain m |",
        "|---:|---:|---:|:---:|---:|:---:|---:|",
    ]
    for row in rows:
        gain = row["folder184_hop_gain_m"]
        gain_text = "" if gain is None else f"{gain:.3f}"
        lines.append(
            f"| {row['horizontal_range_m']} | {row['direct_travel_time_ms']:.2f} | "
            f"{row['surface_excess_delay_ms']:.2f} | {'yes' if row['surface_inside_5ms_gate'] else 'no'} | "
            f"{row['bottom_excess_delay_ms']:.2f} | {'yes' if row['bottom_inside_5ms_gate'] else 'no'} | "
            f"{gain_text} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "In this representative geometry, the surface reflection is outside the 5 ms DOA gate at 0--300 m and enters the gate by about 400 m. This is consistent with the diagnostic pattern from folder 184: carrier agility is weak or unstable at short/medium ranges and becomes strongly beneficial beyond about 600 m.",
        "",
        "The bottom reflection remains outside the 5 ms gate throughout 0--1000 m in this representative geometry. Thus the dominant in-gate coherent reflection expected from this simple image-source map is the surface path, not the bottom path.",
        "",
        "Because source depth is randomized in the simulations, this table should be used as a representative mechanism map rather than a replacement for per-trial metadata.",
    ])
    return "\n".join(lines) + "\n"


def main() -> dict[str, Any]:
    rows = make_rows()
    payload = {
        "config": {
            "sound_speed_m_s": SOUND_SPEED_M_S,
            "water_depth_m": WATER_DEPTH_M,
            "receiver_depth_m": RECEIVER_DEPTH_M,
            "representative_source_depth_m": SOURCE_DEPTH_M,
            "doa_gate_ms": DOA_GATE_MS,
            "distances_m": DISTANCES_M,
            "source_of_gain_values": "184. Full range sweep transition aware validation/full_range_sweep.json",
            "claim_boundary": "representative mechanism map only; not per-trial simulation metadata",
        },
        "rows": rows,
    }
    (HERE / "range_excess_delay_gate_map.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (HERE / "result_summary.md").write_text(markdown(rows), encoding="utf-8")
    print(markdown(rows))
    return payload


if __name__ == "__main__":
    main()
