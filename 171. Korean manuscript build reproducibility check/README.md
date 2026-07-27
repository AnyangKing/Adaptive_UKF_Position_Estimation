# 171. Korean manuscript build reproducibility check

## Purpose

This folder records the corrected build status for the local Korean manuscript:

`paper/manuscript_ko.tex`

Folder 170 reported a build caveat because `latexmk` failed. This folder
continues that investigation and confirms that direct `pdflatex` builds work.

## Result

Status: pass with a documented tool limitation.

- `latexmk` is not currently usable because MiKTeX cannot find the required
  Perl script engine.
- Direct `pdflatex` works when run outside the workspace sandbox.
- Running `pdflatex` twice successfully regenerated:
  `paper/manuscript_ko.pdf`
- Output PDF: 11 pages, 4,883,938 bytes.
- Cross-reference rerun warning was cleared on the second run.

## Working build command

From the `paper/` directory:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ko.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ko.tex
```

## Non-working command

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript_ko.tex
```

Reason:

MiKTeX reported that the Perl script engine required by `latexmk` is missing.

## Log status after successful build

Remaining warnings are layout-level, not fatal:

- Underfull hbox at lines 79--80.
- Hyperref PDF-string warning at line 159 caused by math in a heading or
  bookmark string.
- Underfull hbox at line 223.

There were no fatal LaTeX errors, and the PDF was produced successfully.

## Repository rule

The regenerated PDF and all build artifacts are under `paper/`, which remains
local-only and ignored. They were not staged or pushed.

Only this numbered folder is committed.

## Next recommended step

172 should be a narrow Korean manuscript layout-warning cleanup:

`172. Korean manuscript LaTeX warning cleanup`

Recommended targets:

- remove or suppress the hyperref PDF-string warning at the adaptive-R
  subsection title;
- reduce the small table underfull warnings if easy;
- keep all scientific claims and numbers unchanged.
