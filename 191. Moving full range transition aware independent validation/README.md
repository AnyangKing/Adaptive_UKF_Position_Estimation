# Moving full-range transition-aware independent validation

## Purpose

Folder 190 showed a promising low-n moving-target distance diagnostic. This folder repeats the full 0--1000 m moving-target sweep with a larger independent seed set.

## Protocol

- distances: 0, 100, 200, ..., 1000 m
- moving conditions:
  - radial 0.05 m/s
  - radial 1.0 m/s
  - tangential 1.0 m/s
  - tangential 1.0 m/s with vertical 0.08 m/s
- geometries per distance/condition: 12
- total paired cases: 528
- policies:
  - fixed baseline
  - plain carrier hop
  - frozen folder-181 transition-aware softR

## Independence

This validation uses new seed roots:

- geometry seed root: 1,910,000
- ping/channel seed root: 1,913,000

The folder-181 transition-aware rule is frozen:

- `range_jump_threshold_m = 0.5`
- `max_toa_scale = 100`
- no ground-truth inputs to runtime decisions

## Claim boundary

If successful, this folder can support a manuscript claim that the transition-aware Adaptive-R rule improves moving-target full-range simulation performance under the current signal-level channel.

It still does not replace:

- real-water validation,
- rough-surface/ray-model validation,
- transducer frequency-response calibration,
- final journal-level robustness over broader environments.

