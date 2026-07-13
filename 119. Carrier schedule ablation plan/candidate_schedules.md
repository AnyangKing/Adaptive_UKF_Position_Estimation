# Candidate schedules

## Current canonical schedules

| 이름 | 정의 | 목적 |
|---|---|---|
| `fixed32` | 모든 ping 32 kHz | baseline |
| `linear20_30_34` | 20 ping `linspace(30, 34) kHz` | 현재 논문 본체의 동결 schedule |

## Static/quasi-static ablation candidates

| 이름 | 정의 | 가설 | 위험 |
|---|---|---|---|
| `narrow_linear20_31_33` | 31–33 kHz 20-step linear | hardware/SNR 변화가 작고 whitening 일부 유지 | phase rotation 부족 가능 |
| `wide_linear20_28_36` | 28–36 kHz 20-step linear | 더 큰 phase rotation으로 bias whitening 강화 | transducer response, bandwidth/SNR 차이 커질 수 있음 |
| `four_carrier_cycle` | 30, 31.33, 32.67, 34 kHz 반복 | 적은 carrier로 비슷한 whitening 가능성 | 특정 geometry에서 phase aliasing |
| `two_extreme_alternating` | 30, 34 kHz 반복 | 최대 phase separation | lag-1이 강한 alternating artifact로 바뀔 수 있음 |
| `random20_30_34_seeded` | 30–34 kHz에서 20개 seeded random permutation | deterministic sweep 순서 효과 제거 | seed 의존성 |
| `costas_like_interping` | 30–34 kHz discrete bank의 permutation | inter-ping decorrelation 강화 | Costas prior와 혼동 가능, 설명 주의 |
| `fixed3_hop1_static` | fixed 3 ping + hop 1 ping | dynamic anchor와 whitening 균형 | static에서는 always-hop보다 약할 수 있음 |
| `fixed4_hop1_static` | fixed 4 ping + hop 1 ping | 더 보수적인 sparse hop | whitening 부족 |

## Moving-only candidates

moving schedule은 본체 claim이 아니다. 아래는 future work 후보로만 둔다.

| 이름 | 정의 | 상태 |
|---|---|---|
| `fixed3_hop1` | 65~67에서 시도 | tail safety 후보지만 유의 재현 부족 |
| `fixed4_hop1` | 65~67에서 시도 | 발산/악화는 낮지만 성능 유의성 부족 |
| `risk_gated_sparse` | runtime risk indicator가 높으면 sparse/fixed로 후퇴 | 먼저 predictor 진단 필요 |

## 구현 주의

- carrier별 송신/수신 SNR 차이를 성능 gain으로 착각하면 안 된다.
- schedule은 결과를 본 뒤 수정하면 안 된다.
- static schedule 최적화 결과를 moving target에 그대로 확장하면 안 된다.
