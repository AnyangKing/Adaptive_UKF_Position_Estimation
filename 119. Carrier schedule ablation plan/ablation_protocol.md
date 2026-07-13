# Carrier schedule ablation protocol

## 기본 원칙

1. 현재 논문 본체의 검증된 schedule은 바꾸지 않는다.
2. ablation은 후속 보강 실험이며, 결과가 나오기 전까지 원고 claim을 확장하지 않는다.
3. schedule 선택은 development와 validation을 분리한다.
4. static/quasi-static을 우선하고, moving은 별도 future-work 축으로 둔다.

## Stage 0. Carrier sensitivity pre-screen

목적: 무작정 schedule을 늘리지 않고, 58번처럼 carrier-bias curve를 먼저 본다.

조건:

- 거리: 400, 600 m 우선.
- 기하: 거리당 6~12.
- carrier grid: 28–36 kHz 또는 30–34 kHz 내부 세분화.

지표:

- fixed 32 kHz bias.
- carrier-average bias.
- carrier curve oscillation std.
- predicted phase period vs observed curve.

판정:

- carrier curve가 거의 평평한 geometry는 schedule ablation의 성능 gain을 기대하기 어렵다.
- carrier sensitivity가 큰 geometry에서만 schedule 차이가 의미 있게 보일 가능성이 높다.

## Stage 1. Static 600 m schedule ablation

목적: static 본체 claim을 보강할 schedule design rule을 찾는다.

공통 조건:

- 거리: 600 m.
- 기하: 최소 20, 권장 40.
- ping: 20 ping 기본, 후반 10 ping settled metric 유지.
- baseline: fixed 32 kHz.
- 기존 채택 schedule: linear20_30_34.

비교군:

- fixed32.
- linear20_30_34.
- extremes20_30_34.
- random20_30_34_seeded.
- four_carrier_cycle.
- narrow_linear20_31_33.
- wide_linear20_28_36.
- fixed3_hop1_static.

주요 지표:

- settled RMSE gain.
- median gain.
- improved fraction.
- P90/tail.
- DOA residual lag-1 reduction.
- lag-1 reduction vs RMSE gain correlation.

## Stage 2. Very-slow-drift check

Stage 1에서 살아남은 schedule만 0.005 m/s very-slow-drift에서 확인한다.

조건:

- 거리: 600 m.
- 속도: 0.005 m/s.
- 방향: radial, tangential 분리.
- 기하: 방향당 12 이상.

판정:

- static에서 좋고 0.005 m/s에서도 tail이 악화되지 않는 schedule만 quasi-static 후보.
- 0.010 m/s 이상은 탐색 조건이지 연속 boundary claim이 아니다.

## Stage 3. Moving schedule exploration

moving은 본 논문 본체를 바꾸기 위한 단계가 아니다. 63~67번의 교훈상 moving schedule은 tail predictor
검증이 먼저다.

사전 조건:

- runtime risk indicator가 실제 tail degradation을 예측하는지 GT-label 진단 통과.
- 예: recent DOA innovation variance, NIS tail, vertical velocity component, fixed/hop residual disagreement.

이 조건을 통과하기 전에는 moving RMSE improvement claim으로 가지 않는다.

## 통계 규칙

- schedule 수가 많으므로 p-value만으로 고르지 않는다.
- primary ranking: mean gain + median gain + tail safety + lag-1 reduction.
- 최종 채택은 독립 seed validation에서만 한다.
- development에서 고른 schedule은 반드시 validation에서 다시 잠근다.

## 산출물 형태

ablation을 실행한다면 결과 JSON에는 최소한 아래 항목을 둔다.

```json
{
  "schedule_name": "...",
  "carriers_hz": [...],
  "hop_fraction": 0.0,
  "fixed_mean_rmse_m": 0.0,
  "schedule_mean_rmse_m": 0.0,
  "mean_gain_m": 0.0,
  "median_gain_m": 0.0,
  "p90_gain_m": 0.0,
  "lag1_fixed": 0.0,
  "lag1_schedule": 0.0,
  "decision": "candidate|reject|validate"
}
```
