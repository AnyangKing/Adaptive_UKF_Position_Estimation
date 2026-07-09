# 91. Figure file alignment

## Purpose

This folder creates a manuscript-facing figure set from the existing source folders.

The important correction is that the CRLB/floor figure was originally generated as `fig7_crlb_floor` in folder 70, while manuscript v1 calls it Fig. 6. In this folder it is renamed to the manuscript numbering:

- source: `70. 논문 그림 1차 생성/figures/fig7_crlb_floor.*`
- manuscript canonical name: `fig6_crlb_floor.*`

## Canonical figure set

| Manuscript figure | Canonical file(s) | Source folder | Status |
|---|---|---|---|
| Fig. 1 | `figures/fig1_system_concept.svg`, `figures/fig1_system_concept.png` | 72 | Available |
| Fig. 2 | `figures/fig2_frequency_agile_bias.svg`, `figures/fig2_frequency_agile_bias.png` | 70 | Available |
| Fig. 3 | `figures/fig3_static_600m_paired_rmse.svg`, `figures/fig3_static_600m_paired_rmse.png` | 70 | Available |
| Fig. 4 | `figures/fig4_moving_whitening_lag1.svg`, `figures/fig4_moving_whitening_lag1.png` | 70 | Available |
| Fig. 5 | `figures/fig5_quasi_static_speed_boundary.svg` | 82 | SVG available; PNG still needed for Word-first workflow |
| Fig. 6 | `figures/fig6_crlb_floor.svg`, `figures/fig6_crlb_floor.png` | 70 | Available after renaming from original `fig7_crlb_floor` |

## Manuscript implication

In manuscript v2:

- keep CRLB/floor callout as Fig. 6,
- do not refer to a separate Fig. 7 unless a new related-work positioning figure is created,
- use Table 1 for related-work positioning instead of Fig. 7 unless page space permits an extra figure.

## Next action

The next folder can integrate these figures and the 90번 tables into a clean manuscript v2.

