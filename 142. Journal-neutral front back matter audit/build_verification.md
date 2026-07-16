# Build verification

## Command

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
```

## Final log

```text
Underfull \vbox (badness 10000) has occurred while \output is active []
Package rerunfilecheck Info: File `manuscript.out' has not changed.
Output written on manuscript.pdf (12 pages, 1929319 bytes).
```

## Summary

| 항목 | 결과 |
|---|---:|
| PDF pages | 12 |
| Overfull hbox | 0 |
| Underfull hbox | 0 |
| Underfull vbox | 1 |
| unresolved references/citations | 0 |
| rerun needed | 0 |

## File state

```text
manuscript.tex  67609 bytes  2026-07-16 13:45:36
manuscript.pdf 1929319 bytes  2026-07-16 13:46:26
manuscript.log   24368 bytes  2026-07-16 13:46:26
```

`paper/` remains ignored and is not committed.

