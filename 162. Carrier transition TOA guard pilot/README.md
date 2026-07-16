# 162. Carrier transition TOA guard pilot

## 새 방법

`CarrierTransitionTOAGuardUKF`는 다음 조건이 동시에 발생한 ping에서 절대 TOA(range) 블록만
격리한다.

1. 직전 ping과 carrier가 다르다.
2. 직전 raw range와 현재 raw range 차이가 0.5 m를 넘는다.

해당 ping에서 TOA 분산을 1e12 m²로 두어 update 영향만 사실상 제거한다. TDOA 7개와 DOA
2개는 그대로 adaptive-R UKF에 들어간다. 따라서 전체 관측을 버리지 않고 carrier-induced TOA
branch switch만 분리하는 모달리티 선택적 guard다.

## 개발 범위

- 161번에서 이미 결과를 본 geometry 2, 5, 19만 사용한다.
- fixed, linear20, four-carrier 각각에 기존 adaptive-R과 guard를 같은 관측으로 비교한다.
- 0.5 m threshold와 hard isolation은 이 개발 표본에서 처음 정한 값이다.
- static 전용 pilot이며 이동 표적 성능으로 확장하지 않는다.

## 사전 개발 판정

- geometry 2 four-carrier RMSE를 기존의 25% 이하로 줄이고 발산 제거.
- 세 기하 four-carrier 평균 RMSE 개선.
- linear20 평균 RMSE 악화 10% 이내.
- guard 필터 예외 0.

모두 통과해도 신규 방법의 성능 claim은 불가하며, 163번 완전 신규 seed에서만 채택 여부를
판정한다.

## 실행

```powershell
python test_protocol.py
python run_transition_guard_pilot.py
```

## 완료 결과

개발 기준을 모두 통과했다. geometry 2 four-carrier는 53.001→8.224 m로 감소하고 발산이
사라졌다. 세 기하 four-carrier 평균은 23.198→8.273 m, linear 평균은 6.608→6.607 m였으며
fixed는 guard가 비활성이라 동일했다.

판정은 `advance_to_independent_validation`이지만, 동일한 post-hoc 기하에서 만든 결과이므로
논문 claim은 금지한다. 사용자 지시에 따라 이 폴더에서 연구를 멈추며 163번 신규 seed 검증은
다음 재개 작업으로 남긴다.
