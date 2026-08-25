# softR filter consistency validation

## Headline

- Position NEES is a 3-dof consistency diagnostic. Ideal mean is approximately 3; values far above 3 indicate overconfidence and values far below 3 indicate underconfidence.
- Total NIS is a 10-dof measurement consistency diagnostic for TOA + 7 TDOA + 2 DOA. Ideal mean is approximately 10.
- This is a diagnostic rerun of the 191 moving-target protocol, not a new algorithm.

## Overall policy metrics

| policy | RMSE m | div. | pos NEES | pos NEES P90 | pos NEES > chi2-99 | total NIS | total NIS P90 | total NIS > chi2-99 | n |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fixed_baseline | 12.186 | 0.072 | 207.71 | 465.26 | 0.197 | 23.41 | 62.26 | 0.119 | 528 |
| hop_baseline | 11.337 | 0.072 | 255.84 | 557.20 | 0.195 | 23.02 | 61.19 | 0.119 | 528 |
| hop_transition_softR | 7.389 | 0.004 | 16.00 | 41.43 | 0.083 | 3.65 | 9.07 | 0.038 | 528 |

## Paired RMSE comparisons

| comparison | mean gain m | 95% CI | Wilcoxon p | improved frac | tail worsened | n |
|---|---:|---:|---:|---:|---:|---:|
| softR_vs_hop | 3.948 | [2.882, 5.137] | 1.585e-22 | 0.409 | 0.028 | 528 |
| softR_vs_fixed | 4.797 | [3.800, 5.847] | 1.671e-30 | 0.693 | 0.131 | 528 |
| hop_vs_fixed | 0.849 | [-0.027, 1.661] | 1.336e-07 | 0.593 | 0.214 | 528 |

## softR consistency by distance

| distance m | softR gain vs hop m | tail worsened | softR pos NEES | softR total NIS | n |
|---:|---:|---:|---:|---:|---:|
| 0 | -0.000 | 0.000 | 23.50 | 1.02 | 48 |
| 100 | 0.075 | 0.000 | 0.88 | 0.31 | 48 |
| 200 | 4.833 | 0.000 | 35.25 | 5.68 | 48 |
| 300 | 4.245 | 0.000 | 25.27 | 4.66 | 48 |
| 400 | 4.292 | 0.021 | 21.50 | 5.65 | 48 |
| 500 | 4.960 | 0.021 | 13.85 | 4.52 | 48 |
| 600 | 4.872 | 0.021 | 14.95 | 4.59 | 48 |
| 700 | 3.483 | 0.104 | 16.50 | 2.55 | 48 |
| 800 | 11.557 | 0.042 | 12.33 | 4.01 | 48 |
| 900 | 4.379 | 0.062 | 5.36 | 3.43 | 48 |
| 1000 | 0.730 | 0.042 | 9.27 | 2.83 | 48 |

## Interpretation boundary

This folder answers whether the current transition-aware softR result has a covariance-consistency warning flag under the same simulation protocol. It does not claim real-water consistency, hardware response validation, or arbitrary moving-target generalization.

## Interpretation

The diagnostic result is useful but not a free victory. The transition-aware softR policy preserves the main moving-target performance result: mean RMSE improves from 11.337 m to 7.389 m against the hopping baseline, divergence drops from 7.2% to 0.4%, and the paired Wilcoxon result remains strongly significant.

For consistency, softR is clearly less overconfident than the two baselines in position NEES:

- fixed baseline: mean position NEES 207.71
- hop baseline: mean position NEES 255.84
- transition-aware softR: mean position NEES 16.00

However, ideal 3D position NEES is approximately 3, so softR should not be described as statistically calibrated. The correct manuscript-level statement is that softR substantially reduces overconfidence and innovation-tail exposure, but residual covariance miscalibration remains.

Total NIS tells the complementary story. The two baselines have mean total NIS near 23, above the 10-dof nominal mean, while softR has mean total NIS 3.65. This means the final inflated measurement covariance used by softR is conservative at the measurement-update level. That conservatism is likely part of why divergence is suppressed, but it is also why the method should be presented as a robust adaptive covariance inflation rule rather than a fully calibrated Bayesian filter.

## Manuscript action

If this result is reflected in the manuscript, use a restrained sentence:

> A consistency audit under the same moving-target protocol showed that transition-aware softR reduced position NEES from 255.84 to 16.00 relative to the hopping baseline and lowered the chi2-99 NIS exceedance fraction from 0.119 to 0.038, while remaining imperfectly calibrated relative to the nominal 3-dof NEES target.

Do not claim that softR makes the UKF covariance statistically calibrated.
