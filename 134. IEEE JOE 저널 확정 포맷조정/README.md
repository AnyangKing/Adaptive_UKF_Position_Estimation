# 134. IEEE JOE 저널 확정 포맷조정

## 목적 (사용자 지시 2026-07-13)

**투고 저널을 IEEE Journal of Oceanic Engineering (IEEE JOE)으로 확정.** 이 논문 주제(수중 음향·
USBL·측위)에 정확히 맞는 저널이다. IEEE JOE는 표준 IEEE Transactions 계열이라 **IEEEtran journal
클래스가 그대로 정답** — 원고가 이미 올바른 기반이었고, 저널-특화 관례 조정만 수행했다.
(※ 이전에 착오로 나온 Elsevier "Ocean Engineering"과는 다른 저널.)

## 변경 (`paper/manuscript.tex`, edit in place)

1. **문서클래스**: `\documentclass[journal]{IEEEtran}` 유지(IEEE JOE의 정답). 프리앰블 주석에 타깃
   저널 명시.
2. **Running head**: `\markboth{IEEE JOURNAL OF OCEANIC ENGINEERING (SUBMISSION DRAFT)}{AUTHOR
   et al.: CARRIER-AGILE WHITENING ...}` — IEEE 저널 관례.
3. **저자/Funding**: `\thanks`를 IEEE 관례로 재작성 — "Manuscript submitted to IEEE JOE",
   **Funding을 first-page 각주(\thanks)로 이동**(IEEE는 Funding을 별도 섹션으로 두지 않음), 소속·
   교신저자 placeholder. 저자명은 `First A. Author, ...` placeholder.
4. **Back matter를 IEEE 관례로 재구성**:
   - **제거**: `Author Contributions`, `Conflicts of Interest` (MDPI/Elsevier 관례이지 IEEE JOE
     섹션이 아님; 이해상충은 IEEE 투고 시스템에서 선언).
   - **제거**: 별도 `Funding` 섹션(→ \thanks로 이동).
   - **유지·통합**: `Supplementary Material and Data Availability` 한 절로 간결화.
   - **유지**: `Acknowledgment`(IEEE 단수 철자, 참고문헌 직전 unnumbered) — placeholder.

## 검증 (2026-07-13)

- `cd paper && latexmk manuscript.tex` → **9쪽, 미해결 인용/참조 0, overfull 0**, LaTeX 에러 없음.
- 1쪽 렌더: running head=IEEE JOE, 저자 placeholder, \thanks 각주(투고처·펀딩·소속) 정상.
- 마지막 쪽 렌더: MDPI식 섹션 사라지고 Acknowledgment+References로 IEEE 관례 정리, 참고문헌 10편 정상.

## 판정

**IEEE JOE 포맷 조정 완료.** "저널 정해지면 양식 전환" 계획이 이로써 완료됨(IEEE JOE=IEEEtran이라
추가 전환 불필요). 원고는 이제 **IEEE JOE 제출 양식 기준**으로 서 있으며, 남은 것은 사람 결정
(저자명·소속·교신저자·Funding 내용·Acknowledgment·Data 정책)뿐 — 133번 인계 체크리스트의 행번호
참조(단, back matter 구조가 이번에 IEEE식으로 바뀌었으니 저자정보·Funding은 \thanks에, 나머지는
Acknowledgment/Data 절에 넣으면 됨).

## 다음

투고 전 실무: (a) IEEE JOE author guidelines의 분량·그림 규격 최종 확인(공식 페이지), (b) 저자 정보
입력, (c) IEEEtran 최신 클래스 파일로 제출 패키지화. 그 외는 사람 결정.
