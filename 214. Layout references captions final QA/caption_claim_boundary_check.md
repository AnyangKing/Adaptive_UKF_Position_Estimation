# Caption and claim-boundary check

## Checked principle

Each major figure/table caption should say both:

1. what the artifact supports; and
2. what it does not support.

This prevents accidental over-claiming through captions.

## Current status

| Artifact | Boundary status |
|---|---|
| System concept figure | Correctly descriptive; not used as performance evidence. |
| CRLB/floor figure | Explicitly avoids sub-meter or full-bias-removal claims. |
| Two-ray figure | Explicitly states simplified mechanism, not a full ocean channel model. |
| Carrier sensitivity figure | Shows carrier-locked bias, not direct RMSE improvement. |
| Static 600 m figure | Claims static simulation improvement only. |
| Moving residual figure | Claims decorrelation and failure boundary, not pooled RMSE improvement. |
| Moving full-range figure/table | Claims simulation-level transition-aware soft-R improvement over 0--1000 m only. |
| OOD summary table | Claims tested OOD-family simulation robustness only. |
| Quasi-static figure/table | Keeps continuous safe boundary at 0.005 m/s and avoids broad speed generalization. |
| Failure/limitation table | Keeps failed pilots out of performance claims. |

## Result

No caption currently appears to exceed the evidence boundary established in the latest experiment folders.

The most important protected boundary remains:

> Frequency agility by itself is not presented as a general moving-target solution; the supported moving-target method is transition-aware Adaptive-R/soft-R routing under the tested simulation conditions.
