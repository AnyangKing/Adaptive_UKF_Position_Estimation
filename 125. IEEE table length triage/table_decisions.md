# Table decisions

## `tab:priorart`

결정: 본문 유지.

이유:

- 이 논문은 novelty framing이 매우 중요하다.
- frequency hopping 자체가 새롭지 않기 때문에, 선행연구와의 차이를 표로 분명히 보여주는 것이 방어에
  유리하다.
- reviewer가 가장 먼저 공격할 수 있는 “이미 frequency-hopped USBL이 있는데?”라는 지점을 정면으로
  다룬다.

조치:

- 이번 단계에서는 구조를 바꾸지 않았다.
- 추후 PDF 빌드에서 폭 문제가 생기면 column heading만 더 줄인다.

## `tab:results`

결정: 본문 유지, 강하게 압축.

이유:

- positive/negative result를 한눈에 보여주는 핵심 표다.
- 단, 기존 13행은 IEEE 2단 원고에서 너무 무겁다.
- 세부 speed별 행을 모두 펼치는 대신, 핵심 boundary 판단을 한 행으로 묶는 편이 본문 흐름에 맞다.

적용:

- 13행에서 6행으로 압축.
- 6열에서 5열로 축소.
- static positive, moving negative, whitening positive, moving schedule failure, quasi-static
  boundary, long-range floor를 유지.

## `tab:limitations`

결정: 본문 유지, 편집용 항목 제거.

이유:

- Discussion 끝에서 limitation/future work를 표로 요약하는 것은 유용하다.
- 하지만 “final citation styling”은 과학적 limitation이라기보다 submission checklist에 가깝다.
- 5열 구조는 분량 대비 정보 밀도가 낮다.

적용:

- 5열에서 4열로 축소.
- submission-only citation styling 행 제거.
- scientific limitation과 follow-up 중심으로 정리.

## 보류한 더 큰 변경

이번에는 표를 supplement로 완전히 이동하지 않았다.

이유:

1. 아직 journal target이 확정되지 않았다.
2. supplement 정책이 journal마다 다르다.
3. 지금 단계에서는 PDF 빌드 결과를 먼저 보고, 정말 표가 페이지를 망가뜨리는지 확인하는 것이 안전하다.

