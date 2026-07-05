# 25. 송신 대역폭 최적화

## 목적

600 m 정상상태 방향오차를 줄이기 위해 5 ms gated SRP는 유지하고 송신 LFM bandwidth만
8/12/20/30 kHz로 변경한다. 중심주파수 32 kHz, pulse 길이 10 ms, 표본화율 192 kHz와
수신 SNR 정의는 고정한다.

## 분리

- validation seed: 251000/253000 계열, 거리당 5 ping
- test seed: 252000/254000 계열, 다른 방위·수심, 거리당 10 ping
- 선택점수: overall DOA RMSE + 0.25×worst-distance DOA RMSE
- test 비교: 기존 12 kHz 대 선택 bandwidth

현재 채널은 흡수를 중심주파수에서만 계산하고 트랜스듀서의 실제 주파수 응답을 모델링하지
않는다. 넓은 bandwidth 결과가 좋아도 하드웨어 가능성과 주파수별 흡수/잡음 모델을 추가로
검증해야 한다. test 결과로 bandwidth를 다시 선택하지 않는다.

## 실행

```powershell
python test_bandwidth.py
python run_validation_test.py
```

## 최초 결과 (2026-07-03)

validation 강건 DOA 점수:

| Bandwidth | 전체 RMSE | 최악 거리 | 강건 점수 |
|---:|---:|---:|---:|
| 8 kHz | **1.137°** | 1.365° | **1.478** |
| 12 kHz | 1.231° | 1.467° | 1.598 |
| 20 kHz | 1.165° | **1.276°** | 1.484 |
| 30 kHz | 1.456° | 1.788° | 1.903 |

validation은 8 kHz를 선택했지만 독립 test 위치 RMSE는 다음과 같았다.

| 거리 | 12 kHz | 선택 8 kHz |
|---:|---:|---:|
| 100 m | 1.277 m | **1.244 m** |
| 200 m | 3.903 m | **3.088 m** |
| 400 m | **6.479 m** | 8.071 m |
| 600 m | **13.612 m** | 14.167 m |

거리 평균은 12 kHz 6.318 m, 8 kHz 6.642 m로 선택안이 5.1% 악화됐다. validation
DOA의 작은 차이가 동적 UKF 위치성능으로 일반화되지 않았고, 넓은 bandwidth도 일관된
이득이 없었다.

따라서 기존 12 kHz를 유지한다. validation 표본이 거리당 5 ping으로 작고 현재 채널이
주파수별 흡수와 트랜스듀서 응답을 생략하므로 논문용 파형 최적화 결론으로 사용하지 않는다.
다음 단계는 파형 변경보다 SRP spatial spectrum의 1·2위 peak margin을 관측 quality로
추출해 방향 모호성을 직접 검출하는 것이다.
