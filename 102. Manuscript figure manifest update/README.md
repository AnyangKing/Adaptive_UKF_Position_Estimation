# 102. Manuscript figure manifest update

## Purpose

This folder integrates the polished Fig. 1 from folder 101 into the manuscript-facing source package.

Folder 101 produced the image files, but the clean manuscript in folder 100 still pointed to the older concept-draft Fig. 1. Folder 102 creates the next manuscript source version with the updated Fig. 1 caption and figure manifest.

## Inputs

- `100. Manuscript formatting prep/manuscript_clean_source.md`
- `101. Fig1 visual polish/figures/fig1_system_concept_polished.png`
- `101. Fig1 visual polish/figures/fig1_system_concept_polished.svg`
- `101. Fig1 visual polish/caption_update.md`

## Outputs

- `manuscript_clean_source_fig1_updated.md`
- `figure_manifest_update.md`
- `source_delta.md`
- `precommit_verification.md`

## Decision

Use folder-101 polished Fig. 1 as the preferred manuscript Fig. 1 candidate.

The old folder-95 Fig. 1 remains traceable, but it should no longer be the default figure for manuscript conversion.
