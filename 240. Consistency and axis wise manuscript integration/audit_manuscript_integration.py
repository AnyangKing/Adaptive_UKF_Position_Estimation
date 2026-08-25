"""Audit manuscript integration for folders 238 and 239."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENG = ROOT / "paper" / "manuscript.tex"
KOR = ROOT / "paper" / "manuscript_ko.tex"


REQUIRED_ENG = [
    "position NEES from 255.84 for plain hopping to 16.00",
    "total-NIS 99\\% exceedance fraction from 0.119 to 0.038",
    "not be described as a fully calibrated",
    "horizontal RMSE drops from 7.46 to 4.85~m",
    "7.44 to 4.58~m",
    "\\label{tab:consistencyaxis}",
    "robust adaptive covariance-inflation rule",
]

REQUIRED_KOR = [
    "position NEES 255.84를 16.00으로",
    "99\\% tail 초과율도 0.119에서 0.038",
    "완전히 calibrated된 Bayesian filter라고 표현하지 않는다",
    "horizontal RMSE는 7.46 m에서 4.85 m",
    "vertical RMSE는 7.44 m에서 4.58 m",
    "\\label{tab:consistencyaxis}",
    "adaptive covariance inflation rule",
]

FORBIDDEN = [
    "fully calibrated Bayesian filter.",
    "perfectly calibrated",
    "DOA block NIS was the dominant",
    "DOA block NIS가",
    "6.80",
]


def check(path: Path, required: list[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    missing = [marker for marker in required if marker not in text]
    forbidden = [marker for marker in FORBIDDEN if marker in text]
    problems = []
    if missing:
        problems.append(f"{path.name} missing markers: {missing}")
    if forbidden:
        problems.append(f"{path.name} forbidden markers: {forbidden}")
    return problems


def main() -> None:
    problems = []
    problems.extend(check(ENG, REQUIRED_ENG))
    problems.extend(check(KOR, REQUIRED_KOR))
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    print("PASS: 238/239 consistency and axis-wise results are integrated with claim boundaries.")


if __name__ == "__main__":
    main()
