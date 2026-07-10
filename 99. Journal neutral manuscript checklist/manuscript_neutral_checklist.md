# Journal-neutral manuscript checklist

## A. Scientific claim gates

| Gate | Status | Evidence |
|---|---|---|
| Main claim is static/quasi-static, not general moving-target tracking | PASS | Abstract and Results retain moving-target RMSE boundary. |
| Static 600 m result remains primary | PASS | 13.01 m to 8.87 m, p = 0.0008 in v4-ref. |
| Moving RMSE improvement is not claimed | PASS | Moving result reports -0.10 m, p = 0.301. |
| Quasi-static continuous boundary is 0.005 m/s | PASS | v4-ref and Fig.5 package both state 0.005 m/s. |
| Frequency hopping itself is not claimed as new | PASS | Table 1 and Introduction cite prior FH/Costas/frequency-comb work. |
| Sub-meter long-range claim is absent | PASS | Discussion keeps compact-aperture floor. |

## B. Manuscript completeness gates

| Gate | Status | Evidence |
|---|---|---|
| Abstract exists | PASS | v4-ref has Abstract. |
| Introduction + contribution statement exist | PASS | v4-ref Section 1. |
| Method equations exist | PASS | v4-ref Section 2. |
| Implementation details exist | PASS | v4-ref Section 2.1. |
| Mechanism section exists | PASS | v4-ref Section 4. |
| Static validation exists | PASS | v4-ref Section 6. |
| Moving/quasi-static boundary exists | PASS | v4-ref Section 7. |
| Discussion and conclusion exist | PASS | v4-ref Sections 8--9. |
| Tables exist | PASS | Table 1--3 in v4-ref. |
| Figure captions exist | PASS | Fig.1--6 captions in v4-ref. |
| References exist | PASS | Metadata-closed references in v4-ref. |

## C. Packaging gates

| Gate | Status | Evidence |
|---|---|---|
| Main placeholder citations removed | PASS | Search count = 0 for four major placeholders. |
| Fig.1--6 PNG available | PASS | folder 95 has 6 PNG files. |
| Fig.1--6 SVG available | PASS | folder 95 has 6 SVG files. |
| Fig.5 PNG available | PASS | generated from folder-82 JSON in folder 95. |
| Legacy Fig.7 active callout removed | PASS | only legacy filename note remains. |
| Markdown-only formatting still present | OPEN | Math fences and markdown tables must be converted for final template. |
| Equation numbering | OPEN | Not yet assigned. |
| Journal-specific reference style | OPEN | BibTeX/metadata ready but not final style. |

## D. Submission-readiness rating

Current rating:

> Scientifically assembled, not yet journal-formatted.

Meaning:

- The paper can now be read as a complete draft.
- The next work is editorial/formatting/full-text audit, not core algorithm discovery.

