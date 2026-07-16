# Build report

## Environment

- Date: 2026-07-16
- Working directory: `paper/`
- Engine: MiKTeX `pdflatex`
- Command: `pdflatex -interaction=nonstopmode manuscript.tex`

The first sandboxed build failed because MiKTeX needed access to the user Roaming configuration folder. The same build succeeded with approved elevated execution.

## Build result

```text
Output written on manuscript.pdf (12 pages, 1938316 bytes).
Transcript written on manuscript.log.
```

## Warning scan

Command:

```powershell
rg -n "Overfull|Underfull|Warning|undefined|Rerun|multiply" manuscript.log
```

Relevant output:

```text
Underfull \vbox (badness 10000) has occurred while \output is active []
```

No overfull hbox, unresolved reference, or unresolved citation warning was found in the scan.

## Interpretation

The local patch did not damage the LaTeX build. The remaining underfull vbox warning existed before and is a layout/float-fill issue, not a correctness problem. It should be visually checked in the final PDF QA pass, but it is not urgent.
