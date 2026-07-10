# Figure and table insertion plan

## Canonical figure source

Use the figure package from:

`95. Fig5 PNG and submission packaging/figures/`

For Word/professor review, insert PNG first. Keep SVG files for vector conversion or journal upload if the target supports SVG/EPS/PDF conversion.

## Figure placement

| Figure | Preferred placement | Purpose | Final check |
|---|---|---|---|
| Fig. 1 | End of Section 2 or early Section 4 | System geometry and in-gate reflection mechanism | Concept figure may still need visual polish before final submission. |
| Fig. 2 | Section 4 | Carrier sensitivity of long-range elevation bias | Caption must avoid claiming first-ever frequency hopping. |
| Fig. 3 | Section 6 | Main static 600 m RMSE result | This is the strongest performance figure. |
| Fig. 4 | Section 7 | Moving-target whitening without RMSE gain | Caption must clearly say mechanism claim, not moving-target localization improvement. |
| Fig. 5 | Section 7 | Quasi-static speed boundary | Use folder-95 PNG/SVG; categorical spacing is intentional. |
| Fig. 6 | Section 3 or Discussion | Compact-aperture floor / CRLB-scale comparison | Helps explain why sub-meter 600 m claims are not made. |

## Table placement

| Table | Preferred placement | Role | Conversion risk |
|---|---|---|---|
| Table 1 | Introduction / Related Work | Novelty boundary against prior frequency-diverse work | Wide; may need smaller font or split in Word. |
| Table 2 | End of Section 7 | Positive and negative validation summary | Wide and dense; may become two tables if the journal dislikes large tables. |
| Table 3 | Discussion or Supplement | Limitations and follow-up work | Optional; can be compressed to prose under page limits. |

## Conversion rule

Do not leave the `Figure File Manifest` section inside the final manuscript body. During target-specific conversion:

1. Keep the six figure captions.
2. Insert actual figure callouts according to the table above.
3. Move the manifest to a submission checklist or supplementary packaging note.
4. Verify that every figure number is cited in order.

## Current unresolved visual item

Fig. 1 is still described as a concept draft. Before final submission, run one visual-polish pass or replace it with a cleaner schematic generated from the same geometry.
