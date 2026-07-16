# 147. Manuscript float and structure audit

## 목적

현재 12쪽 IEEE-neutral LaTeX 원고의 섹션 구조, 그림/표 배치, float 순서, 제출 전 위험요소를 점검했다.

이번 폴더는 원고를 직접 수정하지 않는다. `paper/`는 local-only/ignored 상태를 유지하고, 투고 전 반영할 patch 후보만 정리한다.

## 결론

원고의 큰 구조는 IEEE식 논문으로 충분히 자연스럽다.

현재 흐름:

1. Introduction
2. Related Work and Problem Statement
3. System Model and UKF Fusion
4. Baseline Tracking Performance
5. Proposed Carrier-Agile Whitening Method
6. Experimental Validation and Applicability Boundary
7. Discussion
8. Conclusion
9. Supplementary Material and Data Availability / Acknowledgment

이 구조는 “문제 제기 → 기존 방법 한계 → 제안 기전 → 검증 → 경계/논의”로 읽혀서 좋다. 6~7쪽일 때와 달리 12쪽 원고는 연구량이 너무 작아 보이는 문제도 상당히 해소됐다.

## 남은 제출 전 수정 후보

우선순위는 다음과 같다.

1. Data Availability 문장의 figure 범위 수정: 현재 `Figs. concept--floor` 식으로 읽혀 Fig. static/moving/quasi/tworay가 빠져 보일 수 있다.
2. `fig_tworay_fit.png`의 생성 경로를 145번 closure와 연결: claim은 닫혔지만 PNG production path를 명시하면 더 좋다.
3. float 순서 확인: `fig6_crlb_floor.png`가 파일명은 fig6이지만 본문상 앞쪽에 배치된다. 논문 내부 label/caption은 괜찮지만 supplement manifest에서는 “file number != manuscript order”를 조심해야 한다.
4. `table*` 두 개(`tab:priorart`, `tab:results`, `tab:limitations`)가 IEEE double-column float로 페이지 상단 이동할 수 있으므로 최종 PDF visual QA에서 주변 문맥과 맞는지 확인해야 한다.

## 산출물

- `structure_audit.md` — 섹션/float 구조 감사
- `patch_suggestions.md` — 원고에 적용할 수 있는 안전한 수정 후보
- `final_pdf_qa_checklist.md` — 최종 PDF 육안검사 체크리스트
