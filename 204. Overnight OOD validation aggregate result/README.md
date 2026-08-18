# 204. Overnight OOD validation aggregate result

## Purpose

Folder 203 provided the checkpoint/resume runner. This folder records the first completed full overnight OOD validation aggregate.

The per-case checkpoint files remain local in:

```text
203. Overnight OOD validation runner/overnight_results/
```

This folder stores only compact aggregate artifacts so the result is easy to review and commit.

## Completed run

- paired OOD cases: 528 / 528
- policy rows: 1584
- distances: 0, 100, 200, ..., 1000 m
- OOD conditions:
  - accelerating radial
  - curved arc
  - mixed radial+tangential
  - vertical sine maneuver
- geoms per distance/condition: 12
- failed case files: 0
- runtime: about 7728 s, approximately 2 h 9 min

## Main result

| policy | mean RMSE | median RMSE | P90 RMSE | divergence |
|---|---:|---:|---:|---:|
| fixed baseline | 10.832 m | 8.198 m | 22.339 m | 0.049 |
| plain hop | 10.691 m | 7.565 m | 21.611 m | 0.057 |
| transition-aware soft-R | 7.809 m | 6.478 m | 15.936 m | 0.006 |

Pairwise:

- softR vs hop: mean gain 2.881 m, p=9.076e-22, tail worsened 0.036.
- softR vs fixed: mean gain 3.023 m, p=1.015e-18, tail worsened 0.152.
- hop vs fixed: mean gain 0.141 m, but tail worsened 0.242.

## Interpretation

This is stronger than folder 202. The small OOD probe suggested that transition-aware soft-R did not collapse; this 528-case run supports a much stronger statement that the method retained an average OOD benefit across the tested distances and motion classes.

Still, this remains signal-level simulation, not real-water validation.
