"""Build a harmonized provenance manifest for the core adopted result files.

This script does not rerun experiments and does not change any adopted result.
It reads existing JSON outputs plus runner constants and writes a lightweight
metadata manifest in this folder.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def folder(prefix: str) -> Path:
    matches = sorted(ROOT.glob(prefix + "*"))
    if not matches:
        raise FileNotFoundError(prefix)
    return matches[0]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def const_from_py(path: Path, name: str) -> Any:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        text = ast.get_source_segment(path.read_text(encoding="utf-8"), node.value)
                        return text
    return None


def parse_seed_const(path: Path, name: str) -> Any:
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"^{name}\s*=\s*([0-9_]+)", text, flags=re.M)
    return int(m.group(1).replace("_", "")) if m else None


def base_signal_metadata(config_path: Path) -> dict[str, Any]:
    text = config_path.read_text(encoding="utf-8")
    def get_float(name: str) -> float | None:
        m = re.search(rf"{name}:\s*float\s*=\s*([0-9.]+)", text)
        return float(m.group(1)) if m else None
    return {
        "array": {
            "sensor_count": 8,
            "ring_radius_m": 0.033,
            "vertical_spacing_m": 0.079,
        },
        "signal": {
            "sample_rate_hz": get_float("sample_rate_hz"),
            "carrier_hz_default": get_float("carrier_hz"),
            "chirp_bandwidth_hz": get_float("chirp_bandwidth_hz"),
            "pulse_duration_s": get_float("pulse_duration_s"),
            "direct_path_gate_s": 0.005,
        },
        "channel": {
            "sound_speed_m_s": get_float("sound_speed_m_s"),
            "water_depth_m": get_float("water_depth_m"),
            "receiver_depth_m": get_float("receiver_depth_m"),
            "paths": ["direct", "surface", "bottom"],
            "ambient_noise": "colored frequency-shaped noise",
        },
        "usbl_protocol": {
            "source_type": "one_way_synchronized_beacon",
            "toa_mode": "one_way_absolute_toa",
            "common_clock_bias_model": "not_included_in_canonical_validation",
            "per_sensor_hardware_delay_model": "not_included_in_canonical_validation",
        },
    }


def entry_61() -> dict[str, Any]:
    f = folder("61.")
    result = read_json(f / "results" / "static_hop_validation.json")
    runner = f / "run_static_hop.py"
    cfg = result["config"]
    return {
        "folder": f.name,
        "stage": "independent_validation",
        "result_file": str((f / "results" / "static_hop_validation.json").relative_to(ROOT)),
        "protocol_frozen_before_execution": True,
        "automatic_manuscript_update_allowed": True,
        "seed_roots": {
            "geometry": parse_seed_const(runner, "GEOM_ROOT"),
            "ping": parse_seed_const(runner, "PING_ROOT"),
            "bootstrap": 600,
        },
        "distances_m": cfg.get("distances_m"),
        "steps": cfg.get("steps"),
        "settle_start": cfg.get("settle_start"),
        "fixed_carrier_khz": cfg.get("fixed_carrier_khz"),
        "hop_carriers_khz": cfg.get("hop_carriers_khz"),
        "truth_usage": "truth/static position is used for signal synthesis and settled RMSE only; not for measurement extraction or adaptive-R decisions.",
        "claim_allowed": "static long-range carrier-agile RMSE improvement; strongest at 600 m",
        "claim_forbidden": "moving-target RMSE improvement or practical uncalibrated USBL performance",
        "headline_summary": result["summary"]["600"],
        **base_signal_metadata(f / "config.py"),
    }


def entry_63() -> dict[str, Any]:
    f = folder("63.")
    result = read_json(f / "results" / "moving_validation.json")
    cfg = result["config"]
    return {
        "folder": f.name,
        "stage": "mechanism_validation_boundary",
        "result_file": str((f / "results" / "moving_validation.json").relative_to(ROOT)),
        "protocol_frozen_before_execution": True,
        "automatic_manuscript_update_allowed": False,
        "seed_roots": cfg.get("seed_roots"),
        "distance_m": cfg.get("distance_m"),
        "steps": cfg.get("steps"),
        "settle_start": cfg.get("settle_start"),
        "motion_conditions": cfg.get("condition_details"),
        "fixed_carrier_khz": cfg.get("fixed_carrier_khz"),
        "hop_carriers_khz": cfg.get("hop_carriers_khz"),
        "truth_usage": cfg.get("truth_usage"),
        "claim_allowed": "moving-target residual lag-1 reduction as mechanism evidence",
        "claim_forbidden": "moving-target pooled RMSE improvement",
        "headline_summary": result["summary"],
        **base_signal_metadata(f / "config.py"),
    }


def entry_82() -> dict[str, Any]:
    f = folder("82.")
    result = read_json(f / "results" / "quasi_static_boundary.json")
    cfg = result["config"]
    return {
        "folder": f.name,
        "stage": "validation_boundary",
        "result_file": str((f / "results" / "quasi_static_boundary.json").relative_to(ROOT)),
        "protocol_frozen_before_execution": True,
        "automatic_manuscript_update_allowed": True,
        "seed_roots": cfg.get("seed_roots"),
        "distance_m": cfg.get("distance_m"),
        "steps": cfg.get("steps"),
        "settle_start": cfg.get("settle_start"),
        "speeds_m_s": cfg.get("speeds_m_s"),
        "motion_modes": cfg.get("motion_modes"),
        "fixed_carrier_khz": cfg.get("fixed_carrier_khz"),
        "hop_carriers_khz": cfg.get("hop_carriers_khz"),
        "truth_usage": "truth trajectory is used for signal synthesis, RMSE, and offline elevation residual lag-1 only.",
        "claim_allowed": "continuous quasi-static boundary only up to 0.005 m/s",
        "claim_forbidden": "monotonic validation up to 0.100 m/s",
        "headline_summary": result["summary"]["overall"],
        **base_signal_metadata(f / "config.py"),
    }


def entry_160() -> dict[str, Any]:
    f = folder("160.")
    result = read_json(f / "results" / "four_carrier_independent_validation.json")
    cfg = result["config"]
    return {
        "folder": f.name,
        "stage": cfg.get("stage"),
        "result_file": str((f / "results" / "four_carrier_independent_validation.json").relative_to(ROOT)),
        "protocol_frozen_before_execution": cfg.get("protocol_frozen_before_execution"),
        "automatic_manuscript_update_allowed": cfg.get("automatic_manuscript_update_allowed"),
        "seed_roots": {
            "geometry": cfg.get("geometry_seed_root"),
            "ping": cfg.get("ping_seed_root"),
        },
        "distance_m": cfg.get("distance_m"),
        "steps": cfg.get("steps"),
        "settle_start": cfg.get("settle_start"),
        "common_random_ping_seeds": cfg.get("common_random_ping_seeds"),
        "schedule_carriers_khz": cfg.get("schedule_carriers_khz"),
        "truth_usage": "truth/static position is used for signal synthesis and settled error metrics only.",
        "claim_allowed": "four-carrier sparse schedule failed independent validation; linear20 remains supported",
        "claim_forbidden": "four-carrier performance claim",
        "headline_summary": result["summary"],
        **base_signal_metadata(f / "config.py"),
    }


def entry_162() -> dict[str, Any]:
    f = folder("162.")
    result = read_json(f / "results" / "transition_toa_guard_pilot.json")
    cfg = result["config"]
    return {
        "folder": f.name,
        "stage": cfg.get("stage"),
        "result_file": str((f / "results" / "transition_toa_guard_pilot.json").relative_to(ROOT)),
        "protocol_frozen_before_execution": False,
        "automatic_manuscript_update_allowed": cfg.get("manuscript_claim_allowed"),
        "development_geometries": cfg.get("development_geometries"),
        "source_diagnostic": cfg.get("source_diagnostic"),
        "range_jump_threshold_m": cfg.get("range_jump_threshold_m"),
        "truth_usage": "post-hoc development geometry is used for pilot evaluation; no manuscript performance claim allowed.",
        "claim_allowed": "future-work mechanism/pilot only",
        "claim_forbidden": "TOA guard performance claim before independent validation",
        "headline_summary": result["summary"],
        **base_signal_metadata(f / "config.py"),
    }


def main() -> None:
    manifest = {
        "created": "2026-08-11",
        "purpose": "Harmonize provenance metadata for core results without changing adopted metrics.",
        "entries": [entry_61(), entry_63(), entry_82(), entry_160(), entry_162()],
    }
    (HERE / "core_result_metadata_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    rows = [
        "| result | stage | seed roots | P90/tail | truth_usage | claim boundary |",
        "|---|---|---|---|---|---|",
    ]
    for e in manifest["entries"]:
        summary = e.get("headline_summary", {})
        has_p90 = "yes" if "fixed_p90_rmse_m" in json.dumps(summary) or "mean_p90_settled_error_m" in json.dumps(summary) else "limited/no"
        rows.append(
            f"| {e['folder']} | {e.get('stage')} | {e.get('seed_roots')} | {has_p90} | recorded | recorded |"
        )
    (HERE / "metadata_gap_table.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps({"entries": len(manifest["entries"]), "output": "core_result_metadata_manifest.json"}, ensure_ascii=False))


if __name__ == "__main__":
    main()

