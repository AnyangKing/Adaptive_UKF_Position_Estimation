# 103. Sensors free-format dry run

## Purpose

This folder performs a non-final Sensors-style free-format submission dry run.

The goal is not to submit to Sensors yet. The goal is to use Sensors as a concrete formatting stress test because it currently allows free-format submission while still requiring specific manuscript components.

## Inputs

- Latest manuscript source:
  - `102. Manuscript figure manifest update/manuscript_clean_source_fig1_updated.md`
- Polished Fig. 1:
  - `101. Fig1 visual polish/figures/fig1_system_concept_polished.*`
- Fig. 2--6 package:
  - `95. Fig5 PNG and submission packaging/figures/`
- Official Sensors author instructions checked on 2026-07-12:
  - https://www.mdpi.com/journal/sensors/instructions

## Outputs

- `manuscript_sensors_free_format_candidate.md`
- `sensors_requirements_gap_audit.md`
- `front_back_matter_blocks.md`
- `conversion_breakage_log.md`
- `submission_asset_map.md`
- `precommit_verification.md`

## Decision

This folder keeps the journal choice reversible. It prepares a Sensors-compatible free-format candidate and records the gaps that would also matter for many other journals: keywords, data availability, funding, author contributions, conflicts, figure packaging, and editable equations.
