# Next step: 125. IEEE table length triage

## 문제

현재 원고에는 full-width `table*`가 3개 있다.

1. Prior art table
2. Results summary table
3. Limitations/follow-up table

IEEE 2단 논문에서 `table*`는 매우 유용하지만, 너무 길면 그림보다 더 크게 페이지 흐름을 망가뜨린다.
특히 지금 원고는 7쪽 안팎의 compact paper를 목표로 하므로 표 분량을 조절해야 한다.

## 제안 기준

다음 기준으로 표를 분류한다.

| 표 | 기본 판단 | 이유 |
|---|---|---|
| Prior art table | 본문 유지, 짧게 압축 | novelty 방어의 핵심. |
| Results summary table | 본문 유지, 행 일부 축약 | positive/negative boundary를 한눈에 보여주는 핵심 증거. |
| Limitations table | 축약 또는 supplement 이동 후보 | Discussion 문단으로도 대체 가능하고 분량 압박이 크다. |

## 125번에서 할 일

- 각 `table*`의 행 수, column 수, caption 길이, first reference 위치를 점검한다.
- 본문 유지/축약/supplement 이동 후보를 결정한다.
- 가능하면 caption과 문구만 먼저 줄이고, claim 손실이 큰 구조 변경은 보류한다.

