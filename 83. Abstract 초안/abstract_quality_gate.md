# Abstract quality gate

Before using the abstract in a manuscript, check every item below.

## Claim scope

- [x] Does it say the strongest performance result is static 600 m?
- [x] Does it avoid claiming general moving-target RMSE improvement?
- [x] Does it restrict quasi-static wording to very slow drift, 0.005 m/s under the current protocol?
- [x] Does it avoid saying 0.100 m/s is a validated continuous boundary?

## Novelty safety

- [x] Does it avoid “first frequency hopping USBL”?
- [x] Does it frame radar frequency agility and USBL frequency-hopping work as prior art?
- [x] Does it define novelty as mechanism + validation + boundary?

## Numerical consistency

- [x] Static 600 m: 13.01 m to 8.87 m
- [x] Static improvement: -32%, p = 0.0008
- [x] Static median: 13.97 m to 7.96 m
- [x] Moving lag-1: +0.470 to -0.208, p = 5.6e-10
- [x] Moving pooled RMSE: not reliable, -0.10 m, p = 0.301
- [x] 82번 quasi-static: continuous boundary 0.005 m/s

## Recommended abstract choice

Use Version C from `abstract_draft.md` as the baseline if the target is SCI review resilience. Use Version A if the journal has a shorter abstract limit and the related-work section can absorb the prior-art nuance.

## Red-flag phrases to remove

- “first frequency-hopping USBL”
- “moving-target improvement”
- “sub-meter long-range localization”
- “quasi-static up to 0.100 m/s”
- “Kalman filter solves the multipath problem”

## Good phrases to keep

- “post-gating coherent multipath DOA bias”
- “carrier-locked residual”
- “ping-to-ping carrier agility”
- “static long-range validation”
- “motion-induced self-whitening”
- “non-monotonic, geometry-dependent boundary”
