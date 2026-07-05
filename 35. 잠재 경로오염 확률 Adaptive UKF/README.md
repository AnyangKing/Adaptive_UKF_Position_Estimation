# 35. 잠재 경로오염 확률 Adaptive UKF

## 목적

Ping별 물리 판정의 불안정을 줄이기 위해 peak-경로 상대지연 residual을 정상/오염 2상태의
잠재확률로 시간 누적하고, 오염확률에 따라 기존 센서간 TDOA·DOA R을 연속 확대한다.

## 방법

- 예측 위치에서 가능한 peak-경로 순열 중 최소 정규화 residual을 물리 score로 사용
- 정상→오염 0.05, 오염→정상 0.20의 Markov transition
- Logistic emission과 Bayesian recursion으로 매 ping 오염확률 갱신
- TOA R은 유지하고 TDOA·DOA R을 `1+p_bad(max_scale-1)`로 조절
- Validation score q50/q75 및 최대 배율 4/16 중 선택, 독립 test 고정 적용

## 결과 (2026-07-05)

Validation은 q75 문턱과 최대 R×16을 선택했다. 강건 점수는 8.586→8.419이었다.

독립 test:

| 거리 | Baseline 평균 RMSE | 잠재확률 평균 RMSE |
|---:|---:|---:|
| 100 m | 1.807 m | 1.809 m |
| 200 m | 2.696 m | 2.763 m |
| 400 m | 7.391 m | 7.404 m |
| 600 m | 13.348 m | 13.278 m |

강건 점수는 9.648→9.633(-0.15%)으로 사실상 동일하다. 선택 정책의 평균 오염확률도 거리별
약 0.9~1.7%에 머물러 대부분 baseline처럼 동작했다.

## 판정

시간 누적 잠재 오염확률 방식은 **기각**한다. 현재 물리 residual score는 실제 TOA/TDOA/DOA
오염을 충분히 분리하지 못해, 보수적 문턱에서는 거의 작동하지 않고 공격적 문턱은 validation에서도
이득이 작다. 다음 단계는 필터 정책을 더 복잡하게 만들기 전에 물리 feature와 실제 관측오차의
예측관계를 별도 진단해 정보가 존재하는지 확인해야 한다.
