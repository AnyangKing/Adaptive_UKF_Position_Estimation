"""Verify manuscript PNG lineage and reproduce the two-ray PNG deterministically."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPORT = HERE / "figure_lineage_report.json"
TWORAY_REPRODUCED = HERE / "fig_tworay_fit_reproduced.png"


FIGURES = [
    {
        "name": "fig1_system_concept.png",
        "paper": "paper/figures/fig1_system_concept.png",
        "reference": "101. Fig1 visual polish/figures/fig1_system_concept_polished.png",
        "generator": "101. Fig1 visual polish/make_fig1_polished.py",
        "data": [],
    },
    {
        "name": "fig2_frequency_agile_bias.png",
        "paper": "paper/figures/fig2_frequency_agile_bias.png",
        "reference": "95. Fig5 PNG and submission packaging/figures/fig2_frequency_agile_bias.png",
        "generator": "70. 논문 그림 1차 생성/generate_core_figures.py",
        "data": ["58. 반송파 미세도약 코히어런트 편향 진단/results/agility.json"],
    },
    {
        "name": "fig3_static_600m_paired_rmse.png",
        "paper": "paper/figures/fig3_static_600m_paired_rmse.png",
        "reference": "95. Fig5 PNG and submission packaging/figures/fig3_static_600m_paired_rmse.png",
        "generator": "70. 논문 그림 1차 생성/generate_core_figures.py",
        "data": ["61. 정지표적 도약 대규모 독립검증/results/static_hop_validation.json"],
    },
    {
        "name": "fig4_moving_whitening_lag1.png",
        "paper": "paper/figures/fig4_moving_whitening_lag1.png",
        "reference": "95. Fig5 PNG and submission packaging/figures/fig4_moving_whitening_lag1.png",
        "generator": "70. 논문 그림 1차 생성/generate_core_figures.py",
        "data": ["63. 이동표적 도약 대규모검증 백색화 확인/results/moving_validation.json"],
    },
    {
        "name": "fig5_quasi_static_speed_boundary.png",
        "paper": "paper/figures/fig5_quasi_static_speed_boundary.png",
        "reference": "95. Fig5 PNG and submission packaging/figures/fig5_quasi_static_speed_boundary.png",
        "generator": "95. Fig5 PNG and submission packaging/generate_fig5_png.py",
        "data": [
            "82. 준정지 속도 경계 검증 실행/results/quasi_static_boundary.json",
            "82. 준정지 속도 경계 검증 실행/results/quasi_static_trials.csv",
        ],
    },
    {
        "name": "fig6_crlb_floor.png",
        "paper": "paper/figures/fig6_crlb_floor.png",
        "reference": "95. Fig5 PNG and submission packaging/figures/fig6_crlb_floor.png",
        "generator": "70. 논문 그림 1차 생성/generate_core_figures.py",
        "data": ["45. CRLB 이론하한 대비 효율/results/crlb.json"],
    },
    {
        "name": "fig_tworay_fit.png",
        "paper": "paper/figures/fig_tworay_fit.png",
        "reference": "153. Figure source lineage closure/fig_tworay_fit_reproduced.png",
        "generator": "138. 이론-실측 오버레이 그림/generate_tworay_fit_figure.py",
        "data": [
            "58. 반송파 미세도약 코히어런트 편향 진단/results/agility.json",
            "145. Two-ray mechanism evidence closure/results/two_ray_fit.json",
        ],
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require_file(relative: str) -> Path:
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(relative)
    return path


def reproduce_tworay() -> None:
    source = require_file("138. 이론-실측 오버레이 그림/generate_tworay_fit_figure.py")
    spec = importlib.util.spec_from_file_location("folder138_tworay_generator", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load folder-138 generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.OUT = TWORAY_REPRODUCED
    module.main()
    if not TWORAY_REPRODUCED.is_file():
        raise RuntimeError("two-ray reproduction did not create a PNG")


def image_comparison(paper: Path, reference: Path) -> dict:
    with Image.open(paper) as paper_image, Image.open(reference) as reference_image:
        p = paper_image.convert("RGBA")
        r = reference_image.convert("RGBA")
        same_size = p.size == r.size
        if same_size:
            diff = ImageChops.difference(p, r)
            exact_pixels = diff.getbbox() is None
            mean_abs = sum(ImageStat.Stat(diff).mean) / 4.0
        else:
            exact_pixels = False
            mean_abs = None
        return {
            "paper_size_px": list(p.size),
            "reference_size_px": list(r.size),
            "same_size": same_size,
            "exact_pixels": exact_pixels,
            "mean_abs_rgba_difference": mean_abs,
        }


def build_report() -> dict:
    reproduce_tworay()
    records = []
    for item in FIGURES:
        paper = require_file(item["paper"])
        reference = require_file(item["reference"])
        generator = require_file(item["generator"])
        data_paths = [require_file(path) for path in item["data"]]
        comparison = image_comparison(paper, reference)
        records.append(
            {
                **item,
                "paper_bytes": paper.stat().st_size,
                "paper_sha256": sha256(paper),
                "reference_bytes": reference.stat().st_size,
                "reference_sha256": sha256(reference),
                "generator_sha256": sha256(generator),
                "data_sha256": {path.as_posix().replace(ROOT.as_posix() + "/", ""): sha256(path) for path in data_paths},
                "byte_identical": sha256(paper) == sha256(reference),
                **comparison,
            }
        )
    return {
        "schema": "figure-source-lineage-1",
        "figure_count": len(records),
        "byte_identical_count": sum(record["byte_identical"] for record in records),
        "pixel_identical_count": sum(record["exact_pixels"] for record in records),
        "all_generators_present": True,
        "all_data_sources_present": True,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    current = build_report()
    if args.write:
        REPORT.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"wrote {REPORT.name}: {current['byte_identical_count']}/{current['figure_count']} byte-identical, "
            f"{current['pixel_identical_count']}/{current['figure_count']} pixel-identical"
        )
        return 0
    if not REPORT.is_file():
        print("missing report; run with --write")
        return 1
    expected = json.loads(REPORT.read_text(encoding="utf-8"))
    if current != expected:
        print("figure lineage drift detected")
        return 1
    if current["pixel_identical_count"] != current["figure_count"]:
        print("one or more paper figures differ from their reproducible reference")
        return 1
    print(f"ok: {current['figure_count']}/{current['figure_count']} figures have exact pixel lineage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
