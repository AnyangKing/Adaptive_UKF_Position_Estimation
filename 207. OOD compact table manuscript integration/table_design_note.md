# OOD table design note

## Why a table was added

204 is now important enough that burying it in a paragraph makes the moving-target claim harder to audit. A small table lets readers see that the gain is not only a mean-RMSE effect:

- mean RMSE improves,
- P90 improves,
- divergence improves.

## Why no new figure was added

The existing Fig.7 already visualizes the structured 191 distance sweep. Adding a second OOD figure without a dedicated OOD plot script would risk creating a figure whose source lineage is less clean. For now, the OOD result is safer as an aggregate table backed by 204 result files.

## Claim boundary

The table caption explicitly says:

- simulation-level robustness evidence,
- not real-water proof,
- not arbitrary-motion proof.
