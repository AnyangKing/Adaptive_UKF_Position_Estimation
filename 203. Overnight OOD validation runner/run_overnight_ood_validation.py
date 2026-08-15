"""Checkpoint/resume runner for large OOD motion validation."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import time
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
    cfg = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "distances_m",
        "conditions",
        "geoms_per_distance_condition",
        "geometry_seed_root",
        "ping_seed_root",
        "results_dir",
    }
    missing = sorted(required - set(cfg))
    if missing:
        raise ValueError(f"missing config keys: {missing}")
    return cfg


def condition_lookup() -> dict[str, tuple[str, str]]:
    return {name: (name, mode) for name, mode in ood202.OOD_CONDITIONS}


def selected_conditions(cfg: dict[str, Any]) -> list[tuple[int, tuple[str, str]]]:
    lookup = condition_lookup()
    selected = []
    for name in cfg["conditions"]:
        if name not in lookup:
            raise ValueError(f"unknown OOD condition: {name}")
        original_idx = [c[0] for c in ood202.OOD_CONDITIONS].index(name)
        selected.append((original_idx, lookup[name]))
    return selected


def enumerate_cases(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    cases = []
    for distance in cfg["distances_m"]:
        for cond_idx, cond in selected_conditions(cfg):
            for index in range(int(cfg["geoms_per_distance_condition"])):
                cases.append({
                    "distance_m": float(distance),
                    "condition_index": int(cond_idx),
                    "condition": cond[0],
                    "mode": cond[1],
                    "index": int(index),
                })
    return cases


def case_id(case: dict[str, Any]) -> str:
    d = int(round(float(case["distance_m"])))
    return f"d{d:04d}_{case['condition']}_i{int(case['index']):03d}"


def result_path(results_dir: Path, case: dict[str, Any]) -> Path:
    return results_dir / f"{case_id(case)}.json"


def apply_seed_roots(cfg: dict[str, Any]) -> None:
    ood202.GEOM_ROOT = int(cfg["geometry_seed_root"])
    ood202.PING_ROOT = int(cfg["ping_seed_root"])


def run_one_case(case: dict[str, Any]) -> dict[str, Any]:
    cond = (case["condition"], case["mode"])
    rows = ood202.run_case(
        float(case["distance_m"]),
        int(case["condition_index"]),
        cond,
        int(case["index"]),
    )
    return {
        "case_id": case_id(case),
        "case": case,
        "rows": rows,
    }


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def run(config_path: Path, resume: bool = True, overwrite: bool = False, max_cases: int | None = None) -> dict[str, Any]:
    cfg = load_config(config_path)
    apply_seed_roots(cfg)
    results_dir = HERE / cfg["results_dir"]
    results_dir.mkdir(parents=True, exist_ok=True)
    cases = enumerate_cases(cfg)
    if max_cases is not None:
        cases = cases[: int(max_cases)]

    started = time.time()
    completed = 0
    skipped = 0
    failed = 0
    for ordinal, case in enumerate(cases, 1):
        out = result_path(results_dir, case)
        if out.exists() and resume and not overwrite:
            skipped += 1
            print(f"[skip] {ordinal}/{len(cases)} {case_id(case)}")
            continue
        t0 = time.time()
        try:
            payload = run_one_case(case)
            payload["runtime_s"] = time.time() - t0
            payload["config_snapshot"] = {
                "geometry_seed_root": cfg["geometry_seed_root"],
                "ping_seed_root": cfg["ping_seed_root"],
                "truth_usage": cfg.get("truth_usage", ""),
                "claim_boundary": cfg.get("claim_boundary", ""),
            }
            write_json_atomic(out, payload)
            completed += 1
            print(f"[done] {ordinal}/{len(cases)} {case_id(case)} {payload['runtime_s']:.1f}s")
        except Exception as exc:
            failed += 1
            err_payload = {
                "case_id": case_id(case),
                "case": case,
                "error": repr(exc),
                "runtime_s": time.time() - t0,
            }
            write_json_atomic(out.with_suffix(".error.json"), err_payload)
            print(f"[fail] {ordinal}/{len(cases)} {case_id(case)} {exc!r}")

    summary = {
        "config": cfg,
        "results_dir": str(results_dir),
        "cases_requested": len(cases),
        "completed_this_run": completed,
        "skipped_existing": skipped,
        "failed_this_run": failed,
        "elapsed_s": time.time() - started,
    }
    write_json_atomic(HERE / "overnight_runner_last_run.json", summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=HERE / "overnight_ood_config.json")
    parser.add_argument("--resume", action="store_true", default=True)
    parser.add_argument("--no-resume", dest="resume", action="store_false")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--max-cases", type=int, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = run(args.config, resume=args.resume, overwrite=args.overwrite, max_cases=args.max_cases)
    print(json.dumps(result, indent=2, ensure_ascii=False))
