# Axis-wise error decomposition validation

## Overall policy metrics

| policy | 3D RMSE | horizontal RMSE | vertical RMSE | radial RMSE | cross-range RMSE | div. | n |
|---|---:|---:|---:|---:|---:|---:|---:|
| fixed_baseline | 12.186 | 7.842 | 8.154 | 1.013 | 7.637 | 0.072 | 528 |
| hop_baseline | 11.337 | 7.457 | 7.442 | 0.940 | 7.275 | 0.072 | 528 |
| hop_transition_softR | 7.389 | 4.851 | 4.582 | 0.625 | 4.664 | 0.004 | 528 |

## softR gains against hop baseline

| metric | mean gain | 95% CI | Wilcoxon p | improved frac | n |
|---|---:|---:|---:|---:|---:|
| settled_rmse_m | 3.948 | [2.887, 5.154] | 0.0000 | 0.409 | 528 |
| horizontal_rmse_m | 2.606 | [1.955, 3.314] | 0.0000 | 0.399 | 511 |
| vertical_rmse_m | 2.860 | [1.926, 3.971] | 0.0000 | 0.391 | 511 |
| radial_rmse_m | 0.315 | [0.218, 0.432] | 0.0000 | 0.401 | 511 |
| cross_range_rmse_m | 2.611 | [1.952, 3.326] | 0.0000 | 0.395 | 511 |

## Distance-wise softR decomposition

| distance m | 3D gain vs hop | horizontal gain vs hop | vertical gain vs hop | softR horizontal RMSE | softR vertical RMSE | n |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | -0.000 | -0.000 | -0.000 | 1.255 | 0.329 | 48 |
| 100 | 0.075 | 0.072 | 0.031 | 1.201 | 0.846 | 48 |
| 200 | 4.833 | 3.841 | 2.221 | 3.409 | 1.485 | 48 |
| 300 | 4.245 | 2.436 | 3.133 | 3.533 | 2.348 | 48 |
| 400 | 4.292 | 3.433 | 2.337 | 3.845 | 3.051 | 48 |
| 500 | 4.960 | 3.197 | 3.510 | 3.935 | 4.467 | 48 |
| 600 | 4.872 | 3.663 | 3.130 | 5.519 | 5.563 | 48 |
| 700 | 3.483 | 1.684 | 2.878 | 5.689 | 6.477 | 48 |
| 800 | 11.557 | 5.991 | 9.163 | 7.385 | 6.661 | 48 |
| 900 | 4.379 | 2.772 | 3.478 | 7.489 | 8.383 | 48 |
| 1000 | 0.730 | 0.652 | 0.562 | 8.830 | 9.291 | 48 |

## Interpretation boundary

This is a state-space diagnostic under the same simulation protocol as 191/238. It supports axis-wise simulation interpretation only and does not replace real-water validation.

## Interpretation

The transition-aware softR improvement is not only a scalar 3D RMSE artifact. Against the hopping baseline, the mean RMSE reduction appears in both horizontal and vertical components:

- horizontal RMSE: 7.457 m to 4.851 m
- vertical RMSE: 7.442 m to 4.582 m
- cross-range RMSE: 7.275 m to 4.664 m
- radial RMSE: 0.940 m to 0.625 m

The small radial error and much larger cross-range/vertical errors are consistent with the small-aperture USBL interpretation: range-like information is comparatively stable, while angular information dominates the difficult error modes. This complements the folder-238 observation-space result where the DOA block NIS was the dominant residual inconsistency.

The manuscript should use this as a state-space diagnostic, not as an additional generalization claim.
