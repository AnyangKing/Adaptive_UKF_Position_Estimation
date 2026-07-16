# 141. Expanded manuscript warning cleanup

## 목적

140번 시각 QA에서 확인한 12쪽 확장 원고의 LaTeX warning을 claim-safe 조판 수정으로 줄였다.

대상:

- Underfull hbox lines 100--110
- Underfull hbox lines 371--383
- Overfull hbox line 604
- Underfull vbox page-balancing warnings

## 결과

최종 빌드:

```text
Output written on manuscript.pdf (12 pages, 1929675 bytes).
```

최종 warning 상태:

| 항목 | 140번 기준 | 141번 후 |
|---|---:|---:|
| Overfull hbox | 1 | 0 |
| Underfull hbox | 4 | 0 |
| Underfull vbox | 1 | 2 |
| unresolved citation/reference | 0 | 0 |
| rerun needed | 0 | 0 |
| PDF pages | 12 | 12 |

남은 경고:

```text
Underfull \vbox (badness 3701) has occurred while \output is active []
Underfull \vbox (badness 10000) has occurred while \output is active []
```

해석:

- 문장 overflow/underfull 문제는 해소됐다.
- 남은 vbox 경고는 page balancing/float placement 성격이다.
- 140번 시각 QA에서 전체 페이지 흐름이 크게 깨지지 않았으므로, 현 단계에서는 치명적이지 않다.

## 적용한 패치

1. Related Work의 DOA estimation 문단을 줄바꿈 친화적으로 재작성.
2. Estimator Comparison 문단을 두 문단으로 나누고 긴 약어/수치 밀집을 완화.
3. Two-source bias 수식을 `equation` 한 줄에서 `align` 여러 줄로 분리.

## 판단

현재 원고는 12쪽 full manuscript draft로서 분량과 조판 안정성이 모두 개선됐다.

다음 단계는 더 많은 본문 추가보다, 저널/제출용 placeholder를 정리하는 쪽이 맞다.
