# Supplement package v4 manifest

## Scope

Supplement package v4 is the current source-package plan after the computer-checkable weakness patches.

It adds the following evidence to the v3 plan:

- `215. Hardware frequency response sensitivity`: idealized carrier-dependent response mismatch sensitivity.
- `216. Extended OOD motion family validation`: additional OOD motion-family validation.

## Proposed package layout

```text
supplement_adaptive_ukf_carrier_agile_usbl_v4/
  README.md
  data/
    static_600m_validation.*
    quasi_static_boundary.*
    moving_full_range_validation.*
    ood_moving_validation_204.*
    hardware_response_sensitivity_215.*
    extended_ood_motion_family_216.*
    two_ray_fit.*
  code/
    selected_reproduction_scripts/
  figures/
    manuscript_figure_source_pngs/
  docs/
    claim_to_artifact_matrix.md
    source_data_manifest.md
    limitation_and_exclusion_policy.md
```

## New claim mapping

| Added weakness | Folder | What it supports | What it does not support |
|---|---|---|---|
| Hardware response mismatch | 215 | Soft-R robustness under idealized 3/6 dB edge-loss profiles | Measured hardware response validation |
| Moving-family coverage | 216 | Additional OOD-family simulation evidence | Arbitrary moving-target proof |

## Release boundary

This dry run intentionally does not create a ZIP. Final release should wait for:

1. journal/repository choice;
2. anonymization requirements;
3. user/professor approval;
4. final manuscript figure/table numbering.
