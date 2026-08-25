from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "paper" / "manuscript.tex"
KO = ROOT / "paper" / "manuscript_ko.tex"
SRC_191 = ROOT / "191. Moving full range transition aware independent validation" / "run_moving_full_range_independent_validation.py"
SRC_233 = ROOT / "233. Static full range independent validation" / "run_static_full_range_independent_validation.py"
REPORT = Path(__file__).resolve().parent / "audit_report.md"


CHECKS = [
    ("English divergence threshold definition", EN, "exceeds 50~m"),
    ("English divergence failure-fraction wording", EN, "thresholded failure"),
    ("English Wilcoxon signed-rank naming", EN, "Wilcoxon signed-rank test"),
    ("English one-sided alternative", EN, "alternative: gain $>0$"),
    ("English bootstrap CI naming", EN, "bootstrap 95\\% confidence interval"),
    ("English descriptive breakdown boundary", EN, "Distance-wise and cell-wise breakdowns are reported as\ndescriptive diagnostics"),
    ("English pooled confirmatory boundary", EN, "confirmatory claims rely on the pre-specified pooled paired comparisons"),
    ("Korean divergence threshold definition", KO, "3D 위치오차가 50 m를 넘는 경우"),
    ("Korean failure-fraction wording", KO, "실패 trial의 비율"),
    ("Korean Wilcoxon signed-rank naming", KO, "one-sided Wilcoxon signed-rank test"),
    ("Korean one-sided alternative", KO, "gain $>0$"),
    ("Korean bootstrap CI naming", KO, "bootstrap 95\\% confidence interval"),
    ("Korean descriptive breakdown boundary", KO, "거리별 표와 cell별 tail 분해는 기술통계"),
    ("Korean pooled confirmatory boundary", KO, "사전 지정된 pooled paired comparison"),
    ("191 source divergence threshold", SRC_191, "errors > 50.0"),
    ("191 source Wilcoxon greater", SRC_191, 'wilcoxon(gains, alternative="greater")'),
    ("233 source Wilcoxon greater", SRC_233, 'wilcoxon(gains, alternative="greater")'),
]


FORBIDDEN = [
    ("English unsupported corrected per-cell significance", EN, "Bonferroni-significant cell"),
    ("English unsupported all-cell confirmatory claim", EN, "cell-wise confirmatory"),
    ("Korean unsupported corrected per-cell significance", KO, "Bonferroni 유의"),
    ("Korean unsupported all-cell confirmatory claim", KO, "cell별 확증"),
]


def main() -> int:
    failures = []
    lines = ["# Statistical reporting definitions audit", ""]
    for label, path, needle in CHECKS:
        text = path.read_text(encoding="utf-8")
        ok = needle in text
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] {label}: `{needle}`")
        if not ok:
            failures.append(label)

    lines.extend(["", "## Forbidden unsupported-claim scan", ""])
    for label, path, needle in FORBIDDEN:
        text = path.read_text(encoding="utf-8")
        ok = needle not in text
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] {label}: `{needle}`")
        if not ok:
            failures.append(label)

    lines.extend(["", "## Verdict", ""])
    if failures:
        lines.append("FAIL")
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("PASS")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT)
    print("PASS" if not failures else "FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
