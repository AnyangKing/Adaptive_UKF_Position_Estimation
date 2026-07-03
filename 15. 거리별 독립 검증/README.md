# 15. 거리별 독립 검증

## 목적

13번에서 train/validation으로 고정한 10 ms SRP constant correction이 특정 200 m 궤적에만
유효한지 확인한다. 결과를 보고 bias, Q, R, 초기 공분산을 변경하지 않는다.

## 조건

- 거리: 100, 200, 400, 600 m
- 거리당 서로 다른 방위·수심의 궤적 2개
- 궤적당 12 ping, ping별 독립 noise seed
- SNR 20 dB, surface reflection -0.90, bottom reflection +0.60
- 비교: raw SRP와 고정 correction
- 고정 correction: azimuth +0.000265607 rad, elevation +0.016068076 rad를 측정에서 뺌

총 8개 짧은 궤적은 정식 Monte Carlo가 아니라 일반화 실패를 빠르게 찾는 validation이다.
초기 3 ping 이후 RMSE, 표준편차, 50 m 초과 발산률을 기록한다.

## 실행

```powershell
python test_validation.py
python run_distance_validation.py
```

## 최초 결과 (2026-07-03)

거리당 2개 궤적의 초기 3 ping 이후 평균 RMSE:

| 거리 | Raw SRP | 고정 correction | 변화 |
|---:|---:|---:|---:|
| 100 m | **2.058 m** | 3.177 m | -54.3% 악화 |
| 200 m | 10.605 m | **8.079 m** | 23.8% 개선 |
| 400 m | 21.607 m | **21.251 m** | 1.6% 개선 |
| 600 m | 17.959 m | **10.173 m** | 43.4% 개선 |

모든 8개 궤적에서 50 m 초과 발산은 없었다. 하지만 표본이 두 개뿐이어서 거리별
순서가 단조롭지 않고 400 m 편차도 크다.

고정 +0.921° 고도각 correction은 중·장거리에는 대체로 유리했지만 100 m에는 과보정이
됐다. SRP bias가 거리뿐 아니라 소스 수심, 표면반사 지연, SNR에 의존하므로 단일 상수는
전체 영역에 일반화되지 않는다.

이 8개 궤적은 이제 모델 개발에 사용된 것으로 간주하며 이후 최종 test로 재사용하지
않는다. 다음 거리의존 보정 모델은 별도 calibration/validation에서 선택하고 새로운
seed와 방위·수심을 가진 test에서 평가해야 한다.
