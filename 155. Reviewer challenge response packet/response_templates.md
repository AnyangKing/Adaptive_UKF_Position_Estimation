# Reviewer response templates

## R1. “Frequency agility is not new.”

**Response**

We agree that pulse-to-pulse frequency agility and frequency diversity are established concepts.
Accordingly, the manuscript does not claim frequency hopping itself as novel. The contribution is
the identification and validation of carrier-locked, post-gating coherent-multipath DOA bias in a
compact shallow-water USBL chain, and the use of carrier agility to whiten that bias within a
TOA/TDOA/DOA-UKF localization framework while explicitly reporting its static and moving-target
boundaries.

## R2. “The study lacks real-water validation.”

**Response**

We agree and have limited the claims to simulation and signal-level evidence. The current work is
intended to establish the mechanism, statistical static benefit, and operating boundary before
field deployment. Tank/lake/sea validation, including frequency-dependent transducer calibration,
is identified as required future validation and is not represented as completed.

## R3. “Why is there no moving-target RMSE gain?”

**Response**

The moving-target experiment shows statistically strong residual decorrelation but no reliable
pooled RMSE gain for the always-on schedule. We retain this negative result because motion already
provides partial geometric self-whitening and because geometry-dependent tails prevent the
whitening gain from translating uniformly into position RMSE. The manuscript therefore restricts
the performance claim to static and continuously quasi-static conditions.

## R4. “Why 30–34 kHz and 20 carriers?”

**Response**

The schedule is frozen before independent validation and is used as a simple mechanism probe over
the empirically favorable band. We do not claim it is optimal. A preregistered schedule ablation
covering bandwidth, carrier count, order, and sparse schedules is retained as follow-up work.

## R5. “The two-ray fit is overfit.”

**Response**

The oscillation period is not estimated from the bias curve. It is fixed by the image-source excess
delay computed from geometry; only the offset and first-harmonic sine/cosine coefficients are
estimated. The displayed geometries also satisfy the carrier-grid resolution criterion, and the
source JSON, generator, and final PNG are hash- and pixel-traceable.

## R6. “A better filter could solve this.”

**Response**

The estimator comparison and empirical CRLB-scale analysis separate filter efficiency from the
measurement-bias floor. The remaining long-range error is consistent with coherent DOA bias
amplified by compact aperture, so filter replacement alone does not support a sub-meter claim at
600 m under the modeled conditions.

## R9. “Hardware and environmental effects are missing.”

**Response**

The current sensitivity study includes sound-speed and synchronization mismatch, but it does not
replace measured transducer, array, and environmental calibration. We state this limitation
explicitly and require frequency-dependent calibration plus contemporaneous environmental logging
in the field-validation protocol.

## R10. “Where are the data and code?”

**Response**

The project has a content-addressed 91-artifact supplement plan, exact figure lineage, and a
seven-case executable smoke matrix. The final repository/DOI and public-release scope must be
selected by the authors; no public DOI is claimed before that decision.
