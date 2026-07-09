# Reviewer risk and response map

## Risk 1 — “Frequency agility is old”

Likely reviewer point:

> Frequency agility and frequency hopping have long been used in radar/sonar, and USBL frequency-hopped signals already exist.

Response:

Agree and narrow the novelty.

Safe response sentence:

> We do not claim frequency hopping itself as new. The contribution is the identification of a post-gating carrier-locked coherent multipath DOA-bias mechanism in compact shallow-water USBL, and the validation that ping-to-ping carrier agility whitens this residual within a TOA/TDOA/DOA-UKF tracking loop.

Need citations:

- radar glint/frequency agility
- JASA 2007 frequency-hopped acoustic modem USBL
- IEEE 2022 Costas hopping USBL

## Risk 2 — “Why not just use a better filter?”

Likely reviewer point:

> The improvement may be a filter tuning artifact.

Response:

State that the filter and carrier schedule were frozen, and that the method changes the measurement residual before fusion.

Safe response sentence:

> The receiver-side estimator is intentionally kept fixed; the performance change comes from altering the temporal structure of the DOA residual through transmit carrier agility.

Evidence:

- 61 independent validation
- 83 quality gate
- 37--57 failed blind correction routes

## Risk 3 — “Does this solve moving-target localization?”

Likely reviewer point:

> The paper title or abstract may imply moving target improvement.

Response:

Do not imply that. Present moving results as boundary.

Safe response sentence:

> Moving trajectories confirm residual whitening but not a reliable pooled RMSE gain, which we attribute to motion-induced self-whitening and geometry-dependent tail risk.

Evidence:

- 63: lag-1 whitening, RMSE gain not significant
- 64--67: schedule safety attempts not reproduced
- 82: non-monotonic slow-drift boundary

## Risk 4 — “Quasi-static up to 0.100 m/s?”

Likely reviewer point:

> If 0.100 m/s is positive, why is the boundary 0.005 m/s?

Response:

Because the result is not monotonic. A continuous boundary requires every lower tested speed to pass.

Safe response sentence:

> Although 0.030 and 0.100 m/s showed positive aggregate results, 0.010 and 0.050 m/s did not; therefore, we report only 0.005 m/s as the continuous validated slow-drift regime and treat later positive cases as geometry-dependent recoveries.

Evidence:

- 82 speed table

## Risk 5 — “Why are errors still meters?”

Likely reviewer point:

> If the method works, why is 600 m RMSE still 8.87 m?

Response:

Because frequency agility reduces one coherent bias component, not the aperture/geometry limit.

Safe response sentence:

> Carrier agility mitigates the carrier-locked component of the residual but does not change the angular resolution imposed by the compact array aperture.

Evidence:

- 45/79 CRLB/floor analysis
- 56/57 subgrid/ping-count limits

## Risk 6 — “Simulation-only”

Likely reviewer point:

> The result needs tank or field validation.

Response:

Agree and frame as future work, while emphasizing preregistered/frozen-schedule simulation validation.

Safe response sentence:

> The present work establishes the mechanism and simulation-scale validation under a controlled shallow-water channel; field/tank validation and hardware schedule constraints are the next required step.

## Risk 7 — “Was the carrier schedule tuned after seeing results?”

Likely reviewer point:

> The 30--34 kHz schedule may be overfit.

Response:

State frozen policy and independent seeds.

Safe response sentence:

> The 30--34 kHz schedule was fixed before the independent validation runs; the reported static result uses new geometry/seed sequences.

Evidence:

- 61 README/protocol
- 82 protocol/result summary

## Risk 8 — “Why call it UKF if the novelty is transmit design?”

Likely reviewer point:

> The paper title/abstract may confuse estimator contribution with signal design.

Response:

Make the role clear:

> The UKF is the tracking loop into which TOA/TDOA/DOA observations are fused; the proposed contribution is the transmit-side design that changes the residual statistics seen by that loop.
