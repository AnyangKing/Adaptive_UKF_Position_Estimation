# Precommit verification

Verification run for folder 107 before committing.

## Checks

- DOCX dry-run file exists.
- Builder script exists and is reproducible.
- Structural `python-docx` check reports:
  - 130 paragraphs;
  - 4 native Word tables;
  - 6 images;
  - 23 editable equation paragraphs.
- Render QA was attempted but failed because LibreOffice/soffice was not found.
- The render failure is documented in `conversion_dry_run_report.md`.

## Commit scope rule

Only `107. Editable manuscript conversion dry run/` should be staged for this commit.
