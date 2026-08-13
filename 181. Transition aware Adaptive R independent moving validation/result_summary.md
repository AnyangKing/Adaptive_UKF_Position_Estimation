# 181 result summary

## 판정

180번 development pilot에서 나온 `hop_transition_softR`이 독립 moving seed에서도 검증 후보를 통과했다.

## 핵심 수치

총 48 paired moving cases:

| comparison | mean gain (m) | median gain (m) | CI95 (m) | p | improved fraction | tail worsened fraction |
|---|---:|---:|---:|---:|---:|---:|
| softR vs hop baseline | 6.072 | 0.360 | [3.073, 9.600] | 9.63e-06 | 0.604 | 0.042 |
| softR vs fixed baseline | 7.119 | 2.183 | [3.670, 11.224] | 1.28e-04 | 0.708 | 0.229 |

## 해석

- 기존 linear carrier hop은 moving target에서 항상 안전하지 않았다.
- 하지만 carrier transition과 observed reference TOA jump를 이용해 TOA covariance를 soft inflation하면, hop baseline의 tail을 크게 줄이고 평균 RMSE를 개선했다.
- fixed baseline 대비 평균 이득도 양수로 재현되었다.

## 주의해야 할 점

- fixed 대비 tail worsened fraction이 22.9%로 낮지 않다.
- 따라서 이 결과는 “모든 moving geometry에서 안전한 always-on policy”가 아니다.
- 논문에는 per-condition breakdown, divergence rate, tail case를 함께 제시해야 한다.

## 논문 claim 후보

가능:

- Carrier transition-aware observation covariance routing can recover moving-target performance that plain carrier hopping fails to improve.
- The method uses only runtime-observable quantities: carrier transition, reference TOA jump, GCC-SRP disagreement, and block NIS.

금지:

- 모든 이동 표적에서 RMSE가 개선된다.
- frequency hopping 자체만으로 moving target이 개선된다.
- 180 development pilot 결과를 독립검증과 섞어서 표본 수를 부풀린다.

## 다음 확인

- condition별 gain breakdown을 표/그림으로 확인해야 한다.
- fixed 대비 악화 tail의 조건을 183번에서 진단하는 것이 좋다.
