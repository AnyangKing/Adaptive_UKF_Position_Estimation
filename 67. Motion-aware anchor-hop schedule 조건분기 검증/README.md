# 67. Motion-aware anchor-hop schedule 조건분기 검증

## 목적

66번 후처리에서는 조건별 평균 최선 schedule이 달랐다.

- `radial_0.05`: fixed
- `radial_1.0`: hop_always
- `tangential_1.0`: fixed4_hop1
- `tang_1.0_vz`: fixed3_hop1

67번은 이 조건별 oracle-like rule을 독립 seed에서 직접 검증했다. 아직 실제 구현 가능한 motion classifier가 아니라, condition label을 알고 있다고 가정한 상한 검증이다.

## 실험 설정

- 거리: 600 m
- 조건: 4개 이동 조건
- 기하 수: 조건당 8개, 총 32개
- step: 16
- 정착 평가: 8 step 이후
- seed: 66번과 독립

비교 정책:

- fixed
- hop_always
- fixed3_hop1
- fixed4_hop1
- condition_aware

condition_aware 규칙:

| 조건 | 사용 schedule |
|---|---|
| radial_0.05 | fixed |
| radial_1.0 | hop_always |
| tangential_1.0 | fixed4_hop1 |
| tang_1.0_vz | fixed3_hop1 |

## 전체 결과

| 정책 | 평균 RMSE m | 중앙값 RMSE m | P90 평균 m | fixed 대비 평균 이득 m | 95% CI | p | 개선 비율 | lag-1 평균 |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| fixed | 13.094 | 10.163 | 16.760 | 0.000 | [0.000, 0.000] | 1.000 | 0.000 | +0.484 |
| hop_always | 13.310 | 9.248 | 16.733 | -0.216 | [-2.187, +1.791] | 0.720 | 0.375 | -0.006 |
| fixed3_hop1 | 12.609 | 9.020 | 16.051 | +0.486 | [-0.472, +2.042] | 0.647 | 0.406 | +0.145 |
| fixed4_hop1 | 11.909 | 9.288 | 15.235 | +1.185 | [+0.042, +2.695] | 0.102 | 0.563 | +0.157 |
| condition_aware | 13.400 | 10.076 | 16.874 | -0.306 | [-0.654, +0.040] | 0.972 | 0.219 | +0.173 |

## 판정

기각.

66번 조건별 oracle rule은 독립 seed에서 재현되지 않았다.

- condition_aware 평균 RMSE: 13.400 m
- fixed 평균 RMSE: 13.094 m
- 평균 이득: -0.306 m
- p = 0.972
- 개선 비율: 21.9%

즉, condition label만으로 66번의 조건별 최선 schedule을 그대로 적용하는 방법은 신뢰할 수 없다.

## 중요한 부가 결과

이번 seed에서는 `fixed4_hop1`이 가장 좋았다.

- 평균 RMSE: 11.909 m
- fixed 대비 +1.185 m
- P90: 16.760 → 15.235 m
- p = 0.102

다만 p값이 유의하지 않고, 66번에서는 fixed4_hop1이 평균 -0.322 m로 약했다. 따라서 fixed4도 확정 채택은 아니다.

## 66+67 합산 경향

66번과 67번의 공통 정책을 합치면 n=64다.

| 정책 | 평균 이득 m | 중앙값 이득 m | p | 개선 비율 | 발산율 |
|---|---:|---:|---:|---:|---:|
| hop_always | -0.953 | -0.144 | 0.661 | 0.469 | 0.016 |
| fixed3_hop1 | +0.343 | -0.135 | 0.671 | 0.422 | 0.000 |
| fixed4_hop1 | +0.432 | +0.045 | 0.357 | 0.516 | 0.000 |

합산해도 fixed3/fixed4는 유의하지 않다. 그러나 always-hop보다 훨씬 안전하고 발산이 없다.

## 해석

67번은 schedule 연구축을 한 번 더 좁혔다.

1. always-hop은 여전히 보편 해법이 아니다.
2. 66번 조건별 oracle rule은 seed 안정성이 없다.
3. fixed3/fixed4 sparse hop은 성능 개선이 크지는 않지만 tail과 발산 안전성 면에서 살아남는다.
4. 이동표적 일반 schedule로 SCI novelty를 주장하기에는 아직 부족하다.

현재 가장 정직한 논문 방향은 다음과 같다.

- 강한 축: 정지/준정지 600 m frequency-agile bias whitening
- 보조 축: 이동 표적에서는 hop이 lag-1을 낮추지만, motion geometry에 따라 tail risk가 생기며 sparse anchor-hop이 안전 후보
- 아직 미완성 축: 이동 표적 general-purpose adaptive schedule

## 다음 단계

68번에서 둘 중 하나를 선택해야 한다.

### 선택 A: 이동표적 schedule을 더 파기

더 이상 condition label rule이 아니라, 실제 관측 가능한 risk 지표를 써야 한다.

후보:

- 최근 3~4 ping DOA innovation variance
- hop/fixed 간 residual disagreement
- 추정 속도의 vertical component
- short-window NIS tail

목표는 schedule을 “좋은 조건에서 더 공격적으로 hop, 위험 조건에서 fixed4처럼 sparse”로 바꾸는 것이다.

### 선택 B: 논문 축을 정지/준정지로 고정

현재까지 가장 강한 결과는 61번 정지표적 대규모 검증이다. 이동 표적 schedule은 “확장 가능성/한계 분석”으로 두고, novelty 논문 본체는 정지/준정지 표적의 frequency-agile multipath bias whitening으로 잡는 것이 더 안전하다.

현 시점의 권고는 B에 가깝다. 이동표적 schedule은 아직 연구로는 흥미롭지만, 논문 핵심 주장으로 세우기에는 재현성이 약하다.
