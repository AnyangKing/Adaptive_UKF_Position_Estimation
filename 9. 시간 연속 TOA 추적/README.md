# 9. 시간 연속 TOA 추적

## 목적

`8. 파형별 R 교정`에서 확인된 matched-filter peak switching을 줄인다. 매 ping 가장 강한
peak를 독립적으로 고르는 기준과, 이전 TOA에서 2 ms 이내인 peak를 추적하는 방법을
동일 원시 신호에서 비교한다.

2 ms는 음속 1500 m/s에서 경로길이 변화 3 m에 해당한다. 현재 1초 간격, 약 1 m/s
표적에는 여유가 있지만 ping 간격이나 최대속도가 바뀌면 함께 변경해야 하는 물리 제약이다.

## 알고리즘

- 상관 최댓값의 12% 이상인 다중 peak 검출
- 이전 TOA와 2 ms 이내 후보 중 시간적으로 가장 가까운 peak 선택
- 후보가 없으면 strongest peak로 fallback
- 3점 포물선 fractional-sample 보간

첫 ping에서 반사경로에 잠기면 이후에도 잘못된 경로를 유지할 위험이 있다. 따라서 TOA
RMSE와 위치 RMSE, fallback 비율을 모두 기록하며 성능이 나쁘면 채택하지 않는다.

## 실행

```powershell
python test_tracking.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

| 방법 | TOA 거리 RMSE | 5시점 이후 위치 RMSE | 마지막 오차 |
|---|---:|---:|---:|
| Strongest peak | 1.8940 m | **13.384 m** | **10.494 m** |
| Tracked peak | **0.0236 m** | 14.675 m | 12.811 m |

tracking은 절대거리 추정을 약 80배 개선했고 fallback은 0%였지만 위치 RMSE는 9.65%
악화됐다. 오차 분해 결과:

| 방법 | 방사방향 RMSE | 횡방향 RMSE |
|---|---:|---:|
| Strongest peak | 1.638 m | **13.284 m** |
| Tracked peak | **0.994 m** | 14.642 m |

TOA tracking은 의도대로 방사방향 오차를 줄였다. 전체 위치가 악화된 이유는 약 200 m에서
DOA/TDOA의 횡방향 오차가 지배적이고, 부정확한 strongest TOA가 우연히 일부 각도오차를
상쇄했기 때문이다. 따라서 tracked TOA 알고리즘은 유효한 구성요소로 보존하되, 현재
UKF에 단독 채택하지 않는다. 다음 단계에서 GCC 대신 꼬리오차가 작은 SRP-PHAT DOA를
실제 관측으로 사용해 횡방향 오차를 먼저 줄인다.
