# OOD motion transition-aware validation result

## Protocol

- paired OOD cases: 528
- distances: [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
- conditions: ['accelerating_radial', 'curved_arc', 'mixed_radial_tangential', 'vertical_sine']
- policies: fixed, plain hop, transition-aware soft-R
- claim boundary: first-pass OOD probe, not full robustness proof.

## Overall

| policy | mean RMSE | median RMSE | P90 RMSE | divergence |
|---|---:|---:|---:|---:|
| fixed_baseline | 10.832 | 8.198 | 22.339 | 0.049 |
| hop_baseline | 10.691 | 7.565 | 21.611 | 0.057 |
| hop_transition_softR | 7.809 | 6.478 | 15.936 | 0.006 |

## Comparisons

| comparison | mean gain | median gain | improved fraction | tail worsened | p |
|---|---:|---:|---:|---:|---:|
| softR_vs_hop | 2.881 | 0.000 | 0.496 | 0.036 | 9.076e-22 |
| softR_vs_fixed | 3.023 | 0.375 | 0.648 | 0.152 | 1.015e-18 |
| hop_vs_fixed | 0.141 | 0.065 | 0.562 | 0.242 | 2.414e-03 |

## Distance breakdown

| distance | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |
|---:|---:|---:|---:|---:|---:|
| 0 | 2.778 | 3.291 | 3.291 | 0.000 | 0.000 |
| 100 | 1.969 | 1.948 | 1.767 | 0.180 | 0.000 |
| 200 | 6.372 | 6.021 | 3.520 | 2.501 | 0.000 |
| 300 | 11.663 | 12.015 | 5.288 | 6.727 | 0.021 |
| 400 | 10.960 | 10.596 | 5.976 | 4.619 | 0.021 |
| 500 | 12.726 | 14.920 | 9.524 | 5.396 | 0.062 |
| 600 | 12.922 | 12.921 | 9.331 | 3.590 | 0.062 |
| 700 | 12.295 | 12.837 | 9.748 | 3.089 | 0.083 |
| 800 | 15.346 | 14.228 | 11.660 | 2.568 | 0.042 |
| 900 | 16.294 | 13.015 | 12.372 | 0.643 | 0.062 |
| 1000 | 15.828 | 15.809 | 13.427 | 2.382 | 0.042 |

## Condition breakdown

| condition | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |
|---|---:|---:|---:|---:|---:|
| accelerating_radial | 9.729 | 9.439 | 7.192 | 2.247 | 0.030 |
| curved_arc | 10.465 | 10.228 | 7.672 | 2.556 | 0.068 |
| mixed_radial_tangential | 11.254 | 10.352 | 8.098 | 2.254 | 0.023 |
| vertical_sine | 11.881 | 12.745 | 8.276 | 4.468 | 0.023 |