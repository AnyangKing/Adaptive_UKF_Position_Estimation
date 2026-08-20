# 213. Supplement package v3 dry run

## Purpose

This folder updates the supplementary-material plan after the moving full-range and OOD validation work.

The work is a manuscript/package audit only. It does not introduce a new experiment, a new metric, or a new paper claim.

## Why this was needed

Earlier supplement dry runs were centered on the static 600 m, moving-boundary, quasi-static, CRLB, and two-ray evidence. After folders 191, 194, 204, and 209, the manuscript now also depends on:

- structured 0--1000 m moving validation;
- OOD moving-family validation;
- compact moving-result figures and source data;
- stricter claim boundaries for plain hopping and transition-aware soft-R.

Without a v3 package map, a reviewer could reasonably ask which exact artifact reproduces the newest moving-target claims.

## Files in this folder

- `supplement_package_v3_manifest.md` -- proposed archive layout and claim-to-artifact mapping.
- `submission_data_availability_check.md` -- what can be released, what must stay excluded, and what remains to decide before submission.
- `paper_sync_check.md` -- check that the current English/Korean manuscripts have matching supplement expectations.

## Decision

Use supplement package v3 as the current paper-facing package plan.

Do not commit `paper/`, raw overnight outputs, root handoff MD files, or `study_exports/` with this folder. They are working assets, not numbered-folder deliverables.
