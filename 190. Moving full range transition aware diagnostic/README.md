# Moving full-range transition-aware diagnostic

## Purpose

The static target already has a 0--1000 m diagnostic sweep in folder 184. The next practical question is whether the moving-target recovery found in folder 181 at 600 m survives across range.

This folder applies the frozen folder-181 transition-aware Adaptive-R rule to moving targets at:

`0, 100, 200, ..., 1000 m`

with the same four moving conditions used in folder 181.

## Scope

This is a distance diagnostic, not a final validation grid.

- distances: 0--1000 m in 100 m steps
- moving conditions: radial 0.05 m/s, radial 1.0 m/s, tangential 1.0 m/s, tangential 1.0 m/s + vertical 0.08 m/s
- geometries per distance/condition: 3
- policies: fixed baseline, hop baseline, hop-transition softR

## Claim boundary

Allowed:

> The transition-aware Adaptive-R rule is or is not promising across the moving-target range map.

Forbidden:

> Moving-target 0--1000 m performance is finally validated.

If this diagnostic is positive, the next step is a larger independent validation with at least n=12 or n=20 per distance/condition.

