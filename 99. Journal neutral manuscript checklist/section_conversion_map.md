# Section conversion map

This map helps convert the current v4-ref manuscript into different journal structures without changing the scientific claim.

## Current v4-ref structure

1. Abstract
2. Introduction
3. System and Signal Model
4. Post-Gating DOA Bias Floor
5. Carrier-Sensitive Coherent Interference Mechanism
6. Frequency-Agile Whitening Method
7. Static Validation
8. Whitening Evidence and Applicability Boundary
9. Discussion
10. Conclusion
11. Figure Captions
12. Figure File Manifest
13. References

## Sensors-style structure

| Target section | Source material |
|---|---|
| Abstract | Abstract |
| Introduction | Section 1 + Table 1 |
| Materials and Methods / System Model | Sections 2, 5 |
| Mechanism / Observation Design | Section 4 |
| Experiments and Validation | Sections 3, 6, 7 |
| Results | Sections 6, 7 + Table 2 |
| Discussion | Section 8 + Table 3 |
| Conclusions | Section 9 |

Notes:

- Emphasize sensor fusion, observation design, reproducibility, and multi-sensor positioning.
- Keep implementation details because Sensors values reproducibility.

## Applied Acoustics-style structure

| Target section | Source material |
|---|---|
| Abstract | Abstract |
| Introduction | Section 1 |
| Acoustic scenario and signal model | Sections 2, 4 |
| Method | Section 5 + adaptive-R details |
| Numerical validation | Sections 3, 6, 7 |
| Discussion | Section 8 |
| Conclusions | Section 9 |

Notes:

- Emphasize underwater acoustics, gated surface reflection, coherent interference, and acoustic signal processing.
- Be careful: the journal may expect experimental validation. The current work must be framed as numerical/signal-level validation unless field data is added.

## IEEE/OES-style structure

| Target section | Source material |
|---|---|
| Introduction | Section 1 |
| System Model | Section 2 |
| Multipath Bias Mechanism | Sections 3, 4 |
| Carrier-Agile Observation Design | Section 5 |
| Validation | Sections 6, 7 |
| Discussion | Section 8 |
| Conclusion | Section 9 |

Notes:

- Strong fit for underwater localization but likely higher expectation for field relevance.
- Use as stretch target or post-field-validation target.

