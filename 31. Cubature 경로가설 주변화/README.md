# 31. Cubature 경로가설 주변화

## 목적

반사경로 하나를 hard 선택하거나 반사 TDOA를 단일 Gaussian 관측으로 직접 적층하지 않고,
UKF posterior의 상태 불확실성과 가능한 peak-경로 배정을 동시에 주변화하는 새 업데이트를 검증한다.

## 제안 업데이트

1. 기존 TOA 1개·센서간 TDOA 7개·SRP DOA 2개로 Adaptive UKF update
2. 결과 Gaussian을 동일한 양의 가중치의 12개 spherical-radial cubature point로 표현
3. 각 point에서 기준센서의 모든 유효 direct/surface/bottom peak 순열 likelihood 계산
4. `logsumexp`로 경로배정을 주변화하고 point evidence로 상태 가중치 갱신
5. 가중 상태를 평균·공분산으로 moment matching하여 다음 Kalman prediction에 전달

송신시각은 각 가설의 direct 후보 시간을 빼 제거한다. Ground Truth 경로 이름이나 실제 위치는
알고리즘에 사용하지 않는다.

## 검증 규칙

- validation에서 timing scale 0.25/0.5/1.0 ms와 temperature 1/2 중 하나 선택
- test 궤적·환경·noise seed 완전 분리
- validation/test 각각 거리당 4개 10-ping 궤적
- 첫 실행에서 넣었던 `0.1P` covariance retention은 균일 likelihood에서도 P를 팽창시키는
  혼입요인임을 발견해 폐기하고, 균일 evidence에서 원래 moment가 보존되도록 재실험

## 결과 (2026-07-05)

Validation은 `timing_std=1.0 ms, temperature=1`을 선택했다. 강건 점수는 baseline 8.625에서
5.419로 개선됐다.

독립 test:

| 거리 | Baseline 평균 RMSE | 제안 업데이트 평균 RMSE |
|---:|---:|---:|
| 100 m | 1.708 m | 1.468 m |
| 200 m | 11.065 m | 11.945 m |
| 400 m | 8.878 m | 8.958 m |
| 600 m | 9.292 m | 5.223 m |

- 강건 점수: 60.502 → 34.885
- 400m 발산률: 25% → 0%
- 200m 발산률은 양쪽 모두 25%
- 평균 유효 cubature point 수: 약 10.1~11.0/12

## 판정

Hard association과 Gaussian 직접 적층이 일반화에 실패했던 것과 달리, 상태·경로 가설의 soft
주변화는 독립 test의 강건 점수와 600m 오차를 크게 줄여 **신규 핵심 업데이트 후보로 예비 통과**한다.
그러나 200m와 400m 평균이 소폭 악화했고 거리당 4개 궤적뿐이므로 최종 채택은 아니다.

다음 단계에서는 선택된 정책을 변경하지 않고 더 많은 신규 궤적에서 재현성, P90, 발산률을
검증한다. 이후 효과가 유지될 때만 전체 8센서 경로 evidence와 관측 상관모델을 확장한다.
