# 34. 물리증거 검증형 Adaptive UKF

## 목적

반사경로 likelihood로 상태를 직접 이동하지 않고, 기존 TOA/TDOA/DOA update가 물리 경로
evidence를 감소시킬 때만 R을 키워 update를 다시 수행하는 사후검증형 Adaptive UKF를 시험한다.

## 알고리즘

1. UKF prediction posterior에서 peak-경로 배정을 주변화한 log evidence 계산
2. 기존 GCC-SRP routing 및 NIS 기반 TOA/TDOA/DOA update 제안
3. 제안 posterior의 물리 evidence 재계산
4. evidence가 문턱보다 감소하면 prediction 상태로 되돌리고 전체 R을 확대해 재수행

Validation 후보는 evidence 감소 문턱 0/1/2와 R 배율 4/16이다. Validation/test 각각 거리당
4개 독립 10-ping 궤적을 사용했다.

## 결과 (2026-07-05)

Validation은 감소 문턱 0, R×4를 선택했다. 강건 점수는 baseline 5.173에서 4.860으로 개선됐고
재시도율은 거리별 22~64%였다.

독립 test:

| 거리 | Baseline 평균 RMSE | 검증형 평균 RMSE |
|---:|---:|---:|
| 100 m | 1.449 m | 1.516 m |
| 200 m | 3.460 m | 3.593 m |
| 400 m | 5.109 m | 5.471 m |
| 600 m | 12.809 m | 12.761 m |

강건 점수는 8.909→9.025로 악화했다. 600m의 0.4% 개선을 제외하면 모든 거리 평균이 나빠졌다.

## 판정

Ping별 물리 evidence 증감으로 TOA/TDOA/DOA update를 즉시 재판정하는 방법은 **기각**한다.
상태 공분산 변화까지 포함된 marginal evidence는 실제 위치오차 개선 여부와 일대일 대응하지 않으며,
validation의 작은 이득이 test에 일반화되지 않았다.

다음 후보는 ping 하나의 증감이 아니라 경로 일관성을 시간적으로 누적하고, 관측이 정상/오염
상태에 있을 확률을 잠재 Markov 상태로 유지하는 방식이다.
