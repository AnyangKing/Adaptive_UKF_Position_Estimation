# 65. Anchor-hop schedule 이동표적 안전화

## 목적

64번에서 단순 whitening-aware adaptive-R 안전화는 기각됐다. 하지만 frequency hop이 DOA 고도각 오차의 lag-1 자기상관을 낮추는 백색화 효과는 다시 재현됐다.

이번 65번의 목적은 fixed 32 kHz를 동역학 anchor로 유지하고, hop을 간헐적 probe로 넣는 송신 스케줄이 이동 표적에서 더 안전한지 1차 pilot으로 검증하는 것이다.

## 핵심 질문

항상 hop을 쓰지 않고 fixed와 hop을 섞으면 다음을 동시에 만족할 수 있는가?

- fixed-only보다 RMSE가 낮아지는가?
- always-hop의 vertical/tangential 악화를 줄이는가?
- hop의 lag-1 자기상관 감소 효과를 일부 유지하는가?

## 실험 설정

- 거리: 600 m
- 조건: `radial_0.05`, `radial_1.0`, `tangential_1.0`, `tang_1.0_vz`
- 기하 수: 조건당 4개, 총 16개
- step: 16
- 정착 평가: 8 step 이후
- 필터/R 정책: 64번의 단순 R 팽창을 쓰지 않고 동일 wrapper 기본값 유지
- 변화시킨 것: carrier schedule만

64번 전체 규모보다 작게 잡았다. 이유는 schedule별로 원시 신호를 새로 생성해야 해서 계산량이 크기 때문이다. 따라서 65번은 확정 검증이 아니라 go/no-go pilot이다.

## 비교한 schedule

| 정책 | hop 비율 | 설명 |
|---|---:|---|
| fixed | 0.000 | 모든 ping 32 kHz |
| hop_always | 1.000 | 모든 ping 30~34 kHz hop bank |
| alternating_fh | 0.500 | fixed, hop 반복. fixed로 시작 |
| fixed3_hop1 | 0.250 | fixed 3회 후 hop 1회 |
| fixed4_hop1 | 0.188 | fixed 4회 후 hop 1회 |

## 실행

```powershell
python -m py_compile run_anchor_hop_schedule.py whitening_adaptive.py test_diagnostic.py
python test_diagnostic.py
python run_anchor_hop_schedule.py
```

결과 파일:

- `results/anchor_hop_schedule.json`

## 전체 결과

| 정책 | 평균 RMSE m | 중앙값 RMSE m | P90 평균 m | fixed 대비 평균 이득 m | 95% CI | p | 개선 비율 | lag-1 평균 |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| fixed | 10.968 | 11.705 | 12.722 | 0.000 | [0.000, 0.000] | 1.000 | 0.000 | +0.388 |
| hop_always | 10.158 | 9.364 | 11.651 | +0.809 | [-0.745, +2.614] | 0.217 | 0.688 | -0.145 |
| alternating_fh | 9.377 | 8.465 | 10.771 | +1.591 | [+0.467, +3.030] | 0.0078 | 0.750 | -0.151 |
| fixed3_hop1 | 9.913 | 9.143 | 11.891 | +1.055 | [+0.317, +2.032] | 0.0055 | 0.813 | +0.127 |
| fixed4_hop1 | 10.142 | 9.904 | 11.781 | +0.826 | [+0.010, +1.800] | 0.096 | 0.625 | +0.158 |

pilot 기준 최선은 `alternating_fh`다.

- 평균 RMSE: 10.968 → 9.377 m
- 평균 이득: +1.591 m
- bootstrap CI: [+0.467, +3.030] m
- Wilcoxon p: 0.0078
- P90 평균도 12.722 → 10.771 m로 낮아짐
- lag-1 자기상관도 +0.388 → -0.151로 낮아짐

`fixed3_hop1`도 중요하다.

- 평균 이득 +1.055 m
- p = 0.0055
- 개선 비율 81.3%
- hop 비율은 25%라 always-hop보다 안전한 sparse 후보가 될 수 있다.

## 조건별 관찰

### radial_0.05

- `alternating_fh`: +3.08 m 평균 이득, 4/4 개선
- `fixed3_hop1`: +2.16 m 평균 이득
- `fixed4_hop1`: +1.79 m 평균 이득

저속 radial에서는 anchor-hop 계열이 명확히 유리했다.

### radial_1.0

- always-hop: +0.68 m, 4/4 개선
- alternating: +0.21 m
- fixed3_hop1: +0.47 m, 4/4 개선
- fixed4_hop1: -0.55 m

빠른 radial에서는 hop 비율이 너무 낮으면 이득이 줄어든다.

### tangential_1.0

- always-hop: +2.39 m
- alternating: +3.01 m
- fixed3_hop1: +1.16 m
- fixed4_hop1: +1.56 m

이번 seed에서는 tangential 조건에서도 hop이 좋았다. 다만 64번에서는 tangential outlier가 컸으므로 이 결과는 반드시 확대검증해야 한다.

### tangential_1.0 + vertical

가장 중요한 조건이다.

- always-hop: -1.00 m 평균 악화, 개선 비율 25%
- alternating: +0.07 m, 거의 중립
- fixed3_hop1: +0.43 m
- fixed4_hop1: +0.51 m

즉, vertical 조건에서 always-hop이 다시 악화됐고, sparse anchor-hop이 그 악화를 완화했다. 이게 65번의 가장 중요한 수확이다.

## 판정

pilot 채택.

65번은 대규모 확정 검증은 아니지만, 64번에서 막힌 “R 팽창 안전화”보다 더 나은 방향을 보여준다. 특히 다음 결론이 중요하다.

1. frequency hop을 완전히 끄지 않아도 된다.
2. always-hop으로 밀어붙이면 vertical 조건에서 악화될 수 있다.
3. fixed carrier를 anchor로 유지하고 hop을 schedule로 섞으면 tail 악화를 줄이면서 백색화 이점을 일부 유지할 수 있다.

## 논문 novelty 관점

이 결과는 novelty 방향을 다시 살린다.

단순한 주장은 약하다.

> 주파수를 바꾸면 위치추정이 좋아진다.

더 강한 주장은 다음이다.

> coherent multipath DOA bias의 시간상관을 송신 carrier schedule로 제어하고, UKF가 안정적으로 흡수할 수 있는 anchor-hop 관측 설계를 만든다.

이건 단순히 알려진 기술을 조합하는 것보다 더 논문화 가능한 축이다. 핵심은 “frequency agility + Kalman fusion” 자체가 아니라 “bias whitening과 dynamic anchor 사이의 schedule design”이다.

## 한계

- 조건당 4기하, 총 16개인 pilot이다.
- 64번에서 본 tangential outlier가 seed에 따라 달라질 수 있으므로 확정하면 안 된다.
- results JSON은 `.gitignore` 때문에 커밋하지 않고, 핵심 수치는 README에 남겼다.

## 다음 단계

66번은 확대검증이 필요하다.

추천:

`66. Anchor-hop schedule 대규모 독립검증`

설정:

- 조건당 12~16기하 이상
- 63/64번과 독립 seed
- 정책은 너무 늘리지 말고 `fixed`, `hop_always`, `alternating_fh`, `fixed3_hop1`, `fixed4_hop1`만 유지
- 주요 판정:
  - `alternating_fh`가 fixed보다 유의하게 좋은가?
  - `fixed3_hop1` 또는 `fixed4_hop1`이 vertical 조건에서 always-hop보다 안전한가?
  - lag-1 감소와 RMSE 이득이 정책 수준/궤적 수준에서 연결되는가?

66번에서 통과하면 novelty 논문의 방법 축은 `frequency-agile whitening + anchor-hop schedule UKF`로 잡을 수 있다.
