# OOD motion transition-aware validation result

## Protocol

- paired OOD cases: 12
- distances: [400.0, 800.0, 1000.0]
- conditions: ['accelerating_radial', 'curved_arc', 'mixed_radial_tangential', 'vertical_sine']
- policies: fixed, plain hop, transition-aware soft-R
- claim boundary: first-pass OOD probe, not full robustness proof.

## Overall

| policy | mean RMSE | median RMSE | P90 RMSE | divergence |
|---|---:|---:|---:|---:|
| fixed_baseline | 12.333 | 8.770 | 15.884 | 0.083 |
| hop_baseline | 10.720 | 8.574 | 13.077 | 0.083 |
| hop_transition_softR | 8.351 | 8.574 | 11.040 | 0.000 |

## Comparisons

| comparison | mean gain | median gain | improved fraction | tail worsened | p |
|---|---:|---:|---:|---:|---:|
| softR_vs_hop | 2.369 | 0.034 | 0.667 | 0.083 | 3.815e-02 |
| softR_vs_fixed | 3.982 | 0.635 | 0.667 | 0.250 | 3.013e-01 |
| hop_vs_fixed | 1.613 | 0.162 | 0.583 | 0.250 | 6.221e-01 |

## Distance breakdown

| distance | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |
|---:|---:|---:|---:|---:|---:|
| 400 | 16.705 | 13.429 | 6.622 | 6.807 | 0.000 |
| 800 | 11.393 | 10.016 | 9.999 | 0.017 | 0.000 |
| 1000 | 8.901 | 8.715 | 8.431 | 0.283 | 0.250 |

## Condition breakdown

| condition | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |
|---|---:|---:|---:|---:|---:|
| accelerating_radial | 11.826 | 8.190 | 7.394 | 0.796 | 0.000 |
| curved_arc | 7.946 | 9.783 | 8.516 | 1.267 | 0.000 |
| mixed_radial_tangential | 8.502 | 7.565 | 7.453 | 0.112 | 0.333 |
| vertical_sine | 21.059 | 17.340 | 10.039 | 7.301 | 0.000 |