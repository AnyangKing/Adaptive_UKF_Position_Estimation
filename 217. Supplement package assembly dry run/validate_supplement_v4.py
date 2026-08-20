"""Validate supplement package v4 source inventory without creating a ZIP."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


REQUIRED_PATTERNS = [
    # Core manuscript evidence
    "61. */README.md",
    "63. */README.md",
    "82. */result_summary.md",
    "145. Two-ray mechanism evidence closure/README.md",
    "191. Moving full range transition aware independent validation/moving_full_range_independent_validation.json",
    "194. Figure and table update for moving full range/moving_full_range_source.csv",
    "204. Overnight OOD validation aggregate result/compact_metrics.json",
    "209. Supplement source data manifest OOD refresh/source_data_manifest_204.md",
    # New weakness patches
    "215. Hardware frequency response sensitivity/hardware_response_sensitivity.json",
    "215. Hardware frequency response sensitivity/result_summary.md",
    "216. Extended OOD motion family validation/extended_ood_motion_family_validation.json",
    "216. Extended OOD motion family validation/result_summary.md",
    # Figure assets referenced by manuscript
    "paper/figures/fig1_system_concept.png",
    "paper/figures/fig2_frequency_agile_bias.png",
    "paper/figures/fig3_static_600m_paired_rmse.png",
    "paper/figures/fig4_moving_whitening_lag1.png",
    "paper/figures/fig5_quasi_static_speed_boundary.png",
    "paper/figures/fig6_crlb_floor.png",
    "paper/figures/fig7_moving_full_range_rmse.png",
    "paper/figures/fig8_moving_full_range_gain_tail.png",
    "paper/figures/fig_tworay_fit.png",
]


EXCLUDED_PREFIXES = [
    "paper/manuscript",
    ".git/",
    ".claude/",
    "study_exports/",
    "203. Overnight OOD validation runner/overnight_results/",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_pattern(pattern: str) -> tuple[str, Path | None]:
    matches = sorted(ROOT.glob(pattern))
    files = [m for m in matches if m.is_file()]
    if not files:
        return pattern, None
    return files[0].relative_to(ROOT).as_posix(), files[0]


def inspect_file(pattern: str) -> dict[str, Any]:
    relative, path = resolve_pattern(pattern)
    if path is None:
        return {"pattern": pattern, "path": relative, "exists": False}
    item: dict[str, Any] = {
        "pattern": pattern,
        "path": relative,
        "exists": True,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    return item


def validate() -> dict[str, Any]:
    files = [inspect_file(p) for p in REQUIRED_PATTERNS]
    missing = [f["path"] for f in files if not f["exists"]]
    payload = {
        "stage": "supplement_package_v4_dry_run",
        "required_count": len(REQUIRED_PATTERNS),
        "missing_count": len(missing),
        "missing": missing,
        "files": files,
        "excluded_prefixes": EXCLUDED_PREFIXES,
        "claim_boundary": "inventory only; no ZIP or public release created",
    }
    (HERE / "supplement_v4_inventory.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    report = [
        "# Supplement package v4 assembly dry-run report",
        "",
        f"- required files: {payload['required_count']}",
        f"- missing files: {payload['missing_count']}",
        f"- status: {'PASS' if not missing else 'FAIL'}",
        "",
        "## Missing files",
        "",
    ]
    if missing:
        report.extend(f"- `{m}`" for m in missing)
    else:
        report.append("- none")
    report.extend([
        "",
        "## Exclusion policy",
        "",
        "- Do not include LaTeX manuscript source/build artifacts unless explicitly approved.",
        "- Do not include raw overnight checkpoint-heavy outputs from folder 203.",
        "- Do not include root handoff/professor/report/study-management MD files.",
        "- Do not include `.git`, `.claude`, caches, or local editor state.",
    ])
    (HERE / "assembly_dry_run_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = validate()
    print(json.dumps({
        "required_count": result["required_count"],
        "missing_count": result["missing_count"],
        "missing": result["missing"],
    }, indent=2, ensure_ascii=False))
