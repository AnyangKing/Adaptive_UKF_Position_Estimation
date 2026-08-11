# 179. TOA branch switching independent validation

## 목적

162번의 `CarrierTransitionTOAGuardUKF`는 post-hoc tail geometry에서 만든 pilot이었다. 이 폴더는 동일한 guard rule을 새 seed root의 독립 static geometries에서 검증한다.

검증 대상은 성능 향상 claim이 아니라 다음 질문이다.

> carrier transition과 reference TOA jump가 동시에 나타날 때 TOA block만 격리하는 rule이 독립 seed에서도 tail을 줄이는가?

## 설계

- 거리: 600 m static target
- schedule:
  - `fixed32`
  - `linear20_30_34`
  - `four_carrier_cycle`
- 비교:
  - baseline conditional Adaptive-R UKF
  - carrier-transition TOA guard UKF
- seed:
  - geometry root: 1,790,000
  - ping root: 1,793,000
- n: 20 independent geometries
- paired design: 같은 기하, 환경, ping seed, 수신 신호를 baseline과 guard에 입력

## claim boundary

- 이 폴더는 정지 표적 schedule-tail guard 검증이다.
- moving target 성능 claim으로 사용하지 않는다.
- 통과하더라도 180번 moving 개발 후보의 부품으로만 사용한다.
- 실패하면 TOA branch switching guard는 post-hoc tail 설명으로만 남긴다.
