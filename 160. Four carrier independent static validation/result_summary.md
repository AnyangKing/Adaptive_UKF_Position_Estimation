# 160 결과 요약

## 독립검증 결과

159번과 겹치지 않는 신규 seed 20기하에서 fixed, 기존 linear20, four-carrier cycle을 비교했다.

| schedule | mean settled RMSE (m) | median (m) | mean P90 (m) | mean abs lag-1 | divergence |
|---|---:|---:|---:|---:|---:|
| fixed32 | 11.571 | 11.443 | 11.840 | 0.763 | 0/20 |
| linear20_30_34 | **8.798** | **7.765** | **9.889** | **0.336** | 0/20 |
| four-carrier cycle | 11.925 | 9.323 | 14.292 | 0.351 | 1/20 |

### 기존 linear 대 fixed

- mean gain +2.773 m, 약 24.0% RMSE 감소.
- bootstrap CI95 [+1.362, +4.210] m.
- median gain +2.624 m, 15/20 개선.
- one-sided paired Wilcoxon p=0.001576.
- P90 RMSE gain +2.075 m, mean abs lag-1 0.763→0.336, 발산 0.
- 사전 기준 전부 통과.

### four-carrier 대 fixed/linear

- fixed 대비 median gain은 +1.535 m이고 14/20에서 개선했지만 mean gain은 −0.354 m,
  P90 gain은 −0.842 m, 발산은 1/20이었다.
- geometry 2에서 settled RMSE 53.001 m가 발생했다(fixed 10.151, linear 7.360 m).
- linear 대비 mean gain −3.127 m, CI95 [−8.075, −0.138] m, 개선 9/20,
  superiority p=0.943.
- 동결 규칙에 따라 `independent_validation_failed`다. median과 Wilcoxon 일부 지표가 좋아도
  mean·tail·발산 기준을 사후 제거하지 않는다.

## 결론

159번 n=4에서 강해 보였던 four-carrier sparse bank는 독립 seed에서 tail 위험으로 증발했다.
반대로 기존 20-carrier linear sweep은 이번 신규 20기하에서도 fixed 대비 유의하게 재현됐다.
따라서 schedule 최적화 claim은 만들지 않고, **넓고 조밀한 sweep의 강건성**과 **carrier 수를
성급히 줄이면 median 이득과 tail 안정성이 분리될 수 있음**을 보강 결과로 남긴다.

원고 자동 수정은 하지 않는다. 이 결과는 보충자료/응답자료 반영 여부를 별도로 검토한다.
