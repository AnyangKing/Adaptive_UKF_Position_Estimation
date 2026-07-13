# Build verification

## Command

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
```

## Final log extraction

검색 패턴:

```powershell
Select-String -LiteralPath "manuscript.log" -Pattern "Output written|Overfull|Underfull|float-only|undefined|Rerun|Warning|Citation|Reference"
```

중요 출력:

```text
Package rerunfilecheck Info: File `manuscript.out' has not changed.
Output written on manuscript.pdf (7 pages, 1708011 bytes).
```

## Interpretation

The warning extraction contains no active Overfull, Underfull, float-only, undefined citation,
undefined reference, or rerun-needed warning.

## File timestamps

```text
manuscript.tex  2026-07-13 13:59:51
manuscript.pdf  2026-07-13 14:00:14
manuscript.log  2026-07-13 14:00:14
```

## Git policy check

`paper/` remains ignored:

```text
!! paper/
```

Only this 127 numbered folder should be committed.

