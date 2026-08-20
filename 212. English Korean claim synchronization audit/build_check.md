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
- Notes: ordinary underfull warnings only.

## GitHub policy

The modified `paper/manuscript.tex` and generated PDF remain local-only. Only this numbered folder is committed.
