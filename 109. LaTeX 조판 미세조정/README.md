# 109. LaTeX 조판 미세조정

## 목적

108에서 이관한 루트 `manuscript.tex`의 조판 품질을 다듬는다. **원고 내용·수치·claim은 불변,
조판만 손댄다.** 위치 규칙대로 루트 `manuscript.tex`를 직접 수정(edit in place)했고, 이 폴더는
변경 기록만 담는다.

## 변경 (전부 manuscript.tex 프리앰블/표 스타일)

1. `\setlength{\emergencystretch}{3em}` 프리앰블 추가 — 좁은 IEEE 단에서 문단 줄바꿈 여유 확보.
2. §2.1 초기공분산 인라인 수식 `diag(...)`을 두 수식 그룹으로 분리 — 그 사이 줄바꿈 허용.
3. 세 넓은 표(Table 1~3)의 폰트를 `\footnotesize`→`\scriptsize`, `\tabcolsep`를 6pt→3.5pt로
   축소 — 긴 토큰(예: "TOA/TDOA/DOA-UKF") 셀 넘침 해소.

## 결과 (2026-07-12)

- **Overfull hbox 27건 → 1건**(잔여 1건도 3.3pt로 무시 가능). 미해결 인용/참조 0건 유지. 8쪽 PDF.
- `pdftoppm` 렌더 재확인: 본문(§I~IX)·수식(1~17)·전폭 표(Table I·II) 모두 출판 품질. Table II는
  scriptsize에서 13행 전부 가독, 2단 걸친 캡션 정상.
- 검증: 이 환경 MiKTeX `pdflatex` 재컴파일. 아티팩트는 108의 `.gitignore`로 계속 제외.

## 판정

**조판 미세조정 완료.** 원고는 이제 "표·그림·참고문헌 포함, IEEE 저널 조판 품질" 상태다. 남은
것은 내용 마감(human-author 필드)과 저널 선택별 옵션이지 조판 문제가 아니다.

## 다음

human-author 필드(저자·소속·Funding·Data Availability·Conflicts) 구조화, 저널 선택 후 IEEEtran
옵션(예: `[10pt,journal]`, 길이 제한) 맞춤, 그림 SVG→벡터 PDF 교체(선택).
