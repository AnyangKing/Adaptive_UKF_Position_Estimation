# 66. Anchor-hop schedule 중간규모 독립검증

## 목적

65번 pilot에서는 `alternating_fh`와 `fixed3_hop1`이 fixed-only보다 좋아 보였다. 하지만 65번은 조건당 4기하, 총 16개 궤적인 작은 pilot이었다.

66번의 목적은 같은 schedule 후보를 독립 seed, 조건당 8기하, 총 32개 궤적으로 다시 검증해 pilot 결과가 우연인지 확인하는 것이다.

## 실험 설정

- 거리: 600 m
- 조건: `radial_0.05`, `radial_1.0`, `tangential_1.0`, `tang_1.0_vz`
- 기하 수: 조건당 8개, 총 32개
- step: 16
- 정착 평가: 8 step 이후
- seed: 65번과 독립
- 정책:
  - `fixed`
  - `hop_always`
  - `alternating_fh`
  - `fixed3_hop1`
  - `fixed4_hop1`

## 실행

```powershell
python -m py_compile run_anchor_hop_schedule.py whitening_adaptive.py test_diagnostic.py
python test_diagnostic.py
python run_anchor_hop_schedule.py
```

결과 파일:

- `results/anchor_hop_midscale.json`

## 전체 결과

| 정책 | 평균 RMSE m | 중앙값 RMSE m | P90 평균 m | fixed 대비 평균 이득 m | 95% CI | p | 개선 비율 | 발산율 | lag-1 평균 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| fixed | 11.726 | 9.786 | 15.026 | 0.000 | [0.000, 0.000] | 1.000 | 0.000 | 0.000 | +0.257 |
| hop_always | 13.416 | 8.459 | 17.269 | -1.690 | [-4.814, +0.742] | 0.489 | 0.563 | 0.031 | -0.201 |
| alternating_fh | 12.426 | 9.089 | 15.987 | -0.699 | [-2.313, +0.562] | 0.598 | 0.500 | 0.031 | -0.198 |
| fixed3_hop1 | 11.525 | 9.154 | 14.495 | +0.201 | [-1.012, +1.612] | 0.674 | 0.438 | 0.000 | +0.044 |
| fixed4_hop1 | 12.048 | 9.355 | 15.241 | -0.322 | [-1.069, +0.384] | 0.784 | 0.469 | 0.000 | +0.002 |

## 판정

65번 pilot의 강한 `alternating_fh` 이득은 재현되지 않았다.

- 65번: `alternating_fh` +1.59 m, p=0.0078
- 66번: `alternating_fh` -0.70 m, p=0.598

따라서 `alternating_fh`를 보편 채택하면 안 된다.

다만 `fixed3_hop1`은 아직 완전히 버릴 결과는 아니다.

- 평균 RMSE 최선: `fixed3_hop1` 11.525 m
- fixed 대비 평균 이득: +0.201 m
- P90 평균: fixed 15.026 m → fixed3_hop1 14.495 m
- 발산율: 0%
- lag-1 평균: +0.257 → +0.044

즉, `fixed3_hop1`은 유의한 성능 개선은 아니지만, always-hop보다 안전하고 tail을 약간 낮추는 schedule 후보로 남았다.

## 조건별 관찰

### radial_0.05

65번에서는 anchor-hop이 크게 좋아 보였지만 66번에서는 반대로 악화했다.

- fixed: 12.64 m
- hop_always: 12.82 m
- alternating: 14.64 m
- fixed3_hop1: 14.46 m
- fixed4_hop1: 13.91 m

저속 radial에서 pilot 이득은 seed 의존성이 컸다.

### radial_1.0

hop_always와 fixed3_hop1은 평균 기준 좋아졌다.

- hop_always: +1.27 m
- fixed3_hop1: +1.00 m

하지만 개선 비율은 50%라 안정적이지 않다.

### tangential_1.0

always-hop은 크게 악화했다.

- hop_always: -6.94 m 평균 악화
- alternating: -0.10 m
- fixed3_hop1: -0.09 m
- fixed4_hop1: +0.83 m

즉, schedule을 sparse하게 만들면 always-hop의 큰 outlier 악화는 줄인다.

### tangential_1.0 + vertical

가장 중요한 vertical 조건에서는 fixed3_hop1만 평균 기준 좋았다.

- hop_always: -0.91 m
- alternating: -0.51 m
- fixed3_hop1: +1.70 m
- fixed4_hop1: -0.37 m

하지만 fixed3_hop1의 개선 비율은 25%이고 중앙값 이득은 음수다. 몇 개 큰 outlier 완화가 평균을 끌어올린 형태라 확정은 금물이다.

## 해석

66번은 schedule 방향을 완전히 죽이지는 않았지만, 65번처럼 “alternating이면 해결”이라는 단순한 결론을 막았다.

현재까지 더 정직한 결론은 다음이다.

1. always-hop은 백색화는 강하지만 tail/outlier 위험이 크다.
2. alternating은 백색화도 강하지만 독립 seed에서 tail 위험을 충분히 제어하지 못했다.
3. fixed3_hop1은 성능 개선은 약하지만, 발산 없이 lag-1을 낮추고 P90을 약간 낮추는 안전 후보로 남았다.
4. schedule은 고정 패턴 하나로 끝낼 문제가 아니라, motion/geometry-aware schedule이 필요할 가능성이 크다.

## 후처리 oracle 상한

66번 결과 JSON만 사용해 raw simulation 없이 oracle schedule 상한도 계산했다.

### trajectory별 oracle

각 궤적마다 5개 정책 중 사후적으로 가장 RMSE가 낮은 정책을 고르면 다음과 같다.

- fixed 평균: 11.726 m
- trajectory별 oracle 평균: 9.323 m
- 상한 이득: +2.403 m

always-hop을 제외하고 fixed/sparse schedule만 허용해도:

- oracle 평균: 9.803 m
- 상한 이득: +1.924 m

즉, “정책 선택 정보”가 충분하면 schedule로 먹을 수 있는 이득은 남아 있다.

### 조건별 평균 oracle

현실적으로 더 가까운 조건별 평균 최선 schedule은 다음이다.

| 조건 | 조건별 최선 | fixed 평균 m | 최선 평균 m | 이득 m |
|---|---|---:|---:|---:|
| radial_0.05 | fixed | 12.644 | 12.644 | 0.000 |
| radial_1.0 | hop_always | 6.987 | 5.719 | +1.268 |
| tangential_1.0 | fixed4_hop1 | 11.895 | 11.064 | +0.831 |
| tang_1.0_vz | fixed3_hop1 | 15.379 | 13.675 | +1.704 |

조건별 oracle 전체 평균:

- fixed 평균: 11.726 m
- 조건별 oracle 평균: 10.776 m
- 이득: +0.951 m

이 결과는 67번의 방향을 명확히 한다. 고정 schedule 하나를 찾기보다, motion class 또는 추정된 동역학에 따라 hop 비율을 다르게 주는 motion-aware schedule을 검증해야 한다.

## 논문 방향에 미치는 영향

novelty 방향은 유지되지만, 주장 강도를 낮춰야 한다.

강하게 주장하면 안 되는 것:

> alternating fixed-hop schedule이 이동 표적을 보편적으로 개선한다.

현재 주장 가능한 것:

> frequency hop은 coherent multipath DOA bias의 시간상관을 낮추지만, 이동 표적에서는 hop 비율과 motion geometry가 tail risk를 결정한다. 따라서 Kalman fusion과 결합된 frequency-agile 관측 설계는 fixed anchor와 sparse probe의 안전성 제약을 포함해야 한다.

즉, 연구축은 `anchor-hop schedule`에서 한 단계 더 나아가 `motion-aware anchor-hop schedule`로 가야 한다.

## 다음 단계

67번 후보:

`67. Motion-aware anchor-hop schedule 조건분기 검증`

핵심 질문:

- radial_1.0에서는 hop 비율을 높이고, tangential/vertical에서는 sparse fixed3/fixed4를 쓰면 전체 성능이 좋아지는가?
- 모션 타입을 oracle로 주면 상한이 있는가?
- oracle 상한이 있으면, 실제 UKF 추정 velocity/innovation으로 근사 가능한가?

추천 순서:

1. oracle motion-aware schedule:
   - radial 계열: hop_always 또는 fixed3_hop1
   - tangential: fixed4_hop1 또는 fixed3_hop1
   - vertical: fixed3_hop1
2. 같은 66번 rows를 후처리로 조합해 oracle schedule 상한을 먼저 계산
3. 66번 후처리 기준 조건별 oracle 상한은 +0.95m이므로, 67번에서는 이 상한에 접근 가능한 실제 분기 규칙을 설계
4. 상한이 약하면 schedule 축을 정지/준정지 논문으로 제한하고 이동표적 일반화는 보류
