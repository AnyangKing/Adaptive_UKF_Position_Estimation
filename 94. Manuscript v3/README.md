# 94. Manuscript v3

## Purpose

This folder applies the folder-93 code-audit patches to the folder-92 manuscript v2.

The goal is to move the manuscript from "integrated draft" to "method-consistent draft" by making Section 2 and the validation protocol match the committed code and result JSON.

## Outputs

- `manuscript_draft_v3.md`
- `v3_change_log.md`
- `v3_quality_check.md`
- `next_submission_tasks.md`

## Main changes

1. Replaced the oversimplified binary adaptive-R equation with the actual two-stage rule:
   - continuous GCC/SRP disagreement scale,
   - block-wise NIS inflation for TOA, TDOA, and DOA.
2. Added implementation parameters:
   - array geometry,
   - channel model,
   - waveform and sampling,
   - TOA/TDOA/DOA extraction,
   - UKF parameters and base measurement covariance.
3. Added the missing 5 ms direct-path gate detail to the mechanism section.
4. Added validation protocol details:
   - 20 pings,
   - final 10-ping settled window,
   - static n=20,
   - moving n=64,
   - quasi-static n=132 accounting,
   - canonical direct+surface+bottom channel.

## Decision

The v3 manuscript keeps the main scientific claim unchanged. It does not add a new performance result. It improves reproducibility and removes the known Section 2 mismatch found in folder 93.

## Remaining submission blockers

1. Exact citation replacement for placeholders.
2. Figure polish / Fig. 5 PNG if Word-first workflow is used.
3. Journal-specific formatting and equation numbering.
4. Final English compression after the target journal is selected.

