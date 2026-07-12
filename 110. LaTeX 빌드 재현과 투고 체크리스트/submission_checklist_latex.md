# 투고 준비 체크리스트 (LaTeX / IEEEtran 경로)

DOCX용 99·103 체크리스트를 대체한다. 상태 표기: [x] 완료 · [~] 부분 · [ ] 미완(사용자/저자 확정 대기).

## A. 조판·빌드 (AI가 완료 가능 — 대부분 완료)

- [x] IEEEtran journal 문서클래스로 컴파일(`manuscript.tex`, 루트).
- [x] `latexmk` 원커맨드 재현 빌드 + `latexmkrc` (110).
- [x] 8쪽 PDF, 미해결 인용/참조 0건.
- [x] Overfull 27→1건(3.3pt, 무시 가능) — 조판 정리(109).
- [x] 표 3종 전폭(`table*`) scriptsize 배치, 그림 6종 `\includegraphics` 연결.
- [x] 참고문헌 5편 `refs.bib` + IEEEtran.bst 스타일로 연결.
- [ ] 그림을 벡터(PDF/EPS)로 교체(현재 PNG). IEEE는 벡터/고해상 선호 — 선택 개선.
- [ ] 저널 확정 후 문서클래스 옵션(예: `[10pt,journal]`)·길이 제한·컬럼 규격 맞춤.

## B. 내용·수치 무결성 (AI가 검증 — 완료)

- [x] 헤드라인 수치 코드 대조 완료(93): 13.01→8.87 p=0.0008, lag-1 +0.470→−0.208 p=5.6e-10,
      0.005 m/s 경계, n=20/64/132 — 전부 정합.
- [x] claim 경계 유지: moving RMSE 개선 미주장, sub-meter 미약속, "first FH USBL" 미주장,
      0.1 m/s "validated" 미표기.
- [x] §2 adaptive-R 실제 2단계 규칙 반영(94의 P2).
- [x] 5 ms 게이트·구현 파라미터 명시(94의 P1·P3).

## C. human-author 필드 (★ 사용자/저자만 확정 가능 — AI가 지어내지 않음)

- [ ] 저자명·소속·교신저자·ORCID.
- [ ] Author Contributions (CRediT 등 저널 양식).
- [ ] Funding (없으면 저널의 no-funding 문구).
- [ ] Data Availability (리포지토리 URL/DOI 또는 접근 정책 확정).
- [ ] Acknowledgments (선택).
- [ ] Conflicts of Interest (없으면 no-conflict 문구).
  → 현재 원고에 모두 "Human-author decision required" placeholder로 존재. 투고 전 반드시 교체.

## D. 서지 최종 (부분 — 저자 확인 권장)

- [x] 주요 5편 metadata 확보(96) + DOI: radar glint(Loomis 1974), FH-USBL(Beaujean 2007 JASA),
      Costas-USBL(Nhat 2022 IMCOM), frequency-comb iUSBL(Qian 2025), glint background(Delano 1953).
- [~] 저자명 표기·대문자 규칙은 저널 스타일 변환 시 재확인 필요(96 주석).
- [ ] Scopus/WoS/IEEE Xplore로 최근접 선행연구(특히 Costas-USBL) 원문 대조 1회(노벨티 방어).

## E. 저널 선택 (★ 사용자 결정 — 98에 shortlist 있음)

- [ ] 1군(IEEE J. Oceanic Eng. / Ocean Engineering) vs 2군(Applied Acoustics / IEEE Sensors J. /
      MDPI Sensors) 중 확정.
- [ ] 확정 저널의 template·length·figure 규격에 맞춰 최종 조정.

## 요약

**AI 완결 가능 항목(A·B·D 대부분)은 완료.** 남은 것은 본질적으로 **사람이 정해야 하는 것**
(저자 정보 C, 저널 선택 E)과 그에 딸린 조정이다. 지도교수 복귀 후 C·E를 확정하면 투고 준비가
마무리된다.
