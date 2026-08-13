# 183 result summary

## 판정

`hop_transition_softR`은 이번 800/1000 m static independent seed에서 hop baseline과 완전히 동일했다. 이유는 transition risk trigger가 0회였기 때문이다.

최종 decision: `extended_transition_aware_not_validated`

## 핵심 수치

Overall 24 cases:

| policy | mean RMSE (m) | median RMSE (m) | mean P90 (m) | divergence | transition risks |
|---|---:|---:|---:|---:|---:|
| fixed baseline | 19.348 | 19.092 | 19.636 | 0.000 | 0 |
| hop baseline | 12.801 | 9.449 | 14.489 | 0.000 | 0 |
| hop transition softR | 12.801 | 9.449 | 14.489 | 0.000 | 0 |

Comparisons:

| comparison | mean gain (m) | p | improved fraction |
|---|---:|---:|---:|
| softR vs hop | 0.000 | 1.000 | 0.000 |
| softR vs fixed | 6.547 | 6.56e-06 | 0.875 |
| hop vs fixed | 6.547 | 6.56e-06 | 0.875 |

## 해석

- 183의 독립 seed에서는 182에서 보였던 1000 m hop divergence가 재발하지 않았다.
- transition-aware softR은 observed TOA jump가 없으면 개입하지 않으므로 hop baseline과 동일하게 동작했다.
- 따라서 이 폴더는 “softR이 long-range tail을 줄인다”는 증거가 아니라, “trigger가 없을 때는 non-invasive하다”는 sanity check로 해석해야 한다.

## 다음 결정

0--1000 m 100 m 단위 sweep에서는 trigger 발생 구간과 거리별 RMSE 곡선을 함께 본다. 장거리 tail 안정화 claim은 아직 보류한다.
