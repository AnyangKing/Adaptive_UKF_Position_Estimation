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

## Result

| File | Status | Pages | Notes |
|---|---:|---:|---|
| `paper/manuscript.pdf` | built | 14 | English IEEEtran draft |
| `paper/manuscript_ko.pdf` | built | 14 | Korean reading draft |

## Warning status

- No fatal LaTeX error.
- No unresolved reference or citation observed in the build output.
- No overfull-box blocker observed.
- Existing underfull warnings remain non-blocking.
