# 201. Transition-aware Adaptive-R sensitivity validation

## Purpose

Folder 191 showed that the frozen transition-aware Adaptive-R rule improved moving-target 0--1000 m performance. This folder tests whether that result is fragile to the two rule parameters:

- observed TOA range-jump threshold,
- maximum TOA covariance inflation cap.

This is not a new algorithm search. It is a sensitivity validation of the already adopted folder-191 rule.

## Protocol

Inherited from folder 191:

- distances: 0, 200, 400, 600, 800, 1000 m
- moving conditions:
  - radial 0.05 m/s
  - radial 1.0 m/s
  - tangential 1.0 m/s
  - tangential 1.0 m/s with vertical 0.08 m/s
- geometries per distance/condition: 1 representative seed from the folder-191 seed set
- total paired cases per variant: 24
- same geometry, channel, and noise seeds as folder 191
- fixed and plain-hop baselines are read from folder-191 result JSON

Sensitivity grid:

| parameter | values |
|---|---|
| `range_jump_threshold_m` | 0.25, 0.5, 1.0 |
| `max_toa_scale` | 25, 100, 400 |

The canonical folder-191 setting is:

- `range_jump_threshold_m = 0.5`
- `max_toa_scale = 100`

## Claim boundary

This folder is a first-pass subset sensitivity diagnostic. It can identify whether the 191 rule appears extremely brittle, but it cannot by itself replace the full 528-case folder-191 validation, OOD motion validation, environmental sensitivity validation, or real-water validation.

## Result summary

The 24-case first-pass subset did not show obvious threshold/cap brittleness.

- All nine tested settings improved over plain hopping on the subset.
- Gain vs plain hop: 7.171--7.269 m.
- Gain vs fixed: 3.242--3.339 m.
- Tail worsened vs hop: 0.000 for all tested settings.
- Canonical folder-191 setting `0.5/100`: mean RMSE 6.986 m, gain vs hop 7.205 m, gain vs fixed 3.276 m.

Interpretation:

> The transition-aware Adaptive-R benefit is not obviously confined to the exact `0.5/100` parameter pair, but this subset is not large enough to retune the method or replace the full 191 validation.
