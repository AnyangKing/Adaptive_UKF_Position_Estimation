# Build check

## Command

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

Working directory:

```text
paper/
```

## Result

- `paper/manuscript.pdf` built successfully.
- Page count remained 14.
- No fatal build error was observed.
- Remaining warnings are ordinary underfull vbox warnings.
