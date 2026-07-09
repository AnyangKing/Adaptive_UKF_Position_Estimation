# Claim consistency check

## Abstract vs body

| Claim | Abstract | Body | Status |
|---|---|---|---|
| Main application is static long-range USBL | yes | Sections 6, 9 | consistent |
| Frequency hopping itself is not claimed as new | yes | Sections 1, 8 | consistent |
| Static 600 m RMSE 13.01 -> 8.87 m | yes | Section 6 | consistent |
| Moving residual whitening but no reliable RMSE gain | yes | Section 7 | consistent |
| Quasi-static continuous boundary only 0.005 m/s | yes | Section 7 | consistent |
| 0.100 m/s not claimed as boundary | yes | Section 7 | consistent |

## Risk phrases avoided

- first frequency-hopping USBL: avoided
- general moving target improvement: avoided
- sub-meter long-range positioning: avoided
- all multipath solved: avoided
- UKF is the main novelty: avoided

## Current weakest points

1. Citation placeholders remain.
2. System/model section is still high-level.
3. No figure references inserted in body.
4. Some numbers are cited from project summaries and should be rechecked against source JSON before submission.

## Strongest current points

1. Claim boundary is honest and consistent.
2. Positive and negative results are both included.
3. Novelty is defensible against frequency-hopping prior art.
4. The paper now has a coherent story from original TOA/TDOA/DOA-UKF idea to final frequency-agile observation design.
