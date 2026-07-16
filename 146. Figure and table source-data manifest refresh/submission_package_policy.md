# Submission package policy

## Include in a future supplement/archive

When the target journal and data policy are decided, the reproducibility package should include:

- selected numbered experiment folders needed for reproduction;
- result JSON/CSV files cited by figures/tables;
- figure-generation scripts;
- final figure PNG/SVG files;
- a manifest with SHA256 hashes;
- a short `README` explaining the fixed carrier baseline and frozen 30--34 kHz schedule.

## Do not include by default

These remain excluded from the GitHub workflow and should not be packaged unless explicitly decided:

- `paper/` manuscript source/PDF;
- root handoff/report/study files;
- `.claude/`;
- `study_exports/`;
- `__pycache__/`;
- temporary logs;
- exploratory folders not cited by the manuscript.

## GitHub workflow rule

Only numbered research folders should be staged/committed/pushed.

Never use:

```text
git add .
```

Use explicit paths:

```text
git add -- "146. Figure and table source-data manifest refresh"
```

If result files inside a numbered folder are intentionally part of the evidence and are ignored by the global `results/` rule, add only those files explicitly with `git add -f --`.

## Current manuscript-source status

`paper/` is local-only/ignored. This is correct under the user's current policy.
