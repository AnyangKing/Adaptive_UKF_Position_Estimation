# Structure audit

## Current section structure

| Order | Section | Audit |
|---:|---|---|
| 1 | Introduction | Good. Starts from the user's original TOA/TDOA/DOA + Kalman-filter question and narrows to the residual-bias problem. |
| 2 | Related Work and Problem Statement | Good. Related work is not just a literature dump; it defines the novelty boundary. |
| 3 | System Model and UKF Fusion | Good. Establishes observation vector and fixed estimator before proposing carrier agility. |
| 4 | Baseline Tracking Performance | Good. Shows why receiver/filter-only approaches are insufficient. |
| 5 | Proposed Carrier-Agile Whitening Method | Strong. Mechanism is now the paper's center. The two-ray model and schedule justification belong here. |
| 6 | Experimental Validation and Applicability Boundary | Strong. Separates static positive claim from moving/quasi-static boundary. |
| 7 | Discussion | Good. States deployment implication and limitations without overclaiming. |
| 8 | Conclusion | Good. Repeats the bounded claim and future work. |
| 9 | Supplementary/Data/Acknowledgment | Acceptable placeholder stage. Needs author/journal decisions later. |

## Figure/table inventory

Current manuscript has 7 figure files and 6 manuscript tables.

Figures:

1. `fig1_system_concept.png` — concept
2. `fig6_crlb_floor.png` — CRLB/floor
3. `fig_tworay_fit.png` — two-ray fit
4. `fig2_frequency_agile_bias.png` — carrier sensitivity
5. `fig3_static_600m_paired_rmse.png` — static validation
6. `fig4_moving_whitening_lag1.png` — moving boundary
7. `fig5_quasi_static_speed_boundary.png` — quasi-static boundary

Tables:

1. `tab:priorart`
2. `tab:estimators`
3. `tab:routing`
4. `tab:crlb`
5. `tab:results`
6. `tab:quasi`
7. `tab:limitations`

Note: there are seven table-like labeled tables, not six, if `tab:limitations` is counted. The earlier 136 count of "6 tables" missed the limitations table. This is a minor manifest wording correction to remember in a later manifest update.

## IEEE-style fit

The section order is consistent with many IEEE engineering papers:

- Introduction and prior art before model.
- Model before baseline and proposed method.
- Proposed method before experiments.
- Experiments before discussion/conclusion.
- Limitations near the end.

The 12-page length is acceptable for a journal-style IEEE draft. It is not too short anymore. If anything, the risk has shifted from “too little content” to “too many floats in a narrow two-column layout,” which final visual QA should check.

## Float-order risks

### R1. File numbering differs from manuscript order

`fig6_crlb_floor.png` appears before `fig2_frequency_agile_bias.png` in the manuscript flow. This is not a LaTeX problem because captions/labels control figure numbering, but it can confuse humans looking at the `paper/figures/` folder.

Mitigation:

- In supplement manifest, refer to manuscript labels, not only filenames.
- If final journal package allows renaming, consider neutral names such as `fig_floor.png`, `fig_bias.png`, etc.

### R2. Double-column tables may float away

`tab:priorart`, `tab:results`, and `tab:limitations` use `table*`. IEEEtran places double-column floats at page tops, sometimes away from first mention.

Mitigation:

- Final visual QA should check that each table appears within a reasonable distance from its first textual reference.
- If a table drifts too far, move its LaTeX block earlier/later rather than forcing `[H]`-style placement.

### R3. Data Availability figure range is too narrow

The current Data Availability wording says scripts underlying `Figs. concept--floor`, which can be read as excluding static/moving/quasi/two-ray figures depending on label order.

Mitigation:

- Replace with “all figures and tables” or list the numbered source-data manifest.

### R4. Two-ray PNG generation path remains less formal than the JSON/SVG closure

145번 closed the claim with JSON and SVG. The final PNG in `paper/figures/fig_tworay_fit.png` should eventually be regenerated from the 145 data or documented as a conversion artifact.

Mitigation:

- Either convert `135/results/two_ray_fit.svg` to the final PNG, or add a short note in the supplement that `fig_tworay_fit.png` is a rendered version of the 135 SVG.
