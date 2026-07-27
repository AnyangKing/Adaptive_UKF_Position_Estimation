# Table layout polish details

## Problem

After folder 172, the Korean manuscript built successfully but still had three
non-fatal underfull hbox warnings:

- claim-boundary table, lines 79--80;
- validation-summary table, line 223.

The warnings were caused by narrow table cells containing mixed Korean and
English technical terms such as:

- `residual whitening`
- `continuous safe boundary`
- `lag-1 residual whitening`

## Patch

The patch widened the middle result/claim columns and narrowed the shorter
condition/forbidden-expression columns.

No content was rewritten.

## Verification

The manuscript was rebuilt twice with direct `pdflatex`.

Final log status:

- output PDF produced;
- 11 pages;
- no fatal errors;
- no hyperref warnings;
- no rerun-label warning;
- two remaining underfull hbox warnings in the claim-boundary table.

## Interpretation

This pass improved the layout-warning state but did not chase every underfull
warning aggressively. The remaining two warnings are harmless and may be left
until final English/IEEE formatting, where the table will likely be redesigned
for two-column IEEE layout anyway.
