# Precommit verification

Verification run for folder 101 before committing.

## Generated files

- `figures/fig1_system_concept_polished.png`
- `figures/fig1_system_concept_polished.svg`

## Visual checks

- Panel (a) shows the USBL array, target, sea surface, seafloor, direct path, surface-reflected path, compact aperture, and 5 ms DOA gate.
- Panel (b) shows the mechanism distinction between fixed 32 kHz and 30--34 kHz agile pings.
- The right-side estimator block explicitly says the receiver remains the same: TOA/TDOA/DOA to adaptive-R UKF.
- The bottom note prevents overclaiming: the novelty is not frequency hopping itself.
- The figure avoids claiming moving-target RMSE improvement.

## Known caveat

This figure is a polished conceptual schematic, not a scale drawing. It should be used to explain the mechanism, while quantitative results remain in Figs. 2--6.

## Commit scope rule

Only `101. Fig1 visual polish/` should be staged for this commit.
