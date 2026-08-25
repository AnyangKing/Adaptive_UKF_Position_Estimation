"""Audit finite-n clarification for axis-wise diagnostics."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENG = ROOT / "paper" / "manuscript.tex"
KOR = ROOT / "paper" / "manuscript_ko.tex"


def main() -> None:
    eng = ENG.read_text(encoding="utf-8")
    kor = KOR.read_text(encoding="utf-8")
    assert "511 cases with finite settled axis metrics" in eng
    assert "full 3-D RMSE and divergence validation" in eng
    assert "528 cases" in eng
    assert "511 cases를 사용" in kor
    assert "전체 3D RMSE와 발산률 검증은 528 cases 전체" in kor
    assert kor.count("\\caption{표~\\ref{tab:movingfull}와 같은 528개 structured moving-target paired cases") == 1
    print("PASS: finite-n clarification is present in English/Korean manuscripts.")


if __name__ == "__main__":
    main()

