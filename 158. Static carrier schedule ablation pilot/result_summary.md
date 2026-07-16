# Stage-0 schedule pre-screen result

## 범위

- source: 58번 carrier-bias curves.
- distance: 400/600 m.
- geometries: 12.
- carrier source grid: 30–34 kHz.
- endpoint: geometry별 `abs(fixed 32 kHz bias) - abs(schedule mean bias)`.
- UKF/RMSE 실행: 없음.

## 결과

| schedule | mean abs-bias reduction (deg) | improved | P90 gain (deg) | mean |lag-1| | Stage 0 |
|---|---:|---:|---:|---:|---|
| random20 seeded | 0.5166 | 83.3% | 0.9058 | 0.2149 | candidate |
| linear20 30–34 | 0.5166 | 83.3% | 0.9058 | 0.5281 | candidate |
| four-carrier cycle | 0.3604 | 75.0% | 0.7440 | 0.5294 | candidate |
| fixed3-hop1 | 0.1880 | 83.3% | 0.4705 | 0.2223 | candidate |
| narrow linear20 | 0.4081 | 83.3% | 0.8280 | 0.8398 | reject/defer |
| two-extreme alternating | 0.3477 | 75.0% | 0.5887 | 1.0000 | reject/defer |
| fixed32 | ~0 | 25.0%* | ~0 | 1.0000 | baseline |
| wide 28–36 | — | — | — | — | no extrapolation |

* fixed32의 25%는 부동소수점 1e-16 수준 차이이며 실제 개선이 아니다.

## 핵심 발견

seeded random과 canonical linear는 같은 20-carrier 집합이므로 geometry별 평균 편향 상쇄량은 동일했다.
그러나 순서를 randomize하면 bias sequence의 mean absolute lag-1 proxy가 0.5281에서 0.2149로 줄었다.
이는 **carrier set과 carrier order를 분리해서 검증할 가치**가 있음을 보여준다.

two-extreme alternating은 평균 편향을 줄였지만 완전한 양·음 교대 패턴 때문에 |lag-1|=1이었다.
“가장 멀리 떨어진 두 주파수”가 자동으로 whitening schedule이 되는 것은 아니다.

## 다음

Stage 1 full UKF는 계산량을 줄여 fixed32 + random20 + canonical linear + four-carrier만 우선 비교한다.
이 결과도 development seed일 뿐이며, 최종 선택은 별도 독립 seed validation에서만 한다.
