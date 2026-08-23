# Static full-range independent validation

This is an independent n=20-per-distance validation of the frozen static full-range protocol.
It upgrades folder 184 from a low-n diagnostic trend map to a denser validation set.

## Overall paired comparisons

| comparison | mean gain | median gain | 95% CI | p | improved frac | tail worsened | n |
|---|---:|---:|---:|---:|---:|---:|---:|
| hop_vs_fixed | 2.001 | 0.585 | [1.286, 2.740] | 5.343e-09 | 0.645 | 0.141 | 220 |
| softR_vs_hop | -0.011 | 0.000 | [-0.041, 0.011] | 0.5705 | 0.023 | 0.005 | 220 |
| softR_vs_fixed | 1.990 | 0.585 | [1.275, 2.730] | 5.866e-09 | 0.645 | 0.141 | 220 |

## Distance breakdown

| distance | fixed | hop | softR | hop gain vs fixed | softR gain vs fixed | hop tail worsened | softR tail worsened | n |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 7.513 | 9.113 | 9.113 | -1.600 | -1.600 | 0.350 | 0.350 | 20 |
| 100 | 1.722 | 1.619 | 1.619 | 0.103 | 0.103 | 0.000 | 0.000 | 20 |
| 200 | 4.236 | 4.912 | 4.859 | -0.676 | -0.623 | 0.100 | 0.100 | 20 |
| 300 | 5.999 | 4.296 | 4.296 | 1.703 | 1.703 | 0.150 | 0.150 | 20 |
| 400 | 7.616 | 5.792 | 5.792 | 1.824 | 1.824 | 0.100 | 0.100 | 20 |
| 500 | 7.961 | 8.010 | 8.005 | -0.049 | -0.044 | 0.200 | 0.200 | 20 |
| 600 | 10.753 | 7.990 | 8.035 | 2.763 | 2.718 | 0.150 | 0.150 | 20 |
| 700 | 14.671 | 10.752 | 10.755 | 3.919 | 3.916 | 0.050 | 0.050 | 20 |
| 800 | 13.941 | 9.795 | 9.800 | 4.146 | 4.141 | 0.100 | 0.100 | 20 |
| 900 | 19.589 | 13.130 | 13.120 | 6.459 | 6.470 | 0.050 | 0.050 | 20 |
| 1000 | 20.103 | 16.689 | 16.822 | 3.414 | 3.281 | 0.300 | 0.300 | 20 |

## Interpretation boundary

- This validation uses static simulated beacons under the existing shallow-water signal-level simulator.
- It does not add real-water or hardware frequency-response evidence.
- The 0 m case is a near-vertical degenerate geometry and should not be used as positive long-range evidence.
- The main manuscript can use this result only as simulation-level full-range static support.
