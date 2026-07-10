# 95. Fig5 PNG and submission packaging

## Purpose

This folder closes the remaining figure-packaging gap identified in folders 91 and 94:

- Fig. 5 previously existed only as SVG.
- A Word-first or professor-review workflow usually needs PNG figures.

The folder also gathers the current manuscript-facing Fig. 1--6 set into one package.

## Outputs

- `generate_fig5_png.py`
- `figures/fig1_system_concept.{png,svg}`
- `figures/fig2_frequency_agile_bias.{png,svg}`
- `figures/fig3_static_600m_paired_rmse.{png,svg}`
- `figures/fig4_moving_whitening_lag1.{png,svg}`
- `figures/fig5_quasi_static_speed_boundary.{png,svg}`
- `figures/fig6_crlb_floor.{png,svg}`
- `figure_package_manifest.md`
- `submission_readiness_check.md`

## Fig. 5 generation

`generate_fig5_png.py` reads the authoritative folder-82 result JSON:

```text
82. 준정지 속도 경계 검증 실행/results/quasi_static_boundary.json
```

and regenerates Fig. 5 as both PNG and SVG.

The x-axis uses categorical spacing for the tested speed conditions. This is intentional: the purpose is to show the non-monotonic operating boundary cleanly, not to imply a continuous speed-response curve.

## Decision

The figure package is now usable for manuscript v3 professor review. The remaining blockers are not figure availability but citation closure and journal-specific formatting.

