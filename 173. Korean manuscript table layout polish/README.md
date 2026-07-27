# 173. Korean manuscript table layout polish

## Purpose

This pass performs a narrow table-layout polish on the local Korean manuscript:

`paper/manuscript_ko.tex`

The goal was to reduce non-fatal underfull hbox warnings without changing
scientific content.

## Local paper patch

Only two table column specifications were changed.

Claim-boundary table:

```tex
p{0.25\linewidth}p{0.34\linewidth}p{0.31\linewidth}
```

changed to:

```tex
p{0.20\linewidth}p{0.45\linewidth}p{0.25\linewidth}
```

Validation-summary table:

```tex
p{0.23\linewidth}p{0.25\linewidth}p{0.35\linewidth}
```

changed to:

```tex
p{0.20\linewidth}p{0.34\linewidth}p{0.29\linewidth}
```

## Why this was safe

- No manuscript sentence was changed.
- No number was changed.
- No figure or table caption was changed.
- No claim boundary was expanded.
- The change only gives longer English/Korean mixed phrases more horizontal
  room inside the tables.

## Build verification

Direct `pdflatex` was run twice from `paper/`.

Result:

- Build passed.
- PDF generated successfully.
- PDF pages: 11.
- PDF size: 4,883,626 bytes.
- Fatal errors: 0.
- Hyperref warnings: 0.
- Remaining underfull warnings: 2.

## Warning delta

Before this folder:

- underfull hbox warnings: 3
- source lines: 79--80 and 223

After this folder:

- underfull hbox warnings: 2
- source lines: 77--78 and 80--81

The validation-summary table warning at line 223 was removed. The two remaining
warnings are both in the claim-boundary table and are non-fatal.

## Repository rule

`paper/` remains local-only and ignored. The edited `.tex`, regenerated PDF, and
build artifacts were not staged or pushed.

Only this numbered folder is committed.

## Next recommended step

174 should be:

`174. Korean manuscript visual PDF spot check`

Recommended scope:

- inspect the current 11-page Korean PDF visually;
- check title page, tables, figure placement, and final notes;
- do not change scientific claims unless a visual/layout problem requires a
  minimal local paper patch.
