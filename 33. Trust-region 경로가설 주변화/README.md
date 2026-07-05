# 33. Trust-region 경로가설 주변화

## 목적

32번의 confidently-wrong 경로 posterior가 기존 TOA/TDOA/DOA posterior를 과도하게 이동시키는
문제를 줄이기 위해, 경로 update의 Mahalanobis 이동량을 제한하는 trust-region moment matching을
검증한다.

## 방법

- 기존 1ms cubature 경로 likelihood 고정
- raw 경로 posterior 평균 이동 `d`에 대해 `sqrt(dᵀP⁻¹d)` 계산
- 반경 초과 시 혼합비를 줄이고 prior/path posterior의 혼합 평균과 모드간 분산까지 보존
- validation 후보: unbounded, 반경 0.25/0.5/1/2
- validation/test 각각 거리당 4개 독립 궤적

## 결과 (2026-07-05)

Validation은 unbounded를 선택했다. 강건 점수는 baseline 10.256, unbounded 6.313이며 r1도
6.352로 비슷했지만 제한이 거의 발동하지 않았다. 선택된 unbounded의 최초 독립 test 강건 점수는
baseline 10.509에서 34.001로 악화했고 400m 발산률이 0→25%가 됐다.

최초 test를 개발자료로 강등한 사후 진단:

- unbounded: 400m 12.391m, 600m 6.885m, 400m 발산 25%
- r0.25: 400m 10.902m, 600m 7.929m, 400m 발산 25%
- r0.5: 400m 11.645m, 600m 7.185m, 400m 발산 25%
- r1: 400m 12.291m, 600m 6.818m, 400m 발산 25%

## 판정

모든 반경에서 발산이 남아 **trust-region 상태이동 방식은 기각**한다. 한 ping의 큰 이동을 제한해도
잘못된 경로 모드가 여러 ping에서 일관되게 선택되면 작은 편향 이동이 누적된다.

다음 단계부터 반사경로 likelihood로 상태 평균을 직접 이동시키지 않는다. 물리 경로 일관성을
기존 TOA/TDOA/DOA 관측의 신뢰도 또는 공분산에 반영하여, 잘못된 경로가 새로운 위치 모드를
강제로 만드는 구조를 제거한다.
