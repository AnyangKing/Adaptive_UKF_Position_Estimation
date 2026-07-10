# 96. Citation placeholder closure

## Purpose

This folder closes the manuscript's main citation placeholders at the metadata level.

The goal is not to claim that full-text literature review is complete. The goal is narrower:

- replace placeholder labels with verified title/author/venue/page/DOI metadata,
- clarify what each citation supports,
- prevent overclaiming such as "first frequency-hopping USBL."

## Verification source

Metadata was checked on 2026-07-10 using Crossref DOI records and DOI URLs.

## Outputs

- `verified_reference_table.md`
- `bibtex_entries.md`
- `manuscript_reference_patch.md`
- `citation_claim_safety_check.md`
- `make_manuscript_v4_refs.py`
- `manuscript_draft_v4_refs.md`

## Closure status

| Placeholder | Status |
|---|---|
| `[RADAR_FREQ_AGILITY_REF]` | metadata closed |
| `[FH_USBL_REF]` | metadata closed |
| `[COSTAS_USBL_REF]` | metadata closed |
| `[FREQ_COMB_REF]` | metadata closed |

`manuscript_draft_v4_refs.md` has zero remaining occurrences of the four placeholder labels above.

## Remaining caution

For submission, it is still best to access the publisher/IEEE pages or PDFs through the university library and confirm the exact in-text wording. The metadata is strong enough to replace placeholders, but full-text semantic audit remains a final polish step.
