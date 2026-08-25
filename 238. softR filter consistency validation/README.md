# 238. softR filter consistency validation

## 목적

리뷰/감사에서 지적된 가장 큰 미해결 항목은 transition-aware softR가 RMSE와 발산률을 개선하더라도 필터 공분산 일관성은 깨뜨릴 수 있다는 점이었다.

이 폴더는 191번 이동표적 0--1000 m 독립 검증 프로토콜을 그대로 재사용하면서, 각 필터의 settled 구간에서 다음 지표를 추가로 기록한다.

- 위치 NEES: 필터가 보고한 위치 공분산 `P_xyz`가 실제 위치 오차를 어느 정도 설명하는지 확인한다.
- 총 NIS: 실제 업데이트에 사용된 최종 measurement covariance `R` 기준 innovation consistency를 확인한다.
- 블록 NIS: TOA, TDOA, DOA 관측 블록별 이상치를 확인한다.

## 원칙

- 새 알고리즘을 만들지 않는다. 181/191 계열의 frozen transition-aware softR 규칙을 재실행해 일관성 지표만 추가한다.
- ground truth는 신호 합성과 최종 오차/NEES 계산에만 사용한다.
- adaptive decision은 관측 TOA 변화, carrier transition, GCC-SRP disagreement, innovation/NIS만 사용한다.
- NIS는 최종 UKF update에 들어간 `R`을 기준으로 재계산해 보고한다.
- 위치 NEES의 기준 차원은 3이다. 총 NIS의 기준 차원은 TOA 1 + TDOA 7 + DOA 2 = 10이다.

## 결과

`run_softR_consistency_validation.py` 실행 후 `softR_consistency_validation.json`과 `result_summary.md`에 기록한다.

실행 결과, transition-aware softR는 191번의 이동표적 성능 이득을 유지하면서 공분산 과신도 크게 줄였다.

- hop baseline 대비 mean RMSE: 11.337 m → 7.389 m
- divergence rate: 7.2% → 0.4%
- position NEES: 255.84 → 16.00
- total NIS chi2-99 exceedance: 0.119 → 0.038

다만 3D 위치 NEES의 이상적 평균은 약 3이므로, softR를 “완전히 calibration된 필터”라고 주장하면 안 된다. 논문에서는 “과신을 완화하고 발산을 억제했지만, residual covariance miscalibration은 남는다”는 절제된 표현이 맞다.
