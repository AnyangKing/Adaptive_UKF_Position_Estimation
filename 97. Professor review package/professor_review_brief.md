# Professor review brief

## Working title

Carrier-Agile Whitening of Coherent Multipath DOA Bias in Static Shallow-Water USBL Tracking

## One-sentence thesis

In compact shallow-water USBL tracking, a carrier-locked coherent multipath component can remain after direct-path gating and bias DOA estimates; ping-to-ping carrier agility whitens this residual and improves static long-range localization, while moving-target improvement remains limited by motion-induced self-whitening and tail risk.

## Starting idea

The project began with a simple estimator idea:

> Fuse TOA, TDOA, and DOA measurements with a Kalman-family filter to estimate underwater position.

The filter backbone settled on a conditional adaptive-R UKF because the observation model is nonlinear and the measurement quality changes with signal consistency.

## What changed during the research

Early work showed that better filtering alone did not remove the long-range error floor. The dominant remaining error was a small but systematic DOA/elevation bias amplified by compact aperture at long range.

The key discovery was that a large part of the long-range bias was carrier-sensitive:

```math
\phi = 2\pi f \delta + \theta_r
```

When the source is static, `\delta` is nearly fixed, so a fixed carrier can lock the interference phase. A carrier-agile schedule changes `f` ping by ping and turns part of that deterministic bias into a whitened residual.

## Main positive result

Static 600 m validation:

- fixed 32 kHz mean settled RMSE: 13.01 m,
- 30--34 kHz carrier-agile mean settled RMSE: 8.87 m,
- improvement: +4.14 m,
- p = 0.0008,
- median: 13.97 m to 7.96 m.

This is the main performance claim.

## Main boundary result

Moving target:

- elevation residual lag-1 correlation: +0.470 to -0.208,
- p = 5.56e-10,
- pooled moving RMSE gain: -0.10 m,
- p = 0.301.

Interpretation:

Carrier agility whitens the residual, but moving-target localization improvement is not validated. The likely reason is that target motion already changes `\delta(t)`, producing motion-induced self-whitening under a fixed carrier.

## Quasi-static boundary

The conservative continuous quasi-static boundary is 0.005 m/s.

Positive results at 0.030 and 0.100 m/s are not claimed as a continuous speed boundary because 0.010 and 0.050 m/s were not supported. They are treated as geometry-dependent recoveries.

## Novelty framing

Not claimed:

- first frequency hopping,
- first frequency-hopped USBL,
- first radar-like frequency agility concept,
- moving-target RMSE improvement.

Claimed:

- carrier-agile whitening of post-gating coherent multipath DOA bias in compact shallow-water USBL tracking,
- integration with TOA/TDOA/DOA-UKF tracking,
- independent static long-range validation,
- explicit moving/quasi-static applicability boundary including negative results.

## Current manuscript state

The strongest current manuscript file is:

`96. Citation placeholder closure/manuscript_draft_v4_refs.md`

It includes:

- tables,
- figure captions,
- method details aligned to code,
- reference placeholders replaced with metadata-verified references.

## Remaining work before submission

1. Professor approval of paper axis and target journal.
2. Full-text semantic audit of the cited prior work through library/publisher access.
3. Journal template formatting.
4. Equation numbering and reference style.
5. Optional real-water validation plan if the professor wants stronger applied evidence before submission.

