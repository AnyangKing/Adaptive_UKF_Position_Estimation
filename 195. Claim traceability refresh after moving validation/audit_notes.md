# Audit notes

## Checks performed

Searched the Korean and English manuscripts for:

- headline static numbers: 13.01, 8.87, 4.14, 0.0008;
- moving numbers: 528, 3.95, 4.80, 1.59e-22, 1.67e-30;
- quasi-static boundary: 0.005, 11.98, 10.49;
- risk phrases: real-water, first use, post-hoc, plain hopping, 162, 191.

## Findings

1. Static claim remained unchanged and still maps to 61.
2. Moving claim now maps to 191 and is worded as simulation-level transition-aware Adaptive-R.
3. Plain hopping failure remains visible and is not overwritten.
4. Korean and English manuscripts both forbid real-water/arbitrary-motion generalization.
5. 162 remains described as post-hoc/pilot and is not used as final performance evidence.
6. The moving p-value is summarized as `p<10^-21` in abstracts and reported exactly in the body.

## Minor risk to watch later

The manuscript now has more figures/tables and remains 13 pages in IEEEtran.  
196 should check whether the extra moving figure creates float congestion or excessive length.

