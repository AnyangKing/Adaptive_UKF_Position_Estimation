# Moving target failure mode map

이 문서는 기존 결과 JSON만 읽어 만든 실패 지도다. 새 실험이나 새 성능 claim은 없다.

## Failure modes

| failure mode | key evidence | runtime-observable signals | offline-only signals | next action |
|---|---|---|---|---|
| motion_self_whitening | mean gain -0.103 m, p=0.301; lag-1 0.470→-0.208 | short-window DOA innovation variance, GCC-SRP disagreement, NIS tail | true elevation residual lag-1, fixed-vs-hop paired RMSE gain, ground-truth motion class | Do not use lag-1 reduction as a moving-target performance claim. |
| schedule_safety_evaporation | 64 hop gain -0.701 m; 66 hop gain -1.690 m; 67 oracle gain -0.306 m | carrier schedule, GCC-SRP disagreement, NIS, observed TOA/TDOA jumps | oracle condition label, paired RMSE gain | Deprioritize schedule-only motion-aware methods. |
| carrier_transition_toa_branch_switching | 160 four-carrier RMSE 11.925 m, div 0.050; 162 pilot 23.198→8.273 m | reference TOA adjacent range jump, carrier change flag, TOA block NIS, matched-filter peak quality | post-validation selected tail geometry | Run 179 independent validation before using the guard as a method component. |

## Candidate ranking

| priority | candidate | reason | status |
|---:|---|---|---|
| 1 | TOA branch switching independent validation | Uses observable TOA jump + carrier transition and already passed a post-hoc pilot. | validation_candidate_not_claimed |
| 2 | carrier-transition-aware Adaptive-R | Generalizes TOA guard from static tail control into an observed-risk covariance routing rule. | development_candidate |
| 3 | motion-aware adaptive transmission schedule | Oracle condition-aware schedule failed on independent seed; runtime risk detection has a low ceiling. | future_work_only |

## Claim boundary

- Moving-target pooled RMSE improvement is not established.
- Residual lag-1 reduction is mechanism evidence only.
- Post-hoc/oracle results cannot be promoted to method performance without independent validation.
- Future moving-target methods must use only observed TOA/TDOA/DOA/quality/NIS features.
