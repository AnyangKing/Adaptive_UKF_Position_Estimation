# Supplement package v3 manifest

## Scope

This manifest is the current paper-facing supplementary-material plan for the Adaptive UKF / carrier-agile USBL manuscript.

It supports the following limited manuscript line:

> A signal-level USBL simulation study shows that carrier-agile observation design changes coherent multipath-induced DOA bias behavior; plain hopping is useful for diagnosis and static/quasi-static improvement, while transition-aware soft-R routing is the supported moving-target estimator under the tested 0--1000 m and OOD simulation conditions.

It does not support:

- real-water performance;
- arbitrary hardware frequency response robustness;
- arbitrary-motion guarantees outside tested OOD families;
- a claim that frequency hopping alone solves moving-target tracking;
- a claim that TOA/TDOA/DOA + UKF is novel by itself.

## Proposed archive layout

```text
supplement_adaptive_ukf_carrier_agile_usbl_v3/
  README.md
  data/
    static_600m_validation.json
    moving_boundary_validation.json
    quasi_static_boundary_validation.json
    moving_full_range_validation.json
    ood_moving_validation_compact_metrics.json
    crlb_floor.json
    two_ray_fit.json
    method_facts.json
  code/
    45_crlb_floor/
    58_carrier_sensitivity/
    61_static_validation/
    63_moving_boundary/
    82_quasi_static_boundary/
    93_method_code_audit/
    145_two_ray_closure/
    191_moving_full_range_validation/
    194_moving_full_range_figures/
    204_ood_aggregate_result/
  figures/
    fig1_system_concept.png
    fig2_frequency_agile_bias.png
    fig3_static_600m_paired_rmse.png
    fig4_moving_whitening_lag1.png
    fig5_quasi_static_speed_boundary.png
    fig6_crlb_floor.png
    fig7_moving_full_range_rmse.png
    fig8_moving_full_range_gain_tail.png
    fig_tworay_fit.png
  figure_scripts/
    generate_core_figures.py
    make_moving_full_range_figures.py
    reproduce_tworay_fit.py
  docs/
    claim_to_artifact_matrix.md
    figure_source_manifest.md
    table_source_manifest.md
    submission_package_policy.md
    source_data_manifest_204.md
```

## Claim-to-artifact map

| Manuscript claim | Primary artifact | Support level | Boundary |
|---|---|---|---|
| Static 600 m carrier-agile schedule reduces RMSE relative to fixed carrier | `61. ...` result files and summaries | Main static validation | Static simulation only |
| Plain hopping decorrelates moving residuals but does not reliably improve moving RMSE | `63. ...` plus failure series 64--67 | Mechanism and negative boundary | Not a proposed moving estimator |
| Quasi-static benefit collapses by the tested 0.005 m/s boundary | `82. ...` | Boundary result | Does not claim broad moving robustness |
| Transition-aware soft-R improves structured moving validation over 0--1000 m | `191. ...` and `194. ...` | Main moving validation | Structured simulated motion only |
| Transition-aware soft-R retains OOD aggregate advantage | `204. ...` and `209. ...` | OOD simulation evidence | OOD families tested only |
| Two-ray model explains carrier-locked coherent bias qualitatively/quantitatively within the simplified model | `145. ...`, `fig_tworay_fit.png` | Mechanism support | Not a full ocean acoustic model |
| Method parameters and protocol statements match code | `93. ...`, `175. ...`, `176. ...` | Audit support | Only for the adopted simulator/code path |

## Figure-source map

| Figure | Current file | Source folder |
|---|---|---|
| Fig. 1 | `paper/figures/fig1_system_concept.png` | 101 / paper figure asset |
| Fig. 2 | `paper/figures/fig2_frequency_agile_bias.png` | 58 / core figure scripts |
| Fig. 3 | `paper/figures/fig3_static_600m_paired_rmse.png` | 61 / core figure scripts |
| Fig. 4 | `paper/figures/fig4_moving_whitening_lag1.png` | 63 / core figure scripts |
| Fig. 5 | `paper/figures/fig5_quasi_static_speed_boundary.png` | 82 / 95 |
| Fig. 6 | `paper/figures/fig6_crlb_floor.png` | 45 / core figure scripts |
| Fig. 7 | `paper/figures/fig7_moving_full_range_rmse.png` | 191 / 194 |
| Fig. 8 | `paper/figures/fig8_moving_full_range_gain_tail.png` | 191 / 194 |
| Two-ray supplemental figure | `paper/figures/fig_tworay_fit.png` | 145 |

## Exclusion policy

Do not include in the submitted supplement unless deliberately approved later:

- `paper/manuscript.tex`, `paper/manuscript_ko.tex`, PDFs, `.aux`, `.bbl`, `.log`, or LaTeX build products;
- raw checkpoint-heavy overnight runner outputs from folder 203;
- root-level handoff, professor-report, review-summary, or project-management MD files;
- `.git/`, `.claude/`, `study_exports/`, caches, and local editor state;
- any file whose result is post-hoc/pilot-only and not used as a manuscript claim.

## Current packaging status

Ready as a design manifest. Actual ZIP assembly should wait until:

1. author/journal requirements are known;
2. the final manuscript table/figure numbering is stable;
3. the user explicitly approves copying or packaging release files.
