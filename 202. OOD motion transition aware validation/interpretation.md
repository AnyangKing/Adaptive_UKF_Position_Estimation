# Interpretation

## Bottom line

The first-pass OOD motion probe is cautiously positive.

Transition-aware soft-R did not collapse under unseen motion patterns. On the 12-case mid/long-range OOD subset:

- fixed mean RMSE: 12.333 m
- plain hop mean RMSE: 10.720 m
- transition-aware soft-R mean RMSE: 8.351 m
- softR vs hop mean gain: 2.369 m
- softR vs hop Wilcoxon p: 0.038
- softR divergence fraction: 0.000

However, this is not a full robustness proof. The sample size is small, and tail worsening still appears in some 1000 m / mixed-motion cases.

## What this supports

This folder supports a limited statement:

> A first-pass OOD motion probe did not reveal immediate collapse of the transition-aware Adaptive-R rule; the method retained a mean gain over plain hopping on representative curved, accelerating, mixed, and vertical maneuver cases.

## What this does not support

This folder does not support:

- claiming OOD robustness over all motion classes,
- claiming real-water performance,
- replacing the 191 full-range independent moving validation,
- retuning the method based on the OOD subset.

## Important details

### Positive signs

1. Overall mean RMSE improved over both fixed and plain hop.
2. The divergence fraction dropped from 0.083 for fixed/hop to 0.000 for softR.
3. The largest OOD benefit appeared in the vertical_sine condition:
   - fixed: 21.059 m
   - hop: 17.340 m
   - softR: 10.039 m
   - softR gain vs hop: 7.301 m

### Boundary signs

1. At 1000 m, softR gain vs hop was small:
   - hop: 8.715 m
   - softR: 8.431 m
   - gain: 0.283 m
   - tail worsened fraction vs hop: 0.250
2. In mixed_radial_tangential motion, softR gain vs hop was also small:
   - hop: 7.565 m
   - softR: 7.453 m
   - gain: 0.112 m
   - tail worsened fraction vs hop: 0.333

These boundary signs are important. The method should be described as improving the tested OOD subset on average, not as a universally safe moving-target solution.

## Manuscript implication

The OOD result can be used as a supplementary robustness probe, not as a main headline result.

Safe wording:

> In a small OOD motion probe, transition-aware Adaptive-R retained a mean advantage over plain hopping, while also revealing residual tail-risk at the longest range and mixed-motion conditions.

Unsafe wording:

> The proposed method is robust to arbitrary target maneuvers.

## Next step

The next useful validation is a larger OOD run with:

- more seeds per OOD condition,
- 0--1000 m every 100 m,
- separate reporting of radial/cross-range/vertical errors,
- focused tail inspection at 1000 m and mixed radial+tangential motion.

If that larger OOD validation remains positive, the moving-target claim becomes substantially stronger.
