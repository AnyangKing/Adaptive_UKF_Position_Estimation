# 181. Transition aware Adaptive R independent moving validation

## 목적

180번 development pilot에서 유망했던 `hop_transition_softR`을 독립 moving seed에서 검증한다.

180번 이후 동결한 설정:

- `range_jump_threshold_m = 0.5`
- `max_toa_scale = 100`
- carrier schedule: 30--34 kHz linear20
- 기존 Conditional Adaptive-R의 GCC-SRP disagreement/NIS routing 유지

## 실험 설계

- 거리: 600 m
- moving condition: 63번과 동일한 4개 조건
  - `radial_0.05`
  - `radial_1.0`
  - `tangential_1.0`
  - `tang_1.0_vz`
- 조건당 geometry: 12
- 총 paired moving cases: 48
- 비교:
  - `fixed_baseline`
  - `hop_baseline`
  - `hop_transition_softR`
- seed:
  - geometry root: 1,810,000
  - ping root: 1,813,000

## 판정 기준

`hop_transition_softR`이 독립검증 후보를 넘어서려면 다음을 동시에 만족해야 한다.

- hop baseline 대비 mean gain > 0
- hop baseline 대비 Wilcoxon one-sided p < 0.05
- tail worsened fraction <= 0.10
- divergence rate가 hop baseline보다 증가하지 않음
- fixed baseline 대비 평균 이득도 양수이면 강한 성공, 아니면 “hop 안정화 성공”으로 제한

## claim boundary

- 이 폴더는 moving target 성능 claim 후보를 처음으로 독립검증하는 단계다.
- 성공하더라도 원고에 넣기 전에는 181 결과의 per-condition breakdown과 failure cases를 반드시 함께 보고한다.
- 실패하면 180은 development-only pilot으로 강등한다.
