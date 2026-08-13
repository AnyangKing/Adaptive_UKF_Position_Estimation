# Local manuscript changes

## Edited local-only file

- `paper/manuscript_ko.tex`

## Reason

The Korean baseline manuscript still represented the moving-target result as a negative boundary only.  
After 191, that wording became outdated because the frozen transition-aware Adaptive-R rule passed an independent 0--1000 m moving-target validation.

## Important distinction

The manuscript was not changed to claim that carrier hopping alone solves moving USBL tracking.  
It was changed to claim that transition-aware Adaptive-R, using runtime-observable risk indicators, recovers the moving-target tail problem created by plain hopping under the current simulator.

## Not committed

`paper/` remains local-only according to the project rule. The actual TeX edit is intentionally not staged or pushed.

