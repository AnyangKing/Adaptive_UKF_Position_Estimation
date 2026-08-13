# Full range sweep result summary

거리당 n=6 diagnostic sweep이다. 강한 성능 claim에는 추가 독립검증이 필요하다.

| distance | fixed mean | hop mean | softR mean | hop gain vs fixed | softR gain vs fixed | hop div | softR div | softR triggers |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 5.784 | 6.317 | 6.317 | -0.534 | -0.534 | 0.000 | 0.000 | 0 |
| 100 | 2.315 | 2.120 | 2.120 | 0.195 | 0.195 | 0.000 | 0.000 | 0 |
| 200 | 3.031 | 2.949 | 2.949 | 0.083 | 0.083 | 0.000 | 0.000 | 0 |
| 300 | 5.244 | 4.167 | 4.167 | 1.076 | 1.076 | 0.000 | 0.000 | 0 |
| 400 | 7.932 | 7.216 | 7.216 | 0.716 | 0.716 | 0.000 | 0.000 | 0 |
| 500 | 7.846 | 9.544 | 9.544 | -1.698 | -1.698 | 0.000 | 0.000 | 1 |
| 600 | 15.935 | 8.547 | 8.547 | 7.387 | 7.387 | 0.000 | 0.000 | 0 |
| 700 | 14.523 | 9.115 | 9.115 | 5.408 | 5.408 | 0.000 | 0.000 | 0 |
| 800 | 14.848 | 10.051 | 10.051 | 4.797 | 4.797 | 0.000 | 0.000 | 0 |
| 900 | 14.336 | 7.956 | 7.950 | 6.380 | 6.386 | 0.000 | 0.000 | 1 |
| 1000 | 22.496 | 13.741 | 13.741 | 8.755 | 8.755 | 0.000 | 0.000 | 0 |

## 해석 경계

- 0 m는 horizontal distance 0 m 특수 near-vertical case다.
- 거리당 n=6이므로 통계적 trend map으로만 사용한다.
- 평균 이득과 divergence/tail을 반드시 함께 본다.

## 핵심 관찰

- 0 m near-vertical case에서는 hop이 fixed보다 나빴다. 이 조건은 장거리 horizontal USBL claim과 분리한다.
- 100--400 m에서는 hop 이득이 작거나 중간 수준이다.
- 500 m에서는 hop이 악화되었다. 거리별 transition 또는 multipath geometry의 비단조성이 있음을 뜻한다.
- 600--1000 m에서는 hop 이득이 크게 나타났다.
  - 600 m: +7.387 m
  - 700 m: +5.408 m
  - 800 m: +4.797 m
  - 900 m: +6.380 m
  - 1000 m: +8.755 m
- softR trigger는 전체 66 cases에서 2회뿐이어서, static range sweep에서는 hop baseline과 거의 동일하게 동작했다.

## 논문에 반영할 수 있는 안전한 문장

Carrier agility is not uniformly beneficial at all ranges. In this diagnostic sweep, its benefit becomes pronounced beyond approximately 600 m, where the long-range coherent-bias floor dominates, while near/medium ranges can show small or even negative gains.

## 금지 문장

- 모든 거리에서 carrier agility가 개선된다.
- 500 m 악화 또는 0 m 악화를 숨긴다.
- n=6 sweep을 최종 통계 검증처럼 제시한다.
