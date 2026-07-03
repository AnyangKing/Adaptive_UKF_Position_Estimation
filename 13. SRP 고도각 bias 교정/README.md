# 13. SRP 고도각 bias 교정

## 목적

12번에서 확인된 지속적인 SRP 고도각 편향을 test 정보 없이 교정한다.

## 데이터 분리

- train: seed 131001, 독립 장면 30개
- validation: seed 132001, 독립 장면 15개
- test 궤적: seed 93001부터 30 ping
- train/validation 거리 80~650 m, 수심·SNR·반사계수·Doppler 무작위

test 궤적은 보정 모델 종류나 계수 선택에 사용하지 않는다.

## 후보 모델

- constant: train signed 방위각·고도각 residual 평균
- ridge: observable feature `[1, log(TOA range/100), measured elevation, elevation²]`

validation 3D DOA RMSE가 작은 후보 하나를 고정한 뒤 test UKF에 적용한다. 정답 수심이나
위치는 feature로 사용하지 않는다.

30/15 장면은 탐색용 소표본이며 최종 논문 교정에는 별도 대규모 calibration과 신뢰구간이
필요하다. 환경이 달라지면 보정식이 전이되지 않을 위험도 명시한다.

## 실행

```powershell
python test_bias_model.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

validation DOA RMSE:

| 후보 | RMSE |
|---|---:|
| Raw | 1.635° |
| Constant | **1.593°** |
| Ridge | 1.625° |

validation 기준으로 constant 모델이 선택됐다. train에서 추정한 signed residual은
방위각 +0.0152°, 고도각 +0.9207°이며 측정각에서 이 값을 뺀다.

독립 test UKF 결과:

| 관측 | 초기오차 | 5시점 이후 RMSE | 최대오차 | 마지막 오차 |
|---|---:|---:|---:|---:|
| Raw SRP | 10.525 m | 8.284 m | 12.912 m | 12.027 m |
| Corrected SRP | **7.555 m** | **5.919 m** | **9.624 m** | **9.027 m** |

수렴 후 RMSE가 28.55% 개선되어 현재 약 200 m 독립-noise 조건의 최선 결과다. 복잡한
ridge보다 constant가 validation에서 선택된 것은 소표본에서 거리·측정고도 특징의
추가 자유도가 일반화되지 않았기 때문이다.

test 궤적에서 관찰된 약 +3° 고도각 편향보다 교정량이 작지만, calibration 분포 전체에
일반화되는 값만 사용했기 때문에 test에 맞춘 사후 보정은 하지 않는다. 다음 단계는
같은 분리 절차를 5 ms 파형에도 적용해 파형과 보정의 상호작용을 비교한다.
