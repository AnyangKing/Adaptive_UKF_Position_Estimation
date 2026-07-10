# v1 → v2 change log

## Integrated (v1의 known limitation #5 해소)

1. **Table 1 본문 삽입** — Introduction의 radar/underwater 선행연구 문단 직후(90번
   `table_insertion_notes.md` 지시 위치). 인용 placeholder 미해결 상태이므로 캡션에 draft-status
   명시(지시사항 준수). placeholder를 표의 해당 행에도 부착.
2. **Table 2 본문 삽입** — Section 7 끝, static/moving/quasi-static 세 결과 서술 뒤(지시 위치).
   lead-in 문장 지시문 그대로 사용. 표 아래 비단조 해석 문단(90번 제공) 포함.
3. **Table 3 본문 삽입** — Discussion 말미. 페이지 제한 시 문단 압축 옵션을 캡션에 명시(지시 준수).
   80번 future-work 3방향 문단을 Conclusion 말미에 통합.

## Integrated (v1의 known limitation #2 부분 해소)

4. **Figure Captions 절 신설** — 91번 `figure_caption_drafts.md`의 Fig.1~6 캡션 전문 수록.
5. **Figure File Manifest 절 신설** — 91번 canonical 파일 경로 표. fig7→fig6 개명 결정 반영
   (`manuscript_figure_callout_fix.md`), Fig.5 PNG 미생성 주의 유지.
6. **본문 callout 시제 전환** — "Fig. X will show/report/summarize" → 현재형 6곳,
   "Table 1/2 will ..." → 현재형/위치 안내 3곳 (§1·§3·§4·§5·§6·§7·§8).

## Added

7. **References(placeholder) 절 신설** — 4개 placeholder의 현재 확보 상태 명기:
   FH_USBL(JASA 2007 DOI 확보), COSTAS_USBL(Xplore 9721736, 원문 대조 잔여),
   FREQ_COMB(COA 2024), RADAR_FREQ_AGILITY(Xplore 실존 확인·서지 마무리 잔여 + Nathanson APL 대체원).
8. 문서 머리에 v2 통합 출처(89/90/91) 및 draft 상태 명기.

## Consistency check (90번 체크리스트 전 항목 통과)

- [x] Static primary: 13.01 → 8.87 m, p = 0.0008 유지
- [x] Moving RMSE를 개선으로 서술하지 않음 (-0.10 m, p=0.301 그대로)
- [x] Moving whitening: lag-1 +0.470 → -0.208, p = 5.56e-10 유지
- [x] Quasi-static 연속 경계 0.005 m/s 유지
- [x] 0.030/0.100 m/s 양성은 geometry-dependent/non-continuous로만 서술
- [x] Long-range sub-meter 약속 없음

## Not changed (의도적)

- Abstract 본문(수치·claim 경계 v1 그대로 — 검증된 문안 보존)
- 수식·Method 세부(87→88→89 경로로 이미 통합된 것 유지)
- 인용 placeholder 자체(86번 감사 완료 전 치환 금지 원칙)

## Remaining for v3 / submission

1. 인용 placeholder 실서지 치환(86번 프로토콜 + 도서관 IEEE 접속: TAES 2편 저자/연도,
   IMCOM 2022 원문 차별점 문장 1개 인용)
2. §2 구현 세부를 코드와 대조(배열 반경/높이·표본화·펄스길이·carrier 스케줄·τ·정착 창 —
   89번 quality check #4)
3. 영어 tightening(IEEE 스타일로 산문 압축 — 89번 next_to_v2 Priority 5)
4. Fig.5 PNG 변환(Word 워크플로 필요 시), Fig.1 최종 폴리싱
5. 저널 포맷(2단·수식 번호·참고문헌 스타일)
