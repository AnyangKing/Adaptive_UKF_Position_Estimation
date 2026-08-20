# 216. Extended OOD motion family validation

## Purpose

This folder addresses the manuscript weakness:

> Moving-target validation covers tested motion families, not arbitrary moving targets.

Folder 204 already tested four OOD families over 0--1000 m. This folder adds four different OOD motion families as a compact extension.

## Added motion families

- `stop_go`: stationary/slow segment followed by motion onset and deceleration.
- `direction_reversal`: tangential motion reverses direction mid-track.
- `spiral_climb`: rotating horizontal direction with vertical drift.
- `burst_turn`: mostly moderate motion with a short high-speed maneuver.

## Protocol

- distances: 0, 200, 400, 600, 800, 1000 m;
- seeds: 6 per distance/family;
- total paired cases: 144;
- policies: fixed carrier, plain hopping, transition-aware soft-R;
- same signal-level TOA/TDOA/DOA extraction and UKF logic as folder 191.

## Claim boundary

This folder expands the tested OOD motion set. It still does not prove arbitrary moving-target robustness.

Use:

> additional OOD-family simulation evidence

Avoid:

> arbitrary moving target validation
