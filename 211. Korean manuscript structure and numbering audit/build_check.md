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
- Notes: ordinary underfull/hyperref warnings only.

## GitHub policy

The modified `paper/manuscript_ko.tex` and generated PDF remain local-only. Only this numbered folder is committed.
