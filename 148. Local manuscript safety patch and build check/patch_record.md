# Patch record

## File patched locally

`paper/manuscript.tex`

This file is ignored/local-only and is not committed.

## Exact replacement concept

Old wording:

```tex
The simulation scripts, frozen carrier schedules, validation result files (JSON/CSV), and
figure-generation scripts underlying Figs.~\ref{fig:concept}--\ref{fig:floor} will be made
available as supplementary material and/or through a public code repository. The exact repository
URL, DOI, or access policy is to be inserted by the authors before submission.
```

New wording:

```tex
The simulation scripts, frozen carrier schedules, validation result files (JSON/CSV), and
figure-generation/source-data files underlying all figures and numerical tables will be made
available as supplementary material and/or through a public code repository. The representative
two-ray fit curves and reported $\delta/R^2$ values are reproduced from the supplementary
source-data file \texttt{two\_ray\_fit.json}. The exact repository URL, DOI, or access policy is
to be inserted by the authors before submission.
```

## Why this is safe

- Does not change any performance number.
- Does not add a new scientific claim.
- Makes the supplementary-data promise align with folders 144--146.
- Explicitly ties the two-ray values to 145번 closure.

## Deferred

Not applied in this folder:

- renaming figure files;
- reworking double-column float positions;
- converting `fig_tworay_fit.png` directly from the 135 SVG;
- author/funding/repository URL placeholders.

Those should wait until a final journal/submission decision.
