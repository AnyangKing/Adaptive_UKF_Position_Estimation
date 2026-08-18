# Interpretation

## Bottom line

The full overnight OOD validation is positive.

Across 528 paired OOD cases, transition-aware soft-R improved the mean RMSE and reduced divergence relative to both fixed and plain-hop baselines.

Most importantly, plain hopping alone remained risky:

- hop vs fixed mean gain: 0.141 m
- hop vs fixed tail worsened fraction: 0.242

Transition-aware soft-R changed that profile:

- softR vs hop mean gain: 2.881 m
- softR vs hop p-value: 9.076e-22
- softR vs hop tail worsened fraction: 0.036
- softR divergence: 0.006

This supports the core story that frequency agility alone is not the moving-target solution; the filter must respond to carrier-transition-induced observation risk.

## Distance-wise reading

The result is not uniform in every range bin, which is good to preserve honestly.

| distance | softR gain vs hop | tail worse vs hop |
|---:|---:|---:|
| 0 m | 0.000 | 0.000 |
| 100 m | 0.180 | 0.000 |
| 200 m | 2.501 | 0.000 |
| 300 m | 6.727 | 0.021 |
| 400 m | 4.619 | 0.021 |
| 500 m | 5.396 | 0.062 |
| 600 m | 3.590 | 0.062 |
| 700 m | 3.089 | 0.083 |
| 800 m | 2.568 | 0.042 |
| 900 m | 0.643 | 0.062 |
| 1000 m | 2.382 | 0.042 |

The 900 m gain is small compared with neighboring distances. This should be treated as a boundary/heterogeneity signal, not hidden.

## Condition-wise reading

| condition | softR gain vs hop | tail worse vs hop |
|---|---:|---:|
| accelerating_radial | 2.247 | 0.030 |
| curved_arc | 2.556 | 0.068 |
| mixed_radial_tangential | 2.254 | 0.023 |
| vertical_sine | 4.468 | 0.023 |

The vertical sine maneuver showed the largest gain. Mixed radial+tangential did not collapse in the full run, unlike the small 202 subset where it looked more fragile.

## Safe manuscript claim

Safe:

> In a 528-case OOD motion validation over 0--1000 m, transition-aware Adaptive-R retained a significant mean advantage over plain hopping while reducing the divergence rate and limiting tail degradation.

Also safe:

> Plain carrier hopping alone produced only a small mean gain over fixed carrier and a substantial tail-worsening fraction, supporting the need for filter-side transition-aware covariance routing.

Unsafe:

> The proposed method is universally robust to arbitrary target maneuvers.

Unsafe:

> This proves real-water OOD performance.

## What should happen next

The next useful step is to update manuscript/root claim documents with this result, but only after deciding whether to treat this as:

1. a main OOD validation result, or
2. a supplement robustness result supporting the main 191 moving full-range validation.

My recommendation: use it as a strong supplementary robustness result first. If the manuscript needs a larger moving-target evidence block, promote it into the main Results section.
