# Patch suggestions for the manuscript

These are suggestions only. They were not applied in this folder because `paper/` is local-only and manuscript edits should be deliberate.

## P1 — Data Availability figure range

Current risk:

> The simulation scripts, frozen carrier schedules, validation result files (JSON/CSV), and figure-generation scripts underlying Figs.~\ref{fig:concept}--\ref{fig:floor} ...

This can look like only a subset of figures is covered.

Suggested replacement:

> The simulation scripts, frozen carrier schedules, validation result files (JSON/CSV), and figure-generation/source-data files underlying all figures and numerical tables will be made available as supplementary material and/or through a public code repository.

Reason:

- Avoids label-range ambiguity.
- Includes two-ray/static/moving/quasi figures.
- Matches 146번 source-data manifest.

## P2 — Two-ray figure source-data note

Optional sentence near the two-ray figure caption or supplement statement:

> The representative two-ray fit curves and reported $\delta/R^2$ values are reproduced from the source-data manifest in folder 145.

For an actual paper, do not mention “folder 145” literally unless the supplement archive keeps that folder name. In final form:

> The representative two-ray fit curves and reported $\delta/R^2$ values are reproduced from the supplementary source-data file `two_ray_fit.json`.

## P3 — Figure naming caution for supplement

No manuscript text change required. In the supplement package, avoid relying on filename order because:

- `fig6_crlb_floor.png` appears before `fig2_frequency_agile_bias.png` in the paper.
- Manuscript figure numbering follows LaTeX float order, not filename.

Suggested supplement README line:

> Figure filenames are inherited from the development history; manuscript figure order is defined by labels and captions, not filename numbering.

## P4 — 136 manifest table count correction

146번 README says “그림 7개와 표 6개.” The current audit counts seven labeled tables if `tab:limitations` is included.

Recommended future correction:

> 그림 7개와 labeled table 7개.

This is not scientifically important, but it matters for packaging neatness.

## P5 — Final journal style placeholders

Leave placeholders for now, as the user requested:

- author names
- affiliation
- corresponding email
- funding
- data availability repository URL
- journal-specific template

Do not fabricate these.
