# Moving tail case decomposition

This analysis decomposes the 191 full-range moving validation tails without rerunning the simulator.
Tail is defined as paired gain < -1.0 m, i.e. the target policy is more than 1 m worse than the reference.

## Overall

- Cases: 528
- softR vs fixed mean gain: 4.797 m
- softR vs fixed tail worsened fraction: 0.131
- softR vs hop mean gain: 3.948 m
- softR vs hop tail worsened fraction: 0.028
- hop vs fixed tail worsened fraction: 0.214

## Distance decomposition

| distance_m | n | softR_gain_vs_fixed_m | softR_tail_vs_fixed_fraction | softR_gain_vs_hop_m | softR_tail_vs_hop_fraction | hop_tail_vs_fixed_fraction |
|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 48 | -0.255 | 0.083 | -0.000 | 0 | 0.083 |
| 100.000 | 48 | 0.152 | 0.021 | 0.075 | 0 | 0.021 |
| 200.000 | 48 | 4.976 | 0.042 | 4.833 | 0 | 0.167 |
| 300.000 | 48 | 5.573 | 0.062 | 4.245 | 0 | 0.125 |
| 400.000 | 48 | 6.329 | 0.062 | 4.292 | 0.021 | 0.229 |
| 500.000 | 48 | 7.798 | 0.188 | 4.960 | 0.021 | 0.250 |
| 600.000 | 48 | 6.358 | 0.229 | 4.872 | 0.021 | 0.292 |
| 700.000 | 48 | 5.711 | 0.229 | 3.483 | 0.104 | 0.250 |
| 800.000 | 48 | 6.867 | 0.167 | 11.557 | 0.042 | 0.375 |
| 900.000 | 48 | 5.128 | 0.167 | 4.379 | 0.062 | 0.333 |
| 1000.000 | 48 | 4.127 | 0.188 | 0.730 | 0.042 | 0.229 |

## Motion-condition decomposition

| condition | n | softR_gain_vs_fixed_m | softR_tail_vs_fixed_fraction | softR_gain_vs_hop_m | softR_tail_vs_hop_fraction | hop_tail_vs_fixed_fraction |
|---|---:|---:|---:|---:|---:|---:|
| radial_0.05 | 132 | 4.919 | 0.098 | 4.785 | 0.038 | 0.197 |
| radial_1.0 | 132 | 3.940 | 0.136 | 3.168 | 0.008 | 0.212 |
| tang_1.0_vz | 132 | 4.424 | 0.182 | 3.580 | 0.023 | 0.273 |
| tangential_1.0 | 132 | 5.904 | 0.106 | 4.259 | 0.045 | 0.174 |

## Highest softR-vs-fixed tail cells

| distance_m | condition | n | softR_gain_vs_fixed_m | softR_tail_vs_fixed_fraction | softR_gain_vs_hop_m | softR_tail_vs_hop_fraction |
|---:|---|---:|---:|---:|---:|---:|
| 700.000 | radial_1.0 | 12 | 3.337 | 0.417 | 5.684 | 0 |
| 900.000 | tang_1.0_vz | 12 | 2.806 | 0.333 | 1.919 | 0.083 |
| 600.000 | radial_0.05 | 12 | 3.635 | 0.333 | 9.824 | 0 |
| 1000.000 | tangential_1.0 | 12 | 4.216 | 0.333 | -0.729 | 0.167 |
| 600.000 | tang_1.0_vz | 12 | 4.599 | 0.333 | 1.026 | 0.083 |
| 500.000 | tangential_1.0 | 12 | 1.009 | 0.250 | -0.337 | 0.083 |
| 800.000 | tang_1.0_vz | 12 | 1.717 | 0.250 | 4.220 | 0 |
| 700.000 | tang_1.0_vz | 12 | 4.186 | 0.250 | 1.756 | 0.083 |
| 800.000 | radial_0.05 | 12 | 8.400 | 0.250 | 14.166 | 0.167 |
| 0.000 | tang_1.0_vz | 12 | -1.204 | 0.167 | -0.001 | 0 |
| 400.000 | tang_1.0_vz | 12 | 0.589 | 0.167 | 1.388 | 0 |
| 1000.000 | radial_1.0 | 12 | 2.530 | 0.167 | 1.300 | 0 |

## Worst individual softR-vs-fixed cases

| distance_m | condition | index | fixed_rmse_m | hop_rmse_m | softR_rmse_m | softR_gain_vs_fixed_m | softR_gain_vs_hop_m |
|---:|---|---|---:|---:|---:|---:|---:|
| 0.000 | radial_1.0 | 10 | 0.228 | 13.542 | 13.542 | -13.314 | 0.000 |
| 0.000 | tang_1.0_vz | 1 | 0.321 | 13.514 | 13.514 | -13.193 | 0.000 |
| 1000.000 | tangential_1.0 | 5 | 35.343 | 15.255 | 47.902 | -12.559 | -32.647 |
| 300.000 | tang_1.0_vz | 3 | 2.141 | 8.926 | 8.926 | -6.785 | 0.000 |
| 900.000 | radial_1.0 | 4 | 14.450 | 24.411 | 21.193 | -6.743 | 3.218 |
| 400.000 | tang_1.0_vz | 8 | 6.263 | 12.693 | 12.704 | -6.441 | -0.011 |
| 700.000 | radial_1.0 | 9 | 6.160 | 12.418 | 12.418 | -6.258 | -0.001 |
| 700.000 | tangential_1.0 | 9 | 6.042 | 11.975 | 11.975 | -5.934 | 0.000 |
| 900.000 | tangential_1.0 | 1 | 4.011 | 6.000 | 9.406 | -5.395 | -3.406 |
| 700.000 | radial_1.0 | 0 | 8.806 | 13.439 | 13.439 | -4.633 | -0.000 |
| 1000.000 | tangential_1.0 | 8 | 40.476 | 45.026 | 45.026 | -4.550 | 0.000 |
| 500.000 | tangential_1.0 | 1 | 7.067 | 11.394 | 11.394 | -4.326 | 0.000 |
| 700.000 | radial_1.0 | 3 | 9.973 | 14.238 | 14.238 | -4.265 | 0.000 |
| 800.000 | radial_0.05 | 6 | 16.975 | 21.186 | 21.186 | -4.211 | 0.000 |
| 1000.000 | tang_1.0_vz | 0 | 11.124 | 14.982 | 14.982 | -3.858 | 0.000 |

## Interpretation

- The remaining 13.1% softR-vs-fixed tail is not uniformly distributed.
- Most distance-averaged gains remain positive, but tail risk concentrates in a few distance/motion cells.
- The moving-target claim should therefore keep both statements: mean/P90 improvement is strong, but residual tail cases remain and motivate future risk-aware scheduling or additional guards.
