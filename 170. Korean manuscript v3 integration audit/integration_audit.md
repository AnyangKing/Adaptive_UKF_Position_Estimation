# Integration audit details

## Claim-boundary matrix

| Manuscript area | Audit finding | Status |
|---|---|---|
| Abstract | Static 600 m improvement is stated with 13.01 m -> 8.87 m, 4.14 m paired improvement, p = 0.0008. Moving target is stated as whitening without pooled RMSE gain. | Pass |
| Introduction | The research pivot is framed as filter improvement -> observation-error structure design. No first-ever frequency-hopping USBL claim is made. | Pass |
| Claim table | The table explicitly lists allowed and disallowed claims. | Pass |
| Basic performance/limit section | The long-range floor is described as linked to post-gating coherent multipath DOA bias, not fully solved. | Pass |
| Proposed method | Carrier-agile pinging is presented as observation design on top of the same TOA/TDOA/DOA-UKF loop. | Pass |
| Static validation | Static 600 m remains the central performance evidence. | Pass |
| Moving validation | The manuscript says residual whitening is observed but pooled RMSE gain is not reproduced. | Pass |
| Quasi-static validation | The continuous safe boundary remains 0.005 m/s. | Pass |
| Discussion | Folders 160--162 are treated as schedule-design limitation/future-work evidence. | Pass |
| Conclusion | The final claim is narrowed to reducing temporal correlation of carrier-locked coherent multipath DOA bias. | Pass |

## Reference and figure checks

Labels:

- `fig:bias`
- `fig:floor`
- `fig:moving`
- `fig:quasistatic`
- `fig:static`
- `fig:system`
- `fig:tworay`
- `tab:claims`
- `tab:limitations`
- `tab:validation`

References:

- `tab:claims`
- `fig:static`
- `tab:claims`
- `tab:validation`

Missing references: none.

Figure files checked:

- `paper/figures/fig1_system_concept.png`
- `paper/figures/fig6_crlb_floor.png`
- `paper/figures/fig_tworay_fit.png`
- `paper/figures/fig2_frequency_agile_bias.png`
- `paper/figures/fig3_static_600m_paired_rmse.png`
- `paper/figures/fig4_moving_whitening_lag1.png`
- `paper/figures/fig5_quasi_static_speed_boundary.png`

Missing figure files: none.

## Build check

Fresh build was attempted but did not reach LaTeX compilation. MiKTeX returned:

`It seems that this is a fresh TeX installation. Please finish the setup before proceeding.`

Interpretation:

- The current machine's MiKTeX setup needs initialization or repair.
- This audit cannot claim a fresh PDF build.
- The manuscript source audit still passes.
- Build-environment repair should be a separate task if the user wants it.

## No paper patch needed

No local `paper/manuscript_ko.tex` patch was made in this folder because the
claim audit found no manuscript-level contradiction requiring a text change.
