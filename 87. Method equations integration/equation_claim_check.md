# Equation claim check

## Checked claims

| Equation block | Risk | Status |
|---|---|---|
| TOA/TDOA/DOA observation model | might imply ideal observations only | acceptable if followed by residual/noise statement |
| constant-velocity UKF model | might look like main novelty | explicitly framed as backbone |
| adaptive-R rule | might overstate method novelty | explicitly framed as stable fusion wrapper |
| `phi = 2*pi*f*delta + theta_r` | might look like complete multipath model | marked as mechanism-level explanation |
| moving `delta(t)` | might imply moving performance guarantee | used only to explain self-whitening boundary |
| 30--34 kHz schedule | might imply optimized universal schedule | stated as frozen validation schedule, not global optimum |

## Required caution sentences

Use these in v1:

> The phase expression is not used as a full reflected-path estimator; it is used to explain why a carrier-locked residual can become temporally decorrelated under carrier-agile transmission.

> The UKF and adaptive-R routing form the tracking backbone, whereas the proposed contribution is the transmit-side observation design that changes the residual statistics entering that backbone.

> The same phase model also predicts an applicability boundary: target motion changes `delta(t)`, so fixed-carrier transmission can already experience motion-induced self-whitening.

## Do not claim

- We estimate and subtract the multipath phase directly.
- The phase model fully explains all DOA errors.
- Carrier agility removes the aperture limit.
- The UKF is a new filter.
- The method guarantees moving-target RMSE improvement.
