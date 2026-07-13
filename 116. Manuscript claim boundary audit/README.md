# 116. Manuscript claim boundary audit

## 목적

115번에서 재현성 근거가 정리되었으므로, 이번 단계에서는 원고 문장이 근거보다 세게 나가지 않는지
확인했다. 감사 대상은 현재 로컬 원고 `paper/manuscript.tex`와 주요 원고 초안 계열
85·89·92·94·105번이다.

## 결론

**현재 `paper/manuscript.tex`의 claim boundary는 전반적으로 안전하다.** 특히 아래 위험 주장은 피하고
있다.

- frequency hopping / frequency-agile USBL 자체가 최초라는 주장 없음.
- moving target RMSE improvement를 headline으로 주장하지 않음.
- 0.100 m/s까지 quasi-static이 연속 검증됐다는 주장 없음.
- 600 m sub-meter 성능 주장 없음.
- UKF 자체를 novelty로 포장하지 않음.

## 로컬 원고 패치

GitHub에 올리지 않는 로컬 `paper/manuscript.tex`에 작은 패치 2개를 적용했다.

1. 파일 상단 주석이 “project root”라고 되어 있었는데, 현재 실제 위치는 `paper/`이므로 수정.
2. Future work 문장의 “should first prove”를 “should first show”로 완화.

두 패치는 과학적 결과나 수치를 바꾸지 않는다. 원고 파일은 `paper/`에 있으므로 commit/push 대상이 아니다.

## 산출물

- `claim_boundary_table.md`: 안전/위험 claim 표.
- `paper_scan_findings.md`: 실제 원고 스캔 결과와 로컬 패치 기록.
- `next_patch_queue.md`: 다음 원고 수정 때 반영할 선택사항.

## 다음

116번 기준 다음 순서는 117번 `Related work table finalization`이다. claim boundary는 이미 안전한 편이므로,
이제 리뷰어가 “이미 Costas hopping/comb iUSBL 있지 않나?”라고 물었을 때 바로 방어할 Related Work 표를
원고용으로 더 단단하게 만드는 것이 좋다.
