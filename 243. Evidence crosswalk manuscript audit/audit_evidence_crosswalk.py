from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENG = ROOT / "paper" / "manuscript.tex"
KOR = ROOT / "paper" / "manuscript_ko.tex"


CHECKS = [
    # Static 600 m and 0--1000 m reconciliation
    ("61 static headline fixed mean", "13.01"),
    ("61 static headline hop mean", "8.87"),
    ("61 static headline p-value", "p=0.0008"),
    ("233 static full-range pooled fixed mean", "10.37"),
    ("233 static full-range pooled hop mean", "8.37"),
    ("233 static full-range p-value", "5.34\\times10^{-9}"),
    ("233 600 m repeat fixed mean", "10.75"),
    ("233 600 m repeat hop mean", "7.99"),
    ("233 600 m repeat gain", "+2.76"),
    ("61 bootstrap interval lower marker", "+2.17"),
    ("61 bootstrap interval upper marker", "+6.05"),
    # Moving-tail and consistency/axis integration
    ("234 residual softR fixed tail", "0.131"),
    ("234 worst cell tail", "0.417"),
    ("234 tangential vertical condition", "tang\\_1.0\\_vz"),
    ("238 plain-hop NEES", "255.84"),
    ("238 softR NEES", "16.00"),
    ("238 total NIS", "3.65"),
    ("239 horizontal RMSE marker", "7.46"),
    ("239 vertical RMSE marker", "4.58"),
    ("241 finite axis n", "511"),
    ("241 full 3D n", "528"),
]

ENGLISH_ONLY_CHECKS = [
    ("pooled full-range static validation stated", "pooled full-range static validation"),
    ("seed-level effect-size variation stated", "seed-level effect-size variation"),
    ("not selecting only larger effect stated", "selection of only the larger effect"),
]

KOREAN_ONLY_CHECKS = [
    ("Korean pooled full-range marker", "pooled한 full-range static validation"),
    ("Korean effect-size variation marker", "effect-size 변동"),
]

FORBIDDEN = [
    "all static distances improved",
    "is tail-free",
    "tail-free guarantee",
    "fully calibrated Bayesian filter",
    "first frequency hopping USBL",
]


def check_markers(label: str, text: str, checks: list[tuple[str, str]]) -> list[str]:
    failures: list[str] = []
    for desc, marker in checks:
        if marker not in text:
            failures.append(f"{label}: missing {desc}: `{marker}`")
    return failures


def main() -> None:
    eng = ENG.read_text(encoding="utf-8")
    kor = KOR.read_text(encoding="utf-8")

    failures: list[str] = []
    failures += check_markers("English", eng, CHECKS + ENGLISH_ONLY_CHECKS)
    failures += check_markers("Korean", kor, CHECKS + KOREAN_ONLY_CHECKS)

    for marker in FORBIDDEN:
        if marker in eng or marker in kor:
            failures.append(f"forbidden overclaim present: `{marker}`")

    out = ROOT / "243. Evidence crosswalk manuscript audit" / "crosswalk_audit_report.md"
    lines = ["# Evidence crosswalk manuscript audit", ""]
    if failures:
        lines.append("## FAIL")
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("## PASS")
        lines.append("")
        lines.append("Core result markers from folders 61, 233, 234, 238, 239, and 241 are present in both English and Korean manuscripts.")
        lines.append("The 61/233 static 600 m effect-size difference is explicitly framed as independent seed-level variation.")
        lines.append("The 233 full-range static result is explicitly described as pooled, not as a second single-range headline.")
        lines.append("Forbidden overclaims were not found.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: evidence crosswalk markers are present and forbidden overclaims are absent.")


if __name__ == "__main__":
    main()
