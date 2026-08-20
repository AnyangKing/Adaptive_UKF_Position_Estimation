# Build check

## Commands

English:

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

Korean:

```powershell
pdflatex -interaction=nonstopmode manuscript_ko.tex
pdflatex -interaction=nonstopmode manuscript_ko.tex
```

Working directory:

```text
paper/
```

## Output PDFs

| File | Status | Pages | Notes |
|---|---:|---:|---|
| `paper/manuscript.pdf` | built | 14 | English IEEEtran draft |
| `paper/manuscript_ko.pdf` | built | 14 | Korean reading draft |

## Log scan

| Check | Result |
|---|---|
| Fatal LaTeX error | none found |
| Undefined reference | none found |
| Undefined citation | none found |
| Overfull box | none found |
| English warnings | Underfull vbox only |
| Korean warnings | Underfull hbox and existing hyperref bookmark warning only |

## Interpretation

The 215/216 manuscript patch did not introduce a build blocker or reference/citation problem.
