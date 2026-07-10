# Default decisions while professor is away

## D1. Paper axis

Default decision:

> Keep the paper axis as static/quasi-static long-range USBL coherent DOA-bias whitening.

Reason:

- Static 600 m is the strongest result: 13.01 m to 8.87 m, p = 0.0008.
- Moving-target RMSE improvement is not validated.
- The novelty defense is now literature-aware and no longer overclaims frequency hopping itself.

## D2. Claim boundary

Default decision:

> Conservative claim boundary: static long-range targets and very slow drift up to 0.005 m/s.

Reason:

- 0.010 and 0.050 m/s are not supported.
- 0.030 and 0.100 m/s positive results are non-continuous and geometry-dependent.

## D3. Target-journal working assumption

Default decision:

> Prepare the manuscript first for a reproducibility-friendly sensors / sensor-fusion style journal.

Reason:

- The present work is simulation/signal-level and code-audited.
- The paper has strong measurement design, sensor fusion, and positioning/navigation content.
- A more acoustics-specialist or IEEE/OES target may require stronger field validation or a tighter ocean-engineering framing.

## D4. Real-water validation

Default decision:

> Do not block manuscript preparation on real-water validation.

Reason:

- Field validation may become a later upgrade path.
- Current work can still be prepared as a reproducible mechanism and simulation-validation paper.

Reversal condition:

- If the selected target journal requires field or experimental validation, switch to a real-water validation plan before submission.

## D5. Next work priority

Default decision:

1. Prepare a target-journal neutral manuscript package.
2. Complete full-text semantic citation audit when library access is available.
3. Convert to target journal format after choosing the target.
4. Prepare real-water plan as a parallel future-work package, not as a blocker.

## D6. Do-not-cross lines

Do not write:

- "first frequency-hopped USBL,"
- "moving target localization improvement,"
- "quasi-static validated to 0.100 m/s,"
- "sub-meter long-range performance,"
- "field validated."

