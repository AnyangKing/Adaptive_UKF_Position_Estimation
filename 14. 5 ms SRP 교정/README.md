# 14. 5 ms SRP 교정

## 목적

13번의 누출 없는 SRP bias 교정 절차를 5 ms chirp에 독립적으로 반복한다. 10 ms 계수를
재사용하지 않고 같은 train/validation/test seed 분리와 후보 모델을 사용한다.

- train: 30개, seed 131001
- validation: 15개, seed 132001
- test: 약 200 m 30 ping, seed 93001부터
- 후보: constant, observable-feature ridge
- 선택 기준: validation 3D DOA RMSE

10 ms 현재 최선은 수렴 후 위치 RMSE 5.919 m이다. 5 ms 결과는 같은 test 궤적에서
직접 비교하되, test 결과로 보정 계수를 다시 조정하지 않는다.

## 실행

```powershell
python test_bias_model.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

validation DOA RMSE:

| 후보 | RMSE |
|---|---:|
| Raw | 1.622° |
| Constant | 1.584° |
| Ridge | **1.509°** |

validation에 따라 ridge가 선택됐다. 그러나 독립 test UKF 결과는 다음과 같다.

| 관측 | 초기오차 | 5시점 이후 RMSE | 최대오차 | 마지막 오차 |
|---|---:|---:|---:|---:|
| Raw 5 ms SRP | 10.526 m | **14.444 m** | **24.922 m** | **20.755 m** |
| Corrected 5 ms SRP | **4.040 m** | 17.881 m | 40.149 m | 29.113 m |

ridge 보정은 초기 획득을 크게 개선했지만 동적 추적 RMSE를 23.79% 악화시켰다.
정적이고 독립적인 validation 장면의 DOA RMSE 개선이 시간 궤적의 편향과 관측 상관에
일반화되지 않았다. test 결과를 보고 ridge 계수를 다시 맞추지 않으며 5 ms 보정안은
채택하지 않는다.

현재 최선은 13번의 10 ms + constant SRP correction이며 수렴 후 RMSE 5.919 m다.
5 ms는 초기화용 pulse 후보로만 남기고 정상 추적 파형으로 사용하지 않는다.
