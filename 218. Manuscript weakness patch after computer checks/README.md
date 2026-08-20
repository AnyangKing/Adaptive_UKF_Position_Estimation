# 218. Manuscript weakness patch after computer checks

## Purpose

This folder records the manuscript update after the computer-checkable weakness patches in folders 215--217.

The actual manuscript files under `paper/` were edited locally only and are not committed, following the project rule.

## What changed in the local manuscripts

- Added 215 hardware-response mismatch sensitivity as a supplementary robustness check.
- Added 216 extended OOD motion-family validation as additional OOD-family evidence.
- Kept the claim boundary strict:
  - no real-water validation claim;
  - no measured hardware calibration claim;
  - no arbitrary moving-target guarantee;
  - no claim that plain hopping alone solves moving tracking.
- Updated Supplementary Material/Data Availability wording to map 215/216 into the supplement plan.

## Files

- `manuscript_patch_summary.md`
- `build_check.md`

## Decision

The manuscript should now describe 215 and 216 as supporting robustness checks, not as new primary claims.
