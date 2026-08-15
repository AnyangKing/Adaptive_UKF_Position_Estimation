"""Aggregate checkpointed OOD validation case files."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
F202 = next(ROOT.glob("202. OOD motion transition aware validation"))
M202_PATH = F202 / "run_ood_motion_validation.py"

spec = importlib.util.spec_from_file_location("ood202", M202_PATH)
ood202 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(ood202)


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rows(results_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    cases: list[dict[str, Any]] = []
    for path in sorted(results_dir.glob("*.json")):
        if path.name.endswith(".error.json"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if "rows" not in payload:
            continue
        cases.append(payload["case"])
        rows.extend(payload["rows"])
    return rows, cases


def selected_conditions(cfg: dict[str, Any], present_names: set[str] | None = None) -> tuple[tuple[str, str], ...]:
    lookup = {name: (name, mode) for name, mode in ood202.OOD_CONDITIONS}
    names = [name for name in cfg["conditions"] if present_names is None or name in present_names]
    return tuple(lookup[name] for name in names)


def apply_summary_scope(cfg: dict[str, Any], cases: list[dict[str, Any]]) -> None:
    distances = sorted({float(c["distance_m"]) for c in cases})
    present_conditions = {str(c["condition"]) for c in cases}
    ood202.DISTANCES = tuple(distances)
    ood202.OOD_CONDITIONS = selected_conditions(cfg, present_conditions)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def aggregate(config_path: Path) -> dict[str, Any]:
    cfg = load_config(config_path)
    results_dir = HERE / cfg["results_dir"]
    rows, cases = load_rows(results_dir)
    if not rows:
        raise RuntimeError(f"no case rows found in {results_dir}")
    apply_summary_scope(cfg, cases)
    condition_dicts = [{"name": name, "mode": mode} for name, mode in selected_conditions(cfg, {str(c["condition"]) for c in cases})]
    payload = {
        "config": {
            **cfg,
            "conditions": condition_dicts,
            "completed_cases": len(cases),
            "total_paired_cases": len(cases),
            "completed_policy_rows": len(rows),
            "expected_cases": len(cfg["distances_m"]) * len(cfg["conditions"]) * int(cfg["geoms_per_distance_condition"]),
            "truth_usage": cfg.get("truth_usage", ""),
            "claim_boundary": cfg.get("claim_boundary", ""),
        },
        "summary": ood202.summarize(rows),
        "trials": rows,
    }
    json_path = HERE / cfg.get("aggregate_json", "overnight_ood_validation_aggregate.json")
    md_path = HERE / cfg.get("aggregate_markdown", "overnight_ood_validation_summary.md")
    write_json(json_path, payload)
    md_path.write_text(ood202.markdown(payload), encoding="utf-8")
    print(ood202.markdown(payload))
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=HERE / "overnight_ood_config.json")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    aggregate(args.config)
