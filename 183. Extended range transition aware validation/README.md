# 183. Extended range transition aware validation

## 목적

182번에서 800/1000 m static range extension은 평균 RMSE 개선을 보였지만, 1000 m에서 carrier hop divergence가 발생했다. 이 폴더는 181번에서 독립 moving 검증을 통과한 `transition-aware softR`을 static long-range에도 적용해 tail/divergence를 줄일 수 있는지 확인한다.

## 설계

- distances: 800 m, 1000 m
- geometries per distance: 12
- policies:
  - `fixed_baseline`: fixed 32 kHz + Conditional Adaptive-R
  - `hop_baseline`: linear20 30--34 kHz + Conditional Adaptive-R
  - `hop_transition_softR`: linear20 30--34 kHz + transition-aware TOA covariance inflation
- frozen transition-aware parameters:
  - `range_jump_threshold_m = 0.5`
  - `max_toa_scale = 100`

## 판정

주요 질문:

1. hop baseline 대비 평균 RMSE를 개선하는가?
2. hop baseline 대비 divergence/tail을 줄이는가?
3. fixed baseline 대비도 유의미한 이득을 유지하는가?

## claim boundary

- 이 결과는 static simulation extension이다.
- real-water 1 km 성능으로 일반화하지 않는다.
- divergence와 tail을 숨기지 않는다.
