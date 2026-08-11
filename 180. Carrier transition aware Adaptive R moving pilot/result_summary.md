# 180 result summary

## 판정

`hop_transition_softR`은 moving development pilot에서 독립검증 후보로 승격할 만한 신호를 보였다.

단, 이 결과는 n=16 development pilot이다. 논문 성능 claim으로 사용할 수 없고, 181번 이상의 독립검증 전에는 “유망한 후보”로만 기록한다.

## 핵심 비교

| comparison | mean gain (m) | median gain (m) | CI95 (m) | p | improved fraction | tail worsened fraction |
|---|---:|---:|---:|---:|---:|---:|
| softR vs hop baseline | 5.072 | 1.825 | [2.398, 8.052] | 0.00118 | 0.750 | 0.000 |
| softR vs fixed baseline | 2.452 | 1.116 | [0.506, 4.582] | 0.00912 | 0.812 | 0.125 |

## 해석

- hard TOA isolation guard는 179번에서 실패했지만, soft TOA covariance inflation은 moving development set에서 이득 방향을 보였다.
- 이 후보는 carrier transition flag와 observed reference TOA jump만 사용한다.
- 기존 GCC-SRP disagreement와 block NIS routing은 유지한다.
- 즉 새 방향은 “carrier schedule 선택”이 아니라 “carrier transition이 관측 추출에 만든 위험을 adaptive-R에 반영”하는 쪽이다.

## 주의

- development pilot이므로 threshold를 더 만지면 이 seed는 개발 데이터로만 유지해야 한다.
- 181번 독립검증에서는 `range_jump_threshold_m=0.5`, `max_toa_scale=100`을 동결해야 한다.
- 181번에서 실패하면 이 방법도 future work 또는 실패 지도 항목으로 강등한다.

## 다음 제안

`181. Transition-aware Adaptive R independent moving validation`

- 63번과 같은 4개 moving condition
- 조건당 최소 12--16 geometries
- fixed baseline, hop baseline, hop_transition_softR paired 비교
- P90, divergence, per-condition breakdown 필수
- GT는 signal synthesis/final error/offline diagnosis에만 사용
