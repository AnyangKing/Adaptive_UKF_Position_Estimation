# Markdown-to-journal conversion tasks

## Must convert

- Markdown headings to journal heading style.
- Markdown tables to Word/LaTeX tables.
- Math fenced blocks to numbered equations.
- Inline code-style variables to proper math notation.
- Figure file manifest into actual figure insertions or supplementary list.
- Placeholder-like citation keys to final reference style.

## Equation numbering candidates

| Current content | Suggested equation label |
|---|---|
| array center | Eq. (1) |
| source-to-sensor range | Eq. (2) |
| observation vector | Eq. (3) |
| TOA/TDOA ideal terms | Eq. (4) |
| DOA azimuth/elevation | Eq. (5)--(6) |
| UKF state and transition | Eq. (7)--(8) |
| measurement model | Eq. (9) |
| adaptive-R scale | Eq. (10) |
| block-wise NIS inflation | Eq. (11) |
| coherent phase | Eq. (12) |
| static fixed-carrier condition | Eq. (13) |
| carrier-agile condition | Eq. (14) |
| moving self-whitening condition | Eq. (15) |
| settled RMSE | Eq. (16) |
| lag-1 correlation | Eq. (17) |

## Tables

| Table | Current issue | Conversion action |
|---|---|---|
| Table 1 | Wide | May need landscape, smaller font, or split into two tables. |
| Table 2 | Wide and dense | Could be moved to supplement or split into performance/mechanism tables. |
| Table 3 | Optional | Can be compressed into Discussion paragraph if page limit is tight. |

## Figures

Use folder:

`95. Fig5 PNG and submission packaging/figures/`

Recommended initial format:

- Use PNG for Word/professor review.
- Keep SVG for vector conversion if journal supports it.

## Reference style

Current references are metadata-ready but not style-final.

Need to choose:

- numbered IEEE style,
- author-year style,
- journal-specific BibTeX style.

