# 8. 파형별 R 교정

## 목적

이전 단계의 고정 R은 경험적으로 정한 값이었다. 이번에는 파형별 독립 calibration
시나리오에서 실제 신호 추정오차의 평균 bias와 10×10 full covariance를 구하고, 별도
seed와 궤적에서만 성능을 평가한다.

## 분리 원칙

- calibration seed: 81001부터, 파형당 30개 독립 장면
- test seed: 92001부터, 30시점 별도 궤적
- calibration 거리: 80~650 m
- test 거리: 약 200 m부터 시작
- test에서는 매 ping마다 noise seed를 바꿈
- test Ground Truth는 평가에만 사용하고 필터 입력·R 수정에 사용하지 않음

## R 추정

관측 residual은 `[TOA range, TDOA range(7), azimuth, elevation]` 순서다. 평균 residual을
고정 bias correction으로 저장하고, 중심화 residual의 sample covariance에 25% diagonal
shrinkage와 작은 수치 floor를 적용한다. TOA/TDOA/DOA 사이의 경험적 cross covariance도
보존한다.

30표본은 논문용 교정에 충분하지 않으며 구현 방향 확인용이다. 최종 단계에서는 표본을
늘리고 거리·SNR별 이분산 R 또는 회귀형 R을 별도 검증해야 한다.

## 실행

```powershell
python test_calibration.py
python run_calibrated_compare.py
```

## 최초 결과 (2026-07-03)

test 궤적은 약 200 m에서 시작하며 각 ping에 서로 다른 noise seed를 사용했다.

| 파형 | R | 초기오차 | 5시점 이후 RMSE | 최대오차 | 마지막 오차 |
|---|---|---:|---:|---:|---:|
| 5 ms | 기존 | 11.188 m | 22.681 m | 40.938 m | 34.706 m |
| 5 ms | 교정 | 13.327 m | **16.081 m** | 28.746 m | 12.997 m |
| 10 ms | 기존 | 13.069 m | **13.384 m** | 24.776 m | 10.491 m |
| 10 ms | 교정 | 11.782 m | 21.435 m | 46.139 m | **5.439 m** |

5 ms 교정 R은 수렴 후 RMSE를 29.1% 개선했지만 여전히 크다. 10 ms의 전역 교정 R은
평균 RMSE를 60.2% 악화시켰으나 마지막 오차는 줄였다. 30개 장면의 단일 전역
covariance가 거리·수심·SNR에 따른 이분산성과 간헐적 peak switching을 충분히 나타내지
못한 것이다.

더 중요한 발견은 이전 100 m smoke test가 매 ping 같은 noise seed를 재사용했다는
점이다. 독립 seed와 약 200 m 조건에서는 기존 2.8 m 성능이 재현되지 않았다. 앞으로
모든 궤적 실험은 ping별 독립 seed를 기본으로 하며, 과거 2.8 m는 최종 기준으로 사용하지
않는다.

calibration에서 sensor 0 절대거리 표준편차가 5 ms 2.293 m, 10 ms 1.658 m로 나타났다.
이는 단순 가우시안 미세오차보다 matched-filter peak switching이 주된 문제임을 뜻한다.
다음 단계는 R 재조정보다 시간적으로 연속된 TOA peak tracking과 outlier 억제이다.
