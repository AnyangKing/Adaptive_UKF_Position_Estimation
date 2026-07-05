# 22. 직접파 구간 SRP

## 목적

전체 수신 신호의 SRP에는 직접파와 표면·해저 반사가 모두 섞인다. matched-filter로 얻은
가장 이른 센서 도착시각 0.1 ms 전부터 1/2/5 ms만 잘라 SRP를 계산하고 full과 비교한다.

## 분리

- validation seed: 221000 계열
- test seed: 222000 계열, 다른 방위·수심
- 거리: 100/200/400/600 m, 각 10 ping
- 후보: full, 1 ms, 2 ms, 5 ms
- 선택: validation `overall DOA RMSE + 0.25×worst-distance RMSE`
- test UKF: 19번 5° 조건부 라우팅 고정

짧은 창은 후속 반사를 줄이지만 신호 에너지와 주파수 해상도를 잃는다. matched-filter가
반사 peak를 직접파로 오인하면 창 자체가 잘못 배치될 위험도 있다. test 결과로 창 길이를
다시 고르지 않는다.

## 실행

```powershell
python test_gated.py
python run_validation_test.py
```

## 최초 결과 (2026-07-03)

validation DOA:

| SRP 입력창 | 전체 RMSE | 최악 거리 RMSE | 강건 점수 |
|---|---:|---:|---:|
| Full | 2.227° | 3.939° | 3.212 |
| 1 ms | 37.049° | 38.283° | 46.620 |
| 2 ms | 36.532° | 37.884° | 46.003 |
| 5 ms | **1.040°** | **1.430°** | **1.397** |

validation은 5 ms를 선택했다. 1~2 ms는 표본과 주파수 해상도가 부족해 방향추정이
붕괴했고, 5 ms는 직접파 에너지를 충분히 유지하면서 후속 멀티패스를 줄였다.

독립 test UKF:

| 거리 | Full SRP RMSE | 5 ms gated SRP RMSE | 개선 |
|---:|---:|---:|---:|
| 100 m | 1.021 m | **0.672 m** | 34.1% |
| 200 m | 8.741 m | **4.663 m** | 46.7% |
| 400 m | 25.912 m | **6.236 m** | 75.9% |
| 600 m | 15.266 m | **4.319 m** | 71.7% |

모든 test 거리에서 개선됐고 50 m 초과 발산은 없었다. 현재 최선 구성은 10 ms 송신
chirp 중 matched-filter 도착 직전부터 5 ms를 잘라 계산한 SRP DOA + TOA/TDOA + 5°
조건부 신뢰도 라우팅 + 6-state UKF다.

아직 거리당 단일 10-ping 궤적이므로 최종 성능으로 확정하지 않는다. 다음 단계는 이
구성을 여러 방위·수심·SNR·반사계수에서 반복해 평균, 백분위수와 발산률을 확인한다.
