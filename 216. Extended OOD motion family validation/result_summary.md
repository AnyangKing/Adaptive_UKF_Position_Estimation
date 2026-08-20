# Extended OOD motion-family validation result

## Protocol

- paired cases: 144
- distances: [0.0, 200.0, 400.0, 600.0, 800.0, 1000.0]
- conditions: ['stop_go', 'direction_reversal', 'spiral_climb', 'burst_turn']
- policies: fixed, plain hop, transition-aware soft-R
- claim boundary: additional OOD-family simulation, not arbitrary moving-target proof.

## Overall

| policy | mean RMSE | median RMSE | mean P90 | divergence | n |
|---|---:|---:|---:|---:|---:|
| fixed_baseline | 12.475 | 9.266 | 15.321 | 0.056 | 144 |
| hop_baseline | 11.371 | 7.994 | 13.956 | 0.049 | 144 |
| hop_transition_softR | 8.128 | 7.446 | 9.737 | 0.000 | 144 |

## Paired comparisons

| comparison | mean gain | p | improved frac | tail worsened | n |
|---|---:|---:|---:|---:|---:|
| softR_vs_hop | 3.243 | 1.499e-05 | 0.535 | 0.056 | 144 |
| softR_vs_fixed | 4.347 | 4.731e-08 | 0.653 | 0.153 | 144 |
| hop_vs_fixed | 1.104 | 0.000951 | 0.597 | 0.222 | 144 |

## Condition breakdown

| condition | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |
|---|---:|---:|---:|---:|---:|
| stop_go | 11.429 | 11.849 | 9.011 | 2.838 | 0.056 |
| direction_reversal | 12.341 | 10.065 | 7.450 | 2.615 | 0.056 |
| spiral_climb | 10.845 | 11.961 | 6.974 | 4.987 | 0.083 |
| burst_turn | 15.286 | 11.610 | 9.079 | 2.531 | 0.028 |

## Distance breakdown

| distance | fixed | hop | softR | softR gain vs hop | softR tail worse vs hop |
|---:|---:|---:|---:|---:|---:|
| 0 | 3.842 | 3.452 | 3.453 | -0.001 | 0.000 |
| 200 | 11.579 | 8.142 | 4.172 | 3.969 | 0.000 |
| 400 | 12.928 | 16.765 | 6.818 | 9.947 | 0.000 |
| 600 | 16.672 | 14.570 | 10.559 | 4.011 | 0.125 |
| 800 | 12.408 | 12.073 | 11.204 | 0.870 | 0.125 |
| 1000 | 17.422 | 13.225 | 12.564 | 0.661 | 0.083 |

## Interpretation boundary

This extends the simulated OOD motion set, but it still does not prove arbitrary moving-target performance. It should be cited as additional OOD-family evidence only.
