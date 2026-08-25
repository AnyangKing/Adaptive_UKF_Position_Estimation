# 241. Axis metric finite n clarification

## 목적

240번에서 원고에 238/239 진단 결과를 반영했지만, 239의 축별 paired-gain 검정은 528개 전체가 아니라 유한한 settled axis metric을 가진 511개 paired cases로 계산되었다.

## 확인 결과

- 전체 moving validation trial 수: 528 paired cases
- 3D RMSE 및 divergence: 528 cases 기준
- NEES/NIS 정책별 요약: 528 cases 기준
- 축별 paired-gain 검정: 511 finite cases 기준
- 빠진 17개는 모두 0 m near-vertical degenerate 조건에서 발생
- 해당 17개는 발산 trial이 아니라, 축별 settled metric이 유한하게 남지 않은 계산 불능/예외 케이스

## 원고 반영

`tab:consistencyaxis` caption에 다음 경계를 추가했다.

- 축별 paired-gain 통계는 511 finite cases 기준
- 전체 3D RMSE와 divergence 검증은 528 cases 기준

이 패치는 새 실험 없이 표 해석의 n 경계를 명확히 하는 작업이다.

