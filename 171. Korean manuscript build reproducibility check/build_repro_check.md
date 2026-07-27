# Build reproducibility check

## Commands attempted

### 1. `latexmk`

Command:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript_ko.tex
```

Outcome:

Failed.

Reason:

```text
MiKTeX could not find the script engine 'perl' which is required to execute 'latexmk'.
```

Interpretation:

The manuscript itself was not compiled by `latexmk`. This is a local toolchain
dependency issue. Installing Perl or configuring MiKTeX's script engine would be
needed before `latexmk` can be used as the one-command build path.

### 2. `pdflatex` direct build

Command:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ko.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ko.tex
```

Outcome:

Passed.

The second run cleared the cross-reference rerun warning.

## Output artifact

- File: `paper/manuscript_ko.pdf`
- Pages: 11
- Size: 4,883,938 bytes
- Generated: 2026-07-27 19:07 local time

## Remaining warnings

The final log still contains:

- Underfull hbox at lines 79--80.
- Hyperref warning at line 159 about a token not allowed in a PDF string.
- Underfull hbox at line 223.

These are not fatal. They should be cleaned in the next layout pass, but they do
not block reading the Korean PDF.

## Correction to folder 170

Folder 170 correctly identified that `latexmk` was blocked, but it did not yet
test direct `pdflatex`. This folder supersedes that build caveat:

- one-command `latexmk` build: blocked by missing Perl;
- direct `pdflatex` build: successful.
