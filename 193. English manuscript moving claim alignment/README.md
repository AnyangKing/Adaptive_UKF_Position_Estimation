# 193. English manuscript moving claim alignment

## Purpose

Align the English IEEE-format manuscript with the Korean baseline manuscript after the 191 moving full-range validation.

## Source result

- `191. Moving full range transition aware independent validation`
- 0--1000 m moving-target independent validation
- 528 paired cases
- Frozen transition-aware Adaptive-R rule
- softR vs hop mean gain: +3.948 m, p = 1.585e-22
- softR vs fixed mean gain: +4.797 m, p = 1.671e-30

## Local manuscript edits

Edited local-only file:

- `paper/manuscript.tex`

The paper folder remains intentionally untracked and was not committed.

## Claim alignment

The manuscript now distinguishes:

1. Static 600 m carrier-agile validation remains the static claim.
2. Plain moving-target hopping remains a failure/boundary result.
3. Transition-aware Adaptive-R is now the moving-target simulation claim.
4. Real-water validation and arbitrary-motion generalization remain forbidden.

## Build check

The English manuscript should be built locally after this patch. Build artifacts remain local-only.

