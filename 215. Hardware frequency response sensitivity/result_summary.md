# Hardware frequency-response sensitivity result summary

## Overall policy metrics by response profile

| profile | policy | mean RMSE | median RMSE | mean P90 | divergence | n |
|---|---|---:|---:|---:|---:|---:|
| flat_reference | fixed_baseline | 10.530 | 8.304 | 12.480 | 0.031 | 192 |
| flat_reference | hop_baseline | 10.095 | 7.870 | 12.422 | 0.052 | 192 |
| flat_reference | hop_transition_softR | 7.684 | 6.471 | 9.101 | 0.005 | 192 |
| edge_loss_3db | fixed_baseline | 10.530 | 8.304 | 12.480 | 0.031 | 192 |
| edge_loss_3db | hop_baseline | 10.046 | 7.902 | 12.290 | 0.052 | 192 |
| edge_loss_3db | hop_transition_softR | 7.677 | 6.452 | 9.105 | 0.005 | 192 |
| edge_loss_6db | fixed_baseline | 10.530 | 8.304 | 12.480 | 0.031 | 192 |
| edge_loss_6db | hop_baseline | 10.070 | 7.951 | 12.298 | 0.052 | 192 |
| edge_loss_6db | hop_transition_softR | 7.687 | 6.452 | 9.088 | 0.005 | 192 |

## Paired comparisons

| profile | comparison | mean gain | p | improved frac | tail worsened | n |
|---|---|---:|---:|---:|---:|---:|
| flat_reference | softR_vs_hop | 2.411 | 2.928e-07 | 0.370 | 0.042 | 192 |
| flat_reference | softR_vs_fixed | 2.846 | 2.933e-08 | 0.651 | 0.151 | 192 |
| flat_reference | hop_vs_fixed | 0.435 | 0.05904 | 0.531 | 0.224 | 192 |
| edge_loss_3db | softR_vs_hop | 2.369 | 1.794e-07 | 0.380 | 0.042 | 192 |
| edge_loss_3db | softR_vs_fixed | 2.853 | 3.944e-08 | 0.641 | 0.146 | 192 |
| edge_loss_3db | hop_vs_fixed | 0.484 | 0.06408 | 0.521 | 0.224 | 192 |
| edge_loss_6db | softR_vs_hop | 2.383 | 1.765e-07 | 0.375 | 0.042 | 192 |
| edge_loss_6db | softR_vs_fixed | 2.842 | 2.481e-08 | 0.646 | 0.141 | 192 |
| edge_loss_6db | hop_vs_fixed | 0.459 | 0.05431 | 0.526 | 0.229 | 192 |

## Interpretation boundary

This is an idealized response-mismatch sensitivity simulation. It reduces, but does not eliminate, the hardware-response weakness. Real transducer/hydrophone response must still be measured in a later field or bench-validation study.
