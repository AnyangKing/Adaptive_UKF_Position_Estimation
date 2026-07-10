# Cover letter bullets

These bullets are intentionally conservative. They frame the work as a bounded mechanism-and-validation paper, not as a first-ever frequency-hopping paper.

## One-sentence summary

This manuscript shows that ping-to-ping carrier agility can whiten a carrier-locked, post-gating coherent multipath DOA bias in compact shallow-water USBL localization, improving independent static 600 m TOA/TDOA/DOA-UKF tracking while exposing a clear moving-target boundary.

## Main contribution bullets

- The study reframes a long-range compact USBL localization floor as a post-gating coherent DOA-bias problem, not merely as a Kalman-filter tuning problem.
- A mechanism-level phase model explains why direct and in-gate surface-reflected arrivals can create carrier-locked elevation bias under fixed-frequency transmission.
- A frozen 30--34 kHz ping-to-ping carrier schedule reduced independent static 600 m settled RMSE from 13.01 m to 8.87 m, corresponding to a 32% reduction with p = 0.0008.
- Moving-target experiments confirmed residual whitening but did not show reliable pooled RMSE improvement, preventing overclaiming and defining the method's current applicability boundary.
- A quasi-static sweep supports continuous use only up to 0.005 m/s under the present compact-array, shallow-water protocol.

## Novelty wording

Recommended:

> The novelty is not frequency hopping itself, but the identification, validation, and boundary analysis of carrier-agile whitening for post-gating coherent multipath DOA bias in a TOA/TDOA/DOA-UKF USBL tracking loop.

Avoid:

> This is the first frequency-hopping USBL localization method.

Avoid:

> The proposed method enables sub-meter long-range USBL accuracy.

## Reviewer-risk preemption

- We explicitly cite radar frequency-agility/glint work and prior underwater frequency-diverse positioning.
- We separate static performance improvement from moving-target mechanism evidence.
- We report negative moving-target RMSE results and non-monotonic quasi-static speed behavior instead of hiding them.
- We keep the method simulation-based and call for lake/sea validation before broad deployment claims.
