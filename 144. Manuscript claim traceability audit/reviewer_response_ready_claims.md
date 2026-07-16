# Reviewer-response ready claim wording

## Static performance claim

Safe:

> In independent 600 m static trials, the frozen 30--34 kHz ping-to-ping schedule reduced settled RMSE from 13.01 m under fixed 32 kHz transmission to 8.87 m, corresponding to a paired improvement of 4.14 m (p=0.0008).

Avoid:

> Frequency agility generally improves all USBL tracking cases.

Reason: moving target pooled RMSE gain was not significant.

## Moving target boundary

Safe:

> For moving targets, carrier agility strongly decorrelated the elevation residuals, but this whitening did not produce a statistically reliable pooled RMSE gain in the current always-on schedule.

Avoid:

> The proposed carrier-agile method improves moving-target RMSE.

Reason: 63번 결과는 lag-1 whitening positive, RMSE gain non-significant.

## Quasi-static claim

Safe:

> Under the present protocol, continuous quasi-static support is validated only up to 0.005 m/s; higher-speed positives were non-monotonic and geometry-dependent.

Avoid:

> The method is validated for quasi-static targets up to 0.100 m/s.

Reason: 0.010 and 0.050 m/s break the continuous boundary.

## Novelty claim

Safe:

> The contribution is not frequency hopping itself, but its application as a carrier-agile whitening mechanism for post-gating coherent multipath DOA bias in compact shallow-water USBL localization, together with the associated boundary analysis.

Avoid:

> We are the first to use frequency hopping to reduce glint-like error.

Reason: pulse-to-pulse frequency agility/glint decorrelation exists in radar literature.

## Long-range limitation claim

Safe:

> The 600 m residual error is consistent with a systematic-bias floor above the empirical CRLB-scale bound, rather than only with filter suboptimality.

Avoid:

> A better Kalman filter alone should reach sub-meter accuracy at 600 m.

Reason: 45번 CRLB/floor and 43--46 estimator comparisons show the dominant limitation is measurement/bias physics under compact aperture.

## Two-ray mechanism claim

Current safe version before 135:

> The two-ray phase model explains the observed carrier-dependent bias curves in selected representative geometries; the exact example-fit statistics should be tied to a reproducible figure-generation artifact before submission.

Post-135 desired version:

> The representative 400 m and 600 m geometries yielded two-ray fit statistics of R²=... with image-source excess delays of ... ms, as reproduced by `135/results/two_ray_fit.json`.
