# Manuscript figure callout fix

## Current issue

The project history used `fig7_crlb_floor` because an earlier figure plan reserved Fig. 7 for the CRLB/floor plot. Later, the manuscript skeleton moved related-work positioning into Table 1 and shifted the CRLB/floor discussion to Fig. 6.

Therefore, there is a mismatch:

- old generated filename: `fig7_crlb_floor.*`
- manuscript v1 callout: Fig. 6

## Decision

Use Fig. 6 for CRLB/floor in the manuscript.

Reason:

- Fig. 1: system/mechanism concept
- Fig. 2: carrier-sensitive bias
- Fig. 3: static validation
- Fig. 4: moving whitening boundary
- Fig. 5: quasi-static speed boundary
- Fig. 6: CRLB / compact-aperture floor

Use Table 1, not Fig. 7, for related-work differentiation unless a later manuscript version needs an additional positioning diagram.

## Required v2 edits

In manuscript v2:

1. Replace every future/path reference to `fig7_crlb_floor` with `fig6_crlb_floor`.
2. Keep textual callouts as `Fig. 6`.
3. Ensure the figure list and file manifest use the canonical files in `91. Figure file alignment/figures/`.
4. If a related-work figure is later added, number it Fig. 7 only after all six current figures are stable.

