# 217. Supplement package assembly dry run

## Purpose

This folder updates the supplement-package dry run after folders 215 and 216.

It does not create a public repository or a submission ZIP. Instead, it verifies that the paper-facing source artifacts exist and records a reproducible package inventory.

## Why this was needed

Folder 213 defined supplement package v3 before the two computer-checkable weakness patches:

- 215 hardware frequency-response mismatch sensitivity;
- 216 extended OOD motion-family validation.

Those two folders add evidence that should be available to reviewers as supplementary simulation material.

## Files

- `validate_supplement_v4.py` -- checks required source artifacts and writes an inventory.
- `supplement_v4_inventory.json` -- generated path/hash/size inventory.
- `supplement_v4_manifest.md` -- human-readable package layout and exclusion policy.
- `assembly_dry_run_report.md` -- validation result.

## Decision

Use supplement package v4 as the current package plan.

Actual ZIP/public release remains a submission-stage decision because it may depend on journal policy, anonymization, and professor/lab approval.
