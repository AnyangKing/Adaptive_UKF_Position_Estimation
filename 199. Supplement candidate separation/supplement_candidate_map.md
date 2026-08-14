# Supplement candidate map

## 우선순위 A: 가장 먼저 보충자료로 보낼 수 있는 항목

### Detailed quasi-static table

후보:

- quasi-static speed sweep의 상세 수치표

이유:

- 본문에는 “static/near-static에서 이득, moving generalization에서 경계”라는 메시지가 중요하다.
- 상세 속도별 수치는 그림 또는 짧은 요약으로 대체 가능하다.

본문에 남길 최소 정보:

- 검증 조건 수
- 정지/0.005 m/s positive
- 더 빠른 이동에서 이득이 약해지거나 사라지는 경계

### Compact summary table

후보:

- positive/negative validation 전체 요약표

이유:

- 독자에게 유용하지만, 본문 모든 결과를 이미 각 절에서 설명한다면 중복될 수 있다.
- 보충자료 첫 장의 roadmap table로 더 잘 작동할 수 있다.

본문에 남길 최소 정보:

- 핵심 positive: static 600 m, moving transition-aware 0--1000 m
- 핵심 boundary: plain hopping moving tail risk, real-water not yet tested

## 우선순위 B: 쪽수 압박이 있으면 보충자료로 이동

### Empirical-CRLB efficiency table

이유:

- 성능이 물리 하한 대비 어느 정도인지 보여주는 좋은 방어 자료다.
- 하지만 논문의 주 결과는 CRLB 달성이 아니라 coherent bias decorrelation과 adaptive-R recovery다.

본문 대체 방식:

- Method/Discussion에 한두 문장으로 남기고 상세 표는 supplement.

### Baseline comparison details

이유:

- 공정성 방어에는 필요하지만, 표가 길면 본문 흐름을 끊는다.

본문 대체 방식:

- 핵심 비교군과 동일 조건 입력 원칙만 본문에 남긴다.
- 튜닝 범위/세부 seed/발산률은 supplement로 이동.

## 우선순위 C: 가능하면 본문 유지

### Moving full-range figure

이유:

- 현재 논문의 최신 방향을 가장 잘 보여준다.
- 0--1000 m 전체 성능 추세와 800 m failure-and-recovery를 한 번에 설명한다.

### Static validation figure

이유:

- frequency agility의 원래 positive result이므로 본문에서 빠지면 연구의 물리적 설득력이 약해진다.

### Two-ray mechanism figure

이유:

- novelty 방어의 뼈대다.
- 단순 알고리즘 성능표 논문처럼 보이지 않게 만든다.

## 아직 이동 금지

다음은 현 단계에서 보충자료로 보내면 안 된다.

- related-work positioning: 최초성/차별성 방어에 필수
- moving full-range main result: 최신 논문 방향의 중심
- limitation/future work: simulation-only 한계를 정직하게 닫는 방어 장치
