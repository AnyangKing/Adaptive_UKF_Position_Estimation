# 172. Korean manuscript LaTeX warning cleanup

## Purpose

This pass performs a narrow LaTeX warning cleanup on the local Korean
manuscript:

`paper/manuscript_ko.tex`

The scientific content, numbers, figures, tables, and claim boundary were not
changed.

## Local paper patch

Changed one subsection command:

```tex
\subsection{Adaptive-$R$ routing}
```

to:

```tex
\subsection[Adaptive-R routing]{Adaptive-$R$ routing}
```

Reason:

The printed title still shows `Adaptive-$R$ routing`, but the PDF bookmark uses
the plain-text optional title `Adaptive-R routing`. This removes the hyperref
PDF-string warning caused by math mode in a bookmark string.

## Build verification

Direct `pdflatex` was run twice from `paper/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ko.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ko.tex
```

Result:

- Build passed.
- Output PDF: 11 pages.
- Output size: 4,883,938 bytes.
- No fatal errors.
- No unresolved-reference rerun warning.
- Hyperref PDF-string warning removed.

## Remaining warnings

Only non-fatal underfull hbox warnings remain:

- lines 79--80 in the claim-boundary table;
- line 223 in the validation-summary table.

These are table wrapping/layout warnings. They do not change the scientific
content and can be handled in a later table-layout pass if desired.

## Repository rule

`paper/` remains local-only and ignored. The regenerated PDF, auxiliary files,
and edited `.tex` file were not staged or pushed.

Only this numbered folder is committed.

## Next recommended step

173 should be:

`173. Korean manuscript table layout polish`

Recommended scope:

- reduce the remaining underfull warnings in the two summary tables;
- keep all claim wording and numbers unchanged;
- verify with direct `pdflatex` twice;
- commit only the numbered folder.
