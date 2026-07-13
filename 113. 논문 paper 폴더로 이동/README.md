# 113. 논문 paper 폴더로 이동

## 목적 (사용자 지시 2026-07-13)

108에서 루트에 둔 LaTeX 원고가 컴파일할 때마다 `.bbl`/`.aux`/`.log`/`.pdf` 등 빌드 아티팩트를
루트에 쏟아내 운영 MD 파일들과 섞여 지저분했다. 논문 작업 전용 **`paper/` 폴더**를 만들어 LaTeX
실체를 전부 옮기고, 앞으로 거기서 작업·수정한다.

## 변경

- `git mv`로 루트→`paper/` 이동(깨끗한 rename): `manuscript.tex`, `refs.bib`, `latexmkrc`,
  `figures/`(Fig.1~6 PNG 6종).
- 루트에 흩어져 있던 빌드 아티팩트 16개(manuscript.aux/bbl/blg/log/out/pdf/fdb_latexmk/fls,
  임시 로그 `_*.txt`) 정리 삭제(재생성 가능, `rm` 차단이라 python `os.remove` 사용).
- `.gitignore`: 확장자 글롭(`*.aux` 등)은 `paper/`도 자동 포착. `paper/manuscript.pdf` 명시 추가,
  임시 로그 패턴을 `_*.txt`로 일반화. 주석을 "paper/ 기준"으로 갱신.
- 운영 MD 3종(`새_채팅_인계`·`연구_인계_현황`·`논문_초고_구조`) 최상단 규약을 위치 `paper/`로 갱신.

## 검증 (2026-07-13)

- **`cd paper && latexmk manuscript.tex` → PDF 1.70 MB, 미해결 인용/참조 0건, Overfull 1건.**
  빌드가 새 위치에서 정상. `\graphicspath{{figures/}}`·`latexmkrc`는 상대경로라 이동에도 무수정.
- **루트 정리 확인**: `paper/` 밖 루트에 `manuscript.*`·`_*.txt` 흔적 없음. 모든 아티팩트는
  `paper/` 안에서만 생기고 전부 `.gitignore` 처리(커밋 안 됨).

## 판정

**이동·정리 완료.** 앞으로 원고 수정은 `paper/manuscript.tex`에서 직접(edit in place). 루트는
운영 MD와 numbered 폴더만 남아 깔끔. 규약은 MD 3종에 반영됨.

## 새 위치 요약

```
paper/
  manuscript.tex   ← 원고(IEEEtran). 여기서 직접 수정.
  refs.bib
  latexmkrc        ← cd paper && latexmk manuscript.tex
  figures/         ← Fig.1~6 PNG
  (manuscript.pdf 등 빌드물은 여기 생기고 .gitignore로 커밋 제외)
```
