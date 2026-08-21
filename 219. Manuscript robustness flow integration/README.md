# 219. Manuscript robustness flow integration

## Purpose

Integrate folders 215 and 216 into the manuscript flow without turning them into primary claims.

The actual `paper/` manuscript files were edited locally only and are not committed.

## What changed locally

- Added 215 and 216 as supplementary rows in the English compact results table.
- Added matching supplementary rows in the Korean reading draft table.
- Kept the abstract unchanged because 215/216 are robustness checks, not the main story.

## Why this is safer

The manuscript body already mentioned the new checks. Without table rows, the checks looked like late discussion-only additions. The table rows make their role explicit:

- 215 = supplementary sensitivity, not measured hardware calibration.
- 216 = supplementary robustness evidence, not arbitrary-motion proof.

## Files

- `flow_integration_audit.md`
- `build_check.md`
