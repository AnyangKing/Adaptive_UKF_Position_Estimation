# 12. 인과적 DOA 평활화

## 목적

SRP-PHAT의 ping별 방향 변동을 미래 관측 없이 줄인다. 방위각과 고도각을 직접 평균하면
각도 wrap 문제가 있으므로 3차원 단위벡터로 바꿔 causal EMA 후 다시 각도로 변환한다.

## 비교

- raw SRP
- EMA alpha=0.5: 이전 평활 방향 50%, 현재 방향 50%
- EMA alpha=0.8: 이전 평활 방향 80%, 현재 방향 20%

동일한 약 200 m 궤적, 독립 ping noise, TOA/TDOA, adaptive UKF를 사용한다. 미래 시점은
사용하지 않는다.

EMA 관측은 시간상관을 새로 만들며 UKF가 이미 운동모델로 평활화한다. 따라서 이중
평활화와 기동 지연으로 위치가 악화될 수 있고, 그 경우 채택하지 않는다.

## 실행

```powershell
python test_smoothing.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

| DOA | 위치 RMSE | 최대오차 | DOA RMSE |
|---|---:|---:|---:|
| Raw SRP | 8.284 m | 12.912 m | **3.063°** |
| EMA 0.5 | **8.238 m** | **12.754 m** | 3.086° |
| EMA 0.8 | 8.315 m | 12.969 m | 3.136° |

alpha 0.5의 위치 개선은 0.56%에 불과하고 DOA 자체는 악화됐다. 효과 크기가 작고 한
궤적뿐이므로 채택하지 않는다.

raw SRP signed 오차를 분해하면 방위각 평균 +0.191°/RMSE 0.492°, 고도각 평균
+3.012°/RMSE 3.024°였다. 고도각 오차 범위도 +2.603~+3.589°로 지속적인 양의
편향이다. 따라서 주원인은 ping별 jitter가 아니라 멀티패스 기반 고도각 bias이며,
다음 단계는 독립 calibration/validation split에서 SRP bias 보정식을 학습하되 test
궤적은 선택에 사용하지 않는 것이다.
