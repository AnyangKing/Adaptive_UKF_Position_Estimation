# 16. 거리 의존 SRP bias 교정

## 목적

15번에서 단일 상수 correction이 100 m를 과보정하고 장거리에서는 유리했던 현상을
새 데이터 분리로 검증한다. 15번 궤적과 seed는 사용하지 않는다.

## 분리

- train: 거리당 6개, seed 161001
- validation: 거리당 3개, seed 162001
- test: 거리당 신규 12-ping 궤적, seed 163000 계열
- 거리: 100, 200, 400, 600 m

## 후보와 선택

- raw: correction 없음
- constant: 전체 train residual 평균
- linear: `[1, log(measured TOA range/100)]` ridge
- piecewise: 거리별 train 평균을 측정 TOA range로 선형보간

validation 선택점수는 사전에 `overall RMSE + 0.25 × worst-distance RMSE`로 고정했다.
평균만 좋아지고 특정 거리를 크게 망치는 모델을 억제하기 위한 것이다. raw도 후보이므로
모든 correction이 나쁘면 보정하지 않는 선택이 가능하다.

표본은 여전히 탐색용 소규모이며 test 결과로 모델이나 계수를 다시 조정하지 않는다.

## 실행

```powershell
python test_distance_bias.py
python run_test.py
```

## 최초 결과 (2026-07-03)

validation 강건 점수(`overall + 0.25×worst-distance`):

| 후보 | 전체 DOA RMSE | 최악 거리 RMSE | 강건 점수 |
|---|---:|---:|---:|
| Raw | **3.139°** | 5.524° | **4.520** |
| Constant | 3.923° | 6.775° | 5.617 |
| Linear | 3.925° | 6.676° | 5.594 |
| Piecewise | 4.040° | **5.505°** | 5.416 |

사전 선택 규칙에 따라 raw, 즉 correction 없음이 선택됐다. 따라서 test의 raw와 corrected는
의도대로 동일하다.

신규 동적 test의 초기 3 ping 이후 RMSE:

| 거리 | 선택 모델 RMSE | 초기오차 |
|---:|---:|---:|
| 100 m | 0.953 m | 1.333 m |
| 200 m | 14.190 m | 7.811 m |
| 400 m | 33.536 m | 34.910 m |
| 600 m | 20.725 m | 21.991 m |

거리의존 correction 가설은 독립 validation에서 지지되지 않아 기각한다. 15번에서 보였던
상수 correction 개선은 특정 환경·궤적 효과였으며 전체 영역의 고정 보정으로 일반화할
수 없다.

100 m는 1 m 이하였지만 장거리에서는 초기 방향 오차가 거리와 곱해져 수십 m 위치오차가
되고 이후 필터도 회복하지 못했다. 다음 병목은 bias 회귀가 아니라 SRP peak의 환경별
모호성, 거리 비례 초기 공분산, 다중 ping 초기 획득이다.
