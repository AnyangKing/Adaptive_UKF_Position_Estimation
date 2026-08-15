# Interpretation

## Bottom line

The first-pass 24-case subset does not show an obvious parameter fragility.

Across all nine tested settings, transition-aware soft-R improved over both folder-191 baselines on this subset:

- gain vs plain hop: 7.171--7.269 m
- gain vs fixed: 3.242--3.339 m
- tail worsened vs hop: 0.000 for all tested settings

The canonical folder-191 setting, `range_jump_threshold_m=0.5` and `max_toa_scale=100`, was not uniquely special:

- canonical mean RMSE: 6.986 m
- canonical gain vs hop: 7.205 m
- canonical gain vs fixed: 3.276 m

The best subset setting was `threshold=1.0, cap=100/400`, but this folder must not be used to retune the adopted method. The subset is too small for parameter selection.

## What this supports

This supports a limited statement:

> In a first-pass sensitivity probe, the moving-target benefit of transition-aware Adaptive-R was not confined to a single threshold/cap pair.

## What this does not support

This does not support:

- replacing the 191 full 528-case validation,
- changing the adopted canonical setting,
- claiming global robustness over all motion and channel conditions,
- claiming real-water performance.

## Distance-wise canonical behavior

For the canonical `0.5/100` setting:

| distance | canonical RMSE | gain vs hop | tail worse vs hop |
|---:|---:|---:|---:|
| 0 m | 4.764 | -0.000 | 0.000 |
| 200 m | 1.909 | 2.101 | 0.000 |
| 400 m | 3.520 | 3.608 | 0.000 |
| 600 m | 7.598 | 11.811 | 0.000 |
| 800 m | 9.823 | 25.710 | 0.000 |
| 1000 m | 14.301 | -0.001 | 0.000 |

The very large 800 m subset gain is consistent with the failure-and-recovery pattern already seen in folder 191, but this subset should not be treated as a new headline result.

## Condition-wise canonical behavior

| condition | canonical RMSE | gain vs hop | tail worse vs hop |
|---|---:|---:|---:|
| radial_0.05 | 8.942 | 9.622 | 0.000 |
| radial_1.0 | 6.076 | 0.398 | 0.000 |
| tangential_1.0 | 7.390 | 17.141 | 0.000 |
| tang_1.0_vz | 5.535 | 1.659 | 0.000 |

The subset indicates that most of the gain comes from the same tail-prone geometries that motivated transition-aware soft-R. The radial_1.0 and tangential+vertical subset gains are smaller, so broader OOD motion remains necessary.

## Next implication

The next simulation should not be another small threshold tweak. The useful next step is OOD motion validation:

- curved trajectories,
- acceleration/deceleration,
- abrupt turns,
- mixed radial/tangential motion,
- vertical maneuvers not seen in the validation set.

If transition-aware soft-R survives OOD motion, the moving-target manuscript claim becomes much stronger.
