# Figure and table map

## Figure 1 — system and mechanism concept

Source folder:

- 72

Purpose:

- Show compact USBL array, direct path, in-gate surface reflection, and carrier-sensitive interference phase.

Claim supported:

- The problem is not only filtering; it is a physical observation residual entering the filter.

## Figure 2 — bias versus carrier frequency

Source folder:

- 58

Purpose:

- Show that elevation bias changes with carrier frequency at long range.

Claim supported:

- The residual has a carrier-sensitive coherent component.

## Figure 3 — static 600 m validation

Source folder:

- 61, 76

Recommended visualization:

- paired fixed vs hop RMSE points
- mean/median markers
- p-value and -32% label

Claim supported:

- The method reproducibly improves static long-range performance.

## Figure 4 — residual whitening evidence

Source folder:

- 63

Recommended visualization:

- lag-1 residual correlation fixed vs hop
- possibly residual time-series examples

Claim supported:

- Frequency agility changes the temporal residual structure even when RMSE gain is not general.

## Figure 5 — moving/quasi-static boundary

Source folders:

- 63, 82

Recommended visualization:

- speed on x-axis
- mean RMSE gain and decision labels
- mark 0.005 m/s continuous boundary
- mark 0.010 and 0.050 not supported

Claim supported:

- Applicability is non-monotonic and geometry-dependent beyond very slow drift.

## Figure 6 — post-gating bias floor / CRLB relation

Source folders:

- 45, 79

Purpose:

- Show that long-range performance is near a floor and not sub-meter.

Claim supported:

- Frequency agility mitigates one residual component but does not erase aperture/geometry limits.

## Figure 7 — related-work positioning diagram or table

Source folder:

- 78

Purpose:

- Distinguish radar frequency agility, frequency-hopped USBL, Costas USBL, and our coherent DOA-bias whitening claim.

Alternative:

- Use as Table 1 rather than a figure.

## Table 1 — contribution and prior-art differentiation

Columns:

1. Prior work family
2. Uses frequency diversity?
3. USBL positioning?
4. Addresses post-gating coherent DOA bias?
5. Integrated with TOA/TDOA/DOA-UKF tracking?
6. Static/moving boundary quantified?

Purpose:

- Reviewer defense against “frequency agility is old”.

## Table 2 — numerical results summary

Rows:

- static 600 m fixed/hop
- static median
- moving lag-1 whitening
- moving pooled RMSE
- quasi-static 0.005 m/s
- quasi-static non-supported speeds
- CRLB/floor

Purpose:

- Prevent overclaiming by putting positive and negative results together.

## Table 3 — limitation and future-work map

Rows:

- exact citation audit
- real-water validation
- carrier schedule ablation
- motion/geometry-aware schedule
- array aperture scaling

Purpose:

- Show intellectual honesty and clear next research path.
