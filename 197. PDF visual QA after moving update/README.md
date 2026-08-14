# 197. PDF visual QA after moving update

## Purpose

Visually inspect the English IEEE manuscript PDF after the 191 moving full-range result and Fig. 7 were integrated.

## Local file inspected

- `paper/manuscript.pdf`

`paper/` remains local-only and is not committed.

## Overall verdict

The PDF is visually usable as a current manuscript draft.

- Page count: 13
- Fatal layout issue: none found
- Main moving result is visible and understandable
- IEEE two-column flow is acceptable
- No obvious figure overflow or unreadable table overflow

## Main visual observations

1. Page 1 abstract is dense but readable. The updated transition-aware moving claim is visible.
2. Page 9 has a good flow: static validation -> plain-hopping moving boundary -> transition-aware section.
3. Page 10 is the densest result page. Table V and Fig. 7 share the left column, but both remain readable.
4. Fig. 7 successfully shows the 800 m failure-and-recovery pattern.
5. Page 12 contains many summary tables. It is acceptable for the current draft, but Table VI is a supplement candidate if length must be reduced.
6. Page 13 has the limitations table, supplementary/data availability placeholder, acknowledgment placeholder, and references. This is acceptable before author/journal finalization.

## Immediate recommendation

Do not start new simulations yet. First tighten the moving-result narrative so the text around Table V and Fig. 7 reads smoothly and does not feel like a late insertion.

