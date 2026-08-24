from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "paper" / "manuscript.tex"
KO = ROOT / "paper" / "manuscript_ko.tex"
STATIC = ROOT / "233. Static full range independent validation" / "result_summary.md"
TAIL = ROOT / "234. Moving tail case decomposition" / "result_summary.md"
REPORT = Path(__file__).resolve().parent / "audit_report.md"


CHECKS = [
    ("English manuscript has static full-range sample count", EN, "220 paired"),
    ("English manuscript has static full-range mean fixed RMSE", EN, "10.37"),
    ("English manuscript has static full-range mean hop RMSE", EN, "8.37"),
    ("English manuscript has static full-range p-value", EN, "5.34\\times10^{-9}"),
    ("English manuscript has non-monotonic static boundary", EN, "0, 200, and\n500"),
    ("English manuscript has moving residual tail fraction", EN, "0.131"),
    ("English manuscript has worst moving tail cell", EN, "0.417"),
    ("English manuscript has tangential vertical risk marker", EN, "tang\\_1.0\\_vz"),
    ("Korean manuscript has static full-range sample count", KO, "220 paired"),
    ("Korean manuscript has static full-range mean fixed RMSE", KO, "10.37"),
    ("Korean manuscript has static full-range mean hop RMSE", KO, "8.37"),
    ("Korean manuscript has static full-range p-value", KO, "5.34\\times10^{-9}"),
    ("Korean manuscript has non-monotonic static boundary", KO, "0/200/500"),
    ("Korean manuscript has moving residual tail fraction", KO, "0.131"),
    ("Korean manuscript has worst moving tail cell", KO, "0.417"),
    ("Korean manuscript has tangential vertical risk marker", KO, "tang\\_1.0\\_vz"),
    ("Static source has original p-value", STATIC, "5.343e-09"),
    ("Static source has original n", STATIC, "| hop_vs_fixed | 2.001"),
    ("Tail source has original residual tail", TAIL, "softR vs fixed tail worsened fraction: 0.131"),
    ("Tail source has original worst cell", TAIL, "| 700.000 | radial_1.0 | 12 | 3.337 | 0.417"),
]

FORBIDDEN = [
    ("English all-distance overclaim", EN, "carrier agility reliably improves every static geometry"),
    ("English all-distance overclaim 2", EN, "carrier agility improves all static ranges."),
    ("Korean all-distance overclaim", KO, "모든 거리에서 항상 개선된다"),
    ("Korean all-distance overclaim 2", KO, "모든 거리에서 동일하게 개선된다"),
    ("English tail-free overclaim", EN, "eliminates tail risk"),
    ("Korean tail-free overclaim", KO, "tail 위험을 제거했다"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures = []
    lines = ["# 233/234 manuscript integration audit", ""]

    for label, path, needle in CHECKS:
        text = read(path)
        ok = needle in text
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] {label}: `{needle}`")
        if not ok:
            failures.append(label)

    lines.extend(["", "## Forbidden overclaim scan", ""])
    for label, path, needle in FORBIDDEN:
        text = read(path)
        ok = needle not in text
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] {label}: `{needle}`")
        if not ok:
            failures.append(label)

    lines.extend(["", "## Verdict", ""])
    if failures:
        lines.append("FAIL")
        lines.extend(f"- {f}" for f in failures)
    else:
        lines.append("PASS")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT)
    print("PASS" if not failures else "FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
