# 202. OOD motion transition-aware validation

## Purpose

Folder 191 validated transition-aware Adaptive-R on structured moving cases:

- radial 0.05 m/s,
- radial 1.0 m/s,
- tangential 1.0 m/s,
- tangential 1.0 m/s with vertical 0.08 m/s.

This folder tests a first-pass out-of-distribution (OOD) motion set. The goal is not to create a new headline result, but to check whether the 191 moving-target claim collapses under motion patterns that were not used in the main validation.

## OOD motion cases

- accelerating radial motion,
- curved arc motion,
- mixed radial+tangential motion,
- vertical sinusoidal maneuver.

## Protocol

- distances: 400, 800, 1000 m
- OOD conditions: 4
- geometries per distance/condition: 1
- total paired OOD cases: 12
- policies:
  - fixed carrier baseline
  - plain carrier hopping baseline
  - canonical transition-aware soft-R from folder 191

## Claim boundary

This is a first-pass OOD probe, not a full robustness proof. It can show whether there is an immediate OOD failure signal in representative mid/long-range conditions. If it is positive, a larger independent OOD validation should follow.

## Result summary

The 12-case first-pass OOD probe was cautiously positive:

| policy | mean RMSE | P90 RMSE | divergence |
|---|---:|---:|---:|
| fixed baseline | 12.333 m | 15.884 m | 0.083 |
| plain hop | 10.720 m | 13.077 m | 0.083 |
| transition-aware soft-R | 8.351 m | 11.040 m | 0.000 |

Comparison:

- softR vs hop: mean gain 2.369 m, p=0.038, improved fraction 0.667, tail worsened 0.083.
- softR vs fixed: mean gain 3.982 m, p=0.301, improved fraction 0.667, tail worsened 0.250.

Interpretation:

> The method did not immediately collapse under unseen motion patterns, but the subset is too small for a full OOD robustness claim. Residual tail-risk remains at 1000 m and mixed radial+tangential motion.
