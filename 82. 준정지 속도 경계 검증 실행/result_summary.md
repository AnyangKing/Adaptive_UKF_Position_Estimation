# 82번 결과 요약: 준정지 속도 경계 검증

## 한 줄 결론

Frequency-agile pinging의 정지 표적 이득은 600 m에서 재확인되었고, 0.005 m/s의 매우 느린 drift까지는 연속적인 quasi-static claim을 방어할 수 있다. 그러나 0.010 m/s와 0.050 m/s에서 성능 이득이 깨졌으므로, “0.100 m/s까지 준정지 영역”이라고 단조 경계처럼 주장하면 안 된다.

## 실험 조건

- 거리: 600 m
- 관측: TOA + TDOA + DOA
- 필터: Conditional adaptive-R UKF
- baseline: fixed 32 kHz
- treatment: 30--34 kHz ping-to-ping frequency-agile schedule
- 속도: 0, 0.005, 0.010, 0.030, 0.050, 0.100 m/s
- 운동 방향: 0 m/s는 static, 나머지는 radial/tangential
- 반복: 132 paired trials

## 전체 결과

| metric | fixed | hop | 해석 |
|---|---:|---:|---|
| mean settled RMSE | 11.98 m | 10.49 m | +1.49 m gain |
| median settled RMSE | 11.00 m | 8.50 m | median도 개선 |
| P90 RMSE | 19.73 m | 17.50 m | tail도 평균적으로 감소 |
| divergence rate | 3.79% | 4.55% | hop tail 위험은 약간 존재 |
| elevation residual lag-1 | +0.220 | -0.100 | whitening 재확인 |

통계:

- RMSE gain Wilcoxon one-sided p = 8.00e-05
- lag-1 reduction p = 9.17e-08
- lag-1 reduction과 RMSE gain의 Spearman rho = 0.035, p = 0.687

즉 whitening 자체는 강하지만, whitening 크기가 trial별 위치 RMSE 이득을 직접 예측하지는 않는다. 이 점은 63~67번의 moving-target 결과와 일관된다.

## 속도별 결과

| speed (m/s) | fixed mean | hop mean | mean gain | improved fraction | p | decision |
|---:|---:|---:|---:|---:|---:|---|
| 0.000 | 11.95 | 8.62 | +3.32 | 0.667 | 0.0134 | validated |
| 0.005 | 11.14 | 9.72 | +1.42 | 0.667 | 0.0447 | validated |
| 0.010 | 12.13 | 12.35 | -0.22 | 0.583 | 0.2031 | not supported |
| 0.030 | 10.18 | 8.19 | +1.99 | 0.708 | 0.0022 | validated |
| 0.050 | 12.35 | 12.39 | -0.04 | 0.500 | 0.4498 | not supported |
| 0.100 | 14.12 | 10.75 | +3.38 | 0.833 | 0.0048 | validated |

## 해석

연속적인 quasi-static boundary는 0.005 m/s까지만 검증되었다. 이후 0.030 m/s와 0.100 m/s에서 다시 양성 결과가 나오지만, 중간 속도인 0.010 m/s와 0.050 m/s가 깨졌기 때문에 이를 속도 단독의 단조 경계로 볼 수 없다.

방향별로 보면 원인이 더 선명하다.

- 0.010 m/s: tangential은 validated, radial은 not supported
- 0.050 m/s: tangential은 validated, radial은 not supported
- 0.100 m/s: radial/tangential 모두 validated

따라서 이 현상은 “느리면 좋고 빠르면 나쁘다”가 아니라, carrier hopping이 만드는 whitening과 운동이 만드는 self-whitening/tail 위험이 특정 기하에서 결합하는 문제다.

## 논문 반영 문장

안전한 문장:

> Frequency-agile pinging retained a statistically significant benefit for static targets and for very slow drift up to 0.005 m/s in our 600 m protocol. At higher speeds, the benefit became non-monotonic and geometry-dependent, indicating that quasi-static extension requires motion- and geometry-aware scheduling rather than an always-on carrier-agile policy.

피해야 할 문장:

> Frequency-agile pinging is validated for quasi-static targets up to 0.100 m/s.

0.100 m/s 자체는 양성이지만 중간 속도 실패가 있으므로 이렇게 쓰면 reviewer가 바로 물고 들어올 수 있다.

## 다음 연구 후보

1. `radial tail guard`: radial drift에서 hop tail이 커지는 조건을 사전 지표로 탐지할 수 있는지 검증
2. `geometry-dependent quasi-static classifier`: speed 하나가 아니라 radial/tangential 성분, DOA innovation, NIS tail을 묶어 hop 적용 여부를 결정
3. 논문 본체에서는 위 둘을 future work로 두고, 현재 결과는 “static 중심 + very slow drift 제한 + moving boundary”로 정리
