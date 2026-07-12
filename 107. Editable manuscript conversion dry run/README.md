# 107. Editable manuscript conversion dry run

## Purpose

This folder creates a non-final DOCX conversion dry run from the latest tightened manuscript.

The goal is to test conversion mechanics:

- Markdown headings to Word headings;
- fenced math blocks to editable text equations;
- Markdown tables to native Word tables;
- Fig. 1--6 image insertion;
- claim-boundary preservation.

This is not a final journal submission DOCX.

## Design preset

Documents skill preset used:

- `compact_reference_guide`

Resolved tokens applied in the builder:

- US Letter portrait;
- 1 inch margins;
- Calibri 11 pt body;
- 1.25 body line spacing;
- Heading 1: 16 pt, blue, 18 pt before, 10 pt after;
- Heading 2: 13 pt, blue, 14 pt before, 7 pt after;
- table grid with compact 8--9 pt cell text for wide tables.

## Outputs

- `editable_manuscript_conversion_dry_run.docx`
- `scripts/build_docx_dry_run.py`
- `rendered_pages/` after render QA
- `conversion_dry_run_report.md`
- `precommit_verification.md`
