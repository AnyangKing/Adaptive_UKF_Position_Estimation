"""Build and verify a content-addressed dry-run manifest for the supplement.

This script never copies source artifacts and never creates a ZIP.  It records
only relative source paths, proposed archive paths, byte sizes, and SHA256
digests inside folder 152.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / "supplement_v2_manifest.json"


FIXED_ARTIFACTS = [
    ("data", "data/crlb.json", "45. CRLB 이론하한 대비 효율/results/crlb.json"),
    ("data", "data/agility.json", "58. 반송파 미세도약 코히어런트 편향 진단/results/agility.json"),
    ("data", "data/static_hop_validation.json", "61. 정지표적 도약 대규모 독립검증/results/static_hop_validation.json"),
    ("data", "data/moving_validation.json", "63. 이동표적 도약 대규모검증 백색화 확인/results/moving_validation.json"),
    ("data", "data/quasi_static_boundary.json", "82. 준정지 속도 경계 검증 실행/results/quasi_static_boundary.json"),
    ("data", "data/quasi_static_trials.csv", "82. 준정지 속도 경계 검증 실행/results/quasi_static_trials.csv"),
    ("data", "data/method_facts.json", "93. Method 세부 코드 대조/results/method_facts.json"),
    ("data", "data/two_ray_fit.json", "145. Two-ray mechanism evidence closure/results/two_ray_fit.json"),
    ("figure", "figures/fig1_system_concept.png", "paper/figures/fig1_system_concept.png"),
    ("figure", "figures/fig2_frequency_agile_bias.png", "paper/figures/fig2_frequency_agile_bias.png"),
    ("figure", "figures/fig3_static_600m_paired_rmse.png", "paper/figures/fig3_static_600m_paired_rmse.png"),
    ("figure", "figures/fig4_moving_whitening_lag1.png", "paper/figures/fig4_moving_whitening_lag1.png"),
    ("figure", "figures/fig5_quasi_static_speed_boundary.png", "paper/figures/fig5_quasi_static_speed_boundary.png"),
    ("figure", "figures/fig6_crlb_floor.png", "paper/figures/fig6_crlb_floor.png"),
    ("figure", "figures/fig_tworay_fit.png", "paper/figures/fig_tworay_fit.png"),
    ("figure", "figures/two_ray_fit.svg", "145. Two-ray mechanism evidence closure/results/two_ray_fit.svg"),
    ("figure_script", "figure_scripts/make_fig1_polished.py", "101. Fig1 visual polish/make_fig1_polished.py"),
    ("figure_script", "figure_scripts/generate_core_figures.py", "70. 논문 그림 1차 생성/generate_core_figures.py"),
    ("figure_script", "figure_scripts/generate_fig5_png.py", "95. Fig5 PNG and submission packaging/generate_fig5_png.py"),
    ("figure_script", "figure_scripts/reproduce_tworay_fit.py", "145. Two-ray mechanism evidence closure/reproduce_tworay_fit.py"),
    ("document", "docs/claim_to_artifact_matrix.md", "144. Manuscript claim traceability audit/claim_traceability_matrix.md"),
    ("document", "docs/figure_source_manifest.md", "146. Figure and table source-data manifest refresh/figure_source_manifest.md"),
    ("document", "docs/table_source_manifest.md", "146. Figure and table source-data manifest refresh/table_source_manifest.md"),
    ("document", "docs/submission_package_policy.md", "146. Figure and table source-data manifest refresh/submission_package_policy.md"),
    ("document", "docs/current_submission_state.md", "149. Manifest correction and supplement closeout/current_submission_state.md"),
]


CODE_GROUPS = [
    ("45_crlb_floor", "45. CRLB 이론하한 대비 효율"),
    ("58_carrier_sensitivity", "58. 반송파 미세도약 코히어런트 편향 진단"),
    ("61_static_validation", "61. 정지표적 도약 대규모 독립검증"),
    ("63_moving_boundary", "63. 이동표적 도약 대규모검증 백색화 확인"),
    ("82_quasi_static_boundary", "82. 준정지 속도 경계 검증 실행"),
    ("93_method_audit", "93. Method 세부 코드 대조"),
    ("145_two_ray_closure", "145. Two-ray mechanism evidence closure"),
]


FORBIDDEN_SOURCE_PARTS = {".git", ".claude", "study_exports", "__pycache__"}
FORBIDDEN_SOURCE_SUFFIXES = {".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".pdf", ".tex"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def code_artifacts() -> list[tuple[str, str, str]]:
    items: list[tuple[str, str, str]] = []
    for archive_group, source_group in CODE_GROUPS:
        source_dir = ROOT / source_group
        selected = sorted(source_dir.glob("*.py"))
        for optional in ("README.md", "result_summary.md"):
            candidate = source_dir / optional
            if candidate.exists():
                selected.append(candidate)
        for source in sorted(set(selected)):
            relative = source.relative_to(ROOT).as_posix()
            archive = f"code/{archive_group}/{source.name}"
            items.append(("code", archive, relative))
    return items


def validate_source_policy(source: str) -> None:
    path = Path(source)
    if any(part in FORBIDDEN_SOURCE_PARTS for part in path.parts):
        raise ValueError(f"forbidden source path: {source}")
    if path.suffix.lower() in FORBIDDEN_SOURCE_SUFFIXES:
        raise ValueError(f"forbidden source suffix: {source}")
    if source.startswith("paper/") and not source.startswith("paper/figures/"):
        raise ValueError(f"only paper/figures is allowed: {source}")


def build_manifest() -> dict:
    candidates = FIXED_ARTIFACTS + code_artifacts()
    archive_paths = [archive for _, archive, _ in candidates]
    duplicates = [name for name, count in Counter(archive_paths).items() if count > 1]
    if duplicates:
        raise ValueError(f"duplicate archive paths: {duplicates}")

    entries = []
    for category, archive, source in sorted(candidates, key=lambda item: item[1]):
        validate_source_policy(source)
        source_path = ROOT / source
        if not source_path.is_file():
            raise FileNotFoundError(source)
        entries.append(
            {
                "category": category,
                "archive_path": archive,
                "source_path": source,
                "bytes": source_path.stat().st_size,
                "sha256": sha256(source_path),
            }
        )

    category_counts = dict(sorted(Counter(entry["category"] for entry in entries).items()))
    return {
        "schema": "supplement-v2-dry-run-1",
        "policy": {
            "copies_raw_files": False,
            "creates_zip": False,
            "includes_manuscript_source": False,
            "includes_manuscript_pdf": False,
            "figures_from_local_paper_allowed": True,
        },
        "artifact_count": len(entries),
        "total_bytes": sum(entry["bytes"] for entry in entries),
        "category_counts": category_counts,
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the current dry-run manifest")
    args = parser.parse_args()
    current = build_manifest()

    if args.write:
        MANIFEST.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {MANIFEST.name}: {current['artifact_count']} artifacts, {current['total_bytes']} bytes")
        return 0

    if not MANIFEST.exists():
        print(f"missing {MANIFEST.name}; run with --write first")
        return 1
    expected = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if current != expected:
        print("manifest drift detected; inspect source changes before running --write")
        return 1
    print(f"ok: {current['artifact_count']} artifacts, {current['total_bytes']} bytes, no drift")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
