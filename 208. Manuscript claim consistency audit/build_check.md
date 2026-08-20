# Build check

## Korean manuscript

Command:

```powershell
pdflatex -interaction=nonstopmode manuscript_ko.tex
pdflatex -interaction=nonstopmode manuscript_ko.tex
```

Result:

- Build passed.
- Output: `paper/manuscript_ko.pdf`
- Pages: 14
- Notes: only ordinary underfull/hyperref warnings.

## Why only Korean was rebuilt

208 edited only the Korean baseline manuscript. English manuscript was unchanged from 207.
