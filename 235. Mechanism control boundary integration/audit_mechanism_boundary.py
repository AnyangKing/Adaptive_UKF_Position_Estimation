from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "manuscript.tex"
DIRECT_185 = ROOT / "185. Direct path only carrier agility control" / "result_summary.md"
DIRECT_187 = ROOT / "187. No noise direct path carrier control" / "result_summary.md"


REQUIRED_MANUSCRIPT_MARKERS = [
    "Direct-path control runs",
    "no-noise direct-path control",
    "carrier-dependent observation-extraction and noise-response interactions",
    "not as proof that all improvement arises only from two-ray multipath phase rotation",
]

REQUIRED_SOURCE_MARKERS = {
    DIRECT_185: [
        "direct-only control",
        "1000 m",
        "carrier-agility gain",
    ],
    DIRECT_187: [
        "No-noise direct-path control",
        "did **not** survive",
        "observation-extraction/noise interactions",
    ],
}

FORBIDDEN_MANUSCRIPT_MARKERS = [
    "Carrier agility improves long-range USBL only by rotating coherent multipath phase",
    "all long-range carrier-agile gain comes from in-gate coherent multipath phase rotation",
]


def main() -> None:
    manuscript = PAPER.read_text(encoding="utf-8", errors="replace")
    manuscript_flat = " ".join(manuscript.split())
    failures: list[str] = []
    lines = [
        "# Mechanism control boundary audit",
        "",
        "## Manuscript markers",
        "",
    ]
    for marker in REQUIRED_MANUSCRIPT_MARKERS:
        ok = " ".join(marker.split()) in manuscript_flat
        lines.append(f"- {'OK' if ok else 'MISSING'}: `{marker}`")
        if not ok:
            failures.append(f"Missing manuscript marker: {marker}")

    lines.extend(["", "## Source evidence markers", ""])
    for path, markers in REQUIRED_SOURCE_MARKERS.items():
        text = path.read_text(encoding="utf-8", errors="replace")
        lines.append(f"### {path.parent.name}")
        for marker in markers:
            ok = marker in text
            lines.append(f"- {'OK' if ok else 'MISSING'}: `{marker}`")
            if not ok:
                failures.append(f"Missing source marker in {path}: {marker}")
        lines.append("")

    lines.extend(["## Forbidden over-attribution markers", ""])
    for marker in FORBIDDEN_MANUSCRIPT_MARKERS:
        ok = " ".join(marker.split()) not in manuscript_flat
        lines.append(f"- {'OK' if ok else 'HIT'}: `{marker}`")
        if not ok:
            failures.append(f"Forbidden over-attribution marker hit: {marker}")

    status = "PASS" if not failures else "FAIL"
    lines.insert(2, f"Status: **{status}**")
    lines.extend(["", "## Failures", ""])
    lines.extend([f"- {f}" for f in failures] or ["- None"])
    out = Path(__file__).resolve().parent / "mechanism_boundary_audit_report.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(status)
    print(out)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
