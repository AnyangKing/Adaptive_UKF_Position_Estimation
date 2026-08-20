# Build check

## English manuscript

Command:

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

Result:

- Build passed.
- Output: `paper/manuscript.pdf`
- Pages: 14
- Notes: only ordinary underfull warnings.

## Why only English was rebuilt

209 edited only the English `Supplementary Material and Data Availability` paragraph.
