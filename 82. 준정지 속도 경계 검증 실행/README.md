# 82. 준정지 속도 경계 검증 실행

## 목적

81번에서 사전등록한 `static/quasi-static` 표현의 안전선을 실제 실험으로 확인한다.

현재 논문의 강한 양성 결과는 정지 600 m 표적에서 고정 32 kHz 대비 30--34 kHz ping-to-ping frequency-agile 송신이 coherent multipath DOA 편향을 백색화해 RMSE를 낮춘다는 것이다. 반면 이동 표적에서는 백색화 기전은 보였지만 pooled RMSE 이득이 재현되지 않았다. 따라서 본 폴더는 정지와 이동 사이의 “준정지 속도 경계”를 계량한다.

## 고정 조건

- 거리: 600 m
- 관측: TOA + TDOA + DOA
- 필터: Conditional adaptive-R UKF
- baseline: fixed 32 kHz
- treatment: 30--34 kHz 20 ping 선형 도약
- 속도: 0, 0.005, 0.010, 0.030, 0.050, 0.100 m/s
- 운동 방향: 0 m/s는 static 1조건, 나머지는 radial/tangential 2조건
- 반복: 조건당 12개 독립 기하/seed

## 실행 파일

- `run_quasi_static_boundary.py`: 검증 실행, partial resume 지원
- `results/quasi_static_boundary.json`: 전체 결과와 summary
- `results/quasi_static_trials.csv`: trial 단위 결과
- `results/quasi_static_speed_boundary.svg`: 속도별 RMSE gain / lag-1 reduction 그림

## 판정 규칙

속도별로 다음을 만족하면 validated로 판정한다.

1. mean gain = fixed RMSE - hop RMSE > 0
2. median gain > 0
3. improved fraction >= 0.60
4. paired one-sided Wilcoxon p < 0.05

mean/median만 양수이면 positive trend, 아니면 not supported로 기록한다.

## 논문에서의 사용

- 0.005--0.010 m/s까지 validated이면 `static/quasi-static` 표현을 제한적으로 유지할 수 있다.
- 0 m/s만 validated이면 본체 주장은 `static long-range USBL`로 축소하고 quasi-static은 future work로 둔다.
- lag-1 whitening은 유지되지만 RMSE 이득이 사라지면 “기전은 성립하나 성능 이득은 운동 self-whitening으로 소멸한다”는 moving boundary 절을 강화한다.

## 실행 결과 요약

132개 paired trial을 완료했다. 전체적으로는 fixed mean RMSE 11.98 m, hop mean RMSE 10.49 m로 평균 +1.49 m 이득이 있었고, Wilcoxon one-sided p = 8.00e-05였다. DOA 고도각 residual lag-1도 fixed +0.220에서 hop -0.100으로 줄어 whitening 기전은 재확인되었다.

다만 가장 중요한 결론은 “0.100 m/s까지 연속적으로 준정지 영역이 검증되었다”가 아니다. 속도별 판정이 비단조로 나왔다.

| speed (m/s) | fixed mean RMSE | hop mean RMSE | mean gain | p | decision |
|---:|---:|---:|---:|---:|---|
| 0.000 | 11.95 | 8.62 | +3.32 | 0.0134 | validated |
| 0.005 | 11.14 | 9.72 | +1.42 | 0.0447 | validated |
| 0.010 | 12.13 | 12.35 | -0.22 | 0.2031 | not supported |
| 0.030 | 10.18 | 8.19 | +1.99 | 0.0022 | validated |
| 0.050 | 12.35 | 12.39 | -0.04 | 0.4498 | not supported |
| 0.100 | 14.12 | 10.75 | +3.38 | 0.0048 | validated |

따라서 논문용 안전 해석은 다음과 같다.

> Continuous quasi-static boundary는 0.005 m/s까지만 검증되었다. 0.030 m/s와 0.100 m/s에서의 양성 결과는 속도 자체의 단조 경계가 아니라 radial/tangential 기하와 tail 조건이 섞인 비단조 회복으로 해석해야 한다.

방향별 결과도 이 해석을 지지한다. 예를 들어 0.010 m/s에서는 tangential 조건은 validated였지만 radial 조건은 hop tail이 악화되어 not supported였다. 0.050 m/s에서도 tangential은 validated였으나 radial은 not supported였다. 즉 이동/준정지 구간의 핵심 변수는 속도 하나가 아니라 `속도 × 운동방향 × 표면반사 기하 × 필터 tail` 조합이다.

## 논문 반영 결론

- 본체 성능 주장은 계속 `static long-range USBL`을 중심으로 둔다.
- `quasi-static`은 “very slow drift up to 0.005 m/s under this protocol” 정도로 제한해서 쓴다.
- 0.030/0.100 m/s 양성 결과는 확장 claim이 아니라 “motion does not monotonically erase the benefit; geometry-dependent recoveries exist”로 Discussion에 둔다.
- 다음 연구는 `risk-aware geometry/motion classifier`나 `radial tail guard`가 필요하다. 단, 이는 본 논문 본체가 아니라 future work가 더 안전하다.
