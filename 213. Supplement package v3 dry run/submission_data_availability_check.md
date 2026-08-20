# Submission data availability check

## What is release-ready in principle

- Code folders for the adopted simulation and validation path.
- Compact JSON/CSV summaries used by manuscript tables and figures.
- Figure generation scripts for the manuscript figures.
- Claim/source mapping documents.

## What should remain excluded for now

- The local `paper/` manuscript source and build artifacts.
- Large raw overnight outputs in folder 203.
- Professor-facing or handoff-only root documents.
- Study notes and mirrored personal-study files.
- Any pilot/oracle/failure folder that is not needed to reproduce a manuscript claim.

## Data availability wording draft

The manuscript should use cautious language until an actual public repository or supplement ZIP is approved:

> Source code and compact source data required to reproduce the reported simulation figures and tables will be made available with the supplementary material upon publication or during review, subject to anonymization and repository policy.

Avoid wording that says data are already public unless the package has actually been released.

## Reproducibility boundary

The package is meant to reproduce paper-level simulation evidence. It is not a field dataset, a hardware dataset, or a validated real-water USBL benchmark.

## Remaining human decisions

- Whether to release as journal supplement, GitHub release, Zenodo, OSF, or private review archive.
- Whether raw per-ping outputs are necessary or whether compact paired summaries are enough.
- Whether any university or laboratory policy applies before public release.
