# Precommit verification

Verification run for folder 100 before committing.

## Checks

- `manuscript_clean_source.md` exists and is based on folder-96 v4-ref.
- Seven folder-100 output files exist:
  - `README.md`
  - `manuscript_clean_source.md`
  - `equation_numbering_plan.md`
  - `figure_table_insertion_plan.md`
  - `cover_letter_bullets.md`
  - `formatting_todo.md`
  - `clean_source_change_log.md`
- The manuscript contains 23 fenced math blocks, matching the 23 planned equation entries.
- Stale citation-metadata-open language was replaced with final-style-pending language.
- The main scientific boundaries remain intact:
  - static 600 m: 13.01 m to 8.87 m, p = 0.0008;
  - moving-target RMSE gain not claimed;
  - continuous quasi-static boundary limited to 0.005 m/s;
  - sub-meter 600 m performance not claimed.

## Commit scope rule

Only `100. Manuscript formatting prep/` should be staged for this commit.

Do not stage local-only handoff, study, or professor-report files.
