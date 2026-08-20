# Build check

## English manuscript

Command used:

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
- Notes: `latexmk` was not usable because the local MiKTeX installation could not find Perl, so the equivalent `pdflatex`/`bibtex` sequence was used.

## Korean manuscript

Command used:

```powershell
pdflatex -interaction=nonstopmode manuscript_ko.tex
pdflatex -interaction=nonstopmode manuscript_ko.tex
```

Result:

- Build passed.
- Output: `paper/manuscript_ko.pdf`
- Pages: 13
- Notes: only ordinary underfull/hyperref bookmark warnings were observed.

## GitHub policy

The updated PDFs and `.tex` files remain local-only in `paper/`. This numbered folder is the only artifact committed for this step.
