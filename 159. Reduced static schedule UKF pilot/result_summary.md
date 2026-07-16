# 159 결과 요약

## 결과

600 m 정지표적 신규 개발 seed 4기하에서 신호 합성부터 adaptive-R UKF까지 실행했다.

| schedule | mean settled RMSE (m) | median (m) | fixed 대비 mean gain (m) | 개선 기하 | mean P90 (m) | mean abs lag-1 |
|---|---:|---:|---:|---:|---:|---:|
| fixed32 | 9.321 | 9.060 | 0.000 | 0/4 | 9.435 | 0.752 |
| linear20_30_34 | 6.417 | 5.603 | +2.904 | 4/4 | 7.615 | 0.350 |
| random20 seeded | 6.813 | 6.571 | +2.509 | 3/4 | 7.926 | **0.167** |
| four-carrier cycle | **4.109** | **3.974** | **+5.212** | **4/4** | **4.820** | 0.492 |

필터 예외와 50 m 초과 발산은 전 조건에서 0이었다.

## 해석

- Stage 0의 편향 상쇄 후보가 실제 TOA/TDOA/DOA→UKF 경로에서도 fixed보다 좋아질 가능성을
  확인했다.
- random은 linear와 같은 carrier 집합에서 innovation lag-1을 더 낮췄지만 RMSE는 더 좋지 않았다.
  따라서 잔차 백색화 자체가 위치 정확도의 충분조건은 아니다.
- four-carrier cycle은 이 개발 표본에서 가장 낮은 RMSE와 tail을 보였다. 적은 carrier bank가
  full linear sweep보다 유리할 수 있다는 신규 후보지만, 표본이 4개이고 이 결과로 선택했으므로
  독립검증 전에는 최적 또는 채택이라고 부르지 않는다.

## 결정

`four_carrier_cycle`을 기존 canonical `linear20_30_34`와 함께 160번 신규 seed 20기하 검증으로
보낸다. `random20_30_34_seeded`는 mechanism 결과로 보존하되, 이 pilot에서 linear보다 RMSE가
낮지 않아 계산량을 쓰는 우선 검증군에서는 제외한다.
