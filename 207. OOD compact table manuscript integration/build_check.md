# Build check

## Commands

English manuscript:

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

Korean manuscript:

```powershell
pdflatex -interaction=nonstopmode manuscript_ko.tex
pdflatex -interaction=nonstopmode manuscript_ko.tex
```

## Result

- `paper/manuscript.pdf`: build passed, 14 pages.
- `paper/manuscript_ko.pdf`: build passed, 13 pages.
- Warnings were ordinary underfull/hyperref bookmark warnings; no blocking LaTeX error remained.

## Commit policy

The `.tex` and PDF files remain local-only in `paper/`. Only this numbered folder is committed.
