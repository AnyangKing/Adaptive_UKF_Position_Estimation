# LaTeX build QA

## Build commands used

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

Working directory:

```text
paper/
```

## Outputs

| File | Status | Pages | Notes |
|---|---:|---:|---|
| `paper/manuscript.pdf` | built | 14 | English IEEEtran draft |
| `paper/manuscript_ko.pdf` | built | 14 | Korean reading draft |

## Blocking log issues

| Check | Result |
|---|---|
| LaTeX fatal error | none found |
| Undefined reference | none found |
| Undefined citation | none found |
| Missing bibliography pass | none found |
| Overfull box | none found in the log scan |

## Non-blocking warnings

| Warning | File | Interpretation |
|---|---|---|
| Underfull vbox | English log | Ordinary float/page balancing warning; not a manuscript-content issue. |
| Underfull hbox | Korean log | Ordinary line-break issue caused by mixed Korean/English/math strings; can be polished later. |
| hyperref PDF-string warning | Korean log | Section title contains math text such as `Adaptive-$R$`; PDF bookmark removes math tokens. Body text and PDF rendering are not broken. |

## Recommendation

No immediate manuscript patch is required for the current paper-work goal.

Before final submission, polish the Korean reading draft bookmarks only if the Korean PDF is distributed as a formal document. The English submission draft currently has no unresolved-reference or overfull-box blocker.
