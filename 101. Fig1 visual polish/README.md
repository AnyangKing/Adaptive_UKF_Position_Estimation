# 101. Fig1 visual polish

## Purpose

This folder replaces the earlier concept-draft Fig. 1 with a cleaner manuscript-facing schematic.

The figure's job is to make the paper's central mechanism immediately visible:

1. direct and surface-reflected arrivals can be processed coherently inside the 5 ms DOA gate;
2. fixed carrier transmission can lock the coherent phase and create correlated DOA bias;
3. ping-to-ping carrier agility changes the residual statistics before the same TOA/TDOA/DOA adaptive-R UKF receives the measurements.

## Inputs

- Existing Fig. 1 package:
  - `95. Fig5 PNG and submission packaging/figures/fig1_system_concept.png`
  - `95. Fig5 PNG and submission packaging/figures/fig1_system_concept.svg`
- Current manuscript caption:
  - `100. Manuscript formatting prep/manuscript_clean_source.md`

## Outputs

- `make_fig1_polished.py`: reproducible figure-generation script.
- `figures/fig1_system_concept_polished.png`
- `figures/fig1_system_concept_polished.svg`
- `caption_update.md`
- `visual_review_notes.md`

## Decision

Use this polished figure as the next candidate Fig. 1. The old figure remains available in folder 95, but the new version should be preferred for manuscript conversion unless the professor requests a different visual style.
