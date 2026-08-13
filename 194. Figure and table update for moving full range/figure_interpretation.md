# Figure interpretation

## fig7_moving_full_range_rmse

Shows distance-wise mean settled RMSE for:

- fixed 32 kHz;
- plain 30--34 kHz hopping;
- transition-aware soft-R.

The key visual message is not simply that hopping helps.  
At 800 m, plain hopping is worse than fixed, while transition-aware soft-R recovers the tail.

## fig8_moving_full_range_gain_tail

Shows:

- soft-R gain vs fixed;
- soft-R gain vs hop;
- soft-R tail-worsened fraction vs hop.

This figure supports the wording that transition-aware routing reduces the moving-tail problem but does not make tail risk exactly zero.

## Recommended manuscript use

- Use `fig7` as the main moving validation figure.
- Use `fig8` if space allows, or keep it for supplementary material.
- Keep `tab:movingfull` in the manuscript as exact numerical backing.

