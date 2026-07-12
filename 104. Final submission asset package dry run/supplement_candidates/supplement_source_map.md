# Supplement source map

This map identifies what should be considered for a reproducibility supplement or public archive.

## Required minimum for reproducibility

| Claim / figure | Source candidate | Purpose |
|---|---|---|
| Fig. 1 mechanism schematic | `101. Fig1 visual polish/make_fig1_polished.py` | Reproduce polished Fig. 1. |
| Fig. 2 carrier sensitivity | Folder 58 / 70 figure-generation lineage | Reproduce frequency-agile bias mechanism figure. |
| Fig. 3 static 600 m validation | Folder 61 result JSON/CSV and folder 70 figure script lineage | Reproduce main performance figure and headline 13.01 m to 8.87 m result. |
| Fig. 4 moving whitening boundary | Folder 63 result JSON/CSV and figure script lineage | Reproduce lag-1 whitening and moving RMSE boundary. |
| Fig. 5 quasi-static boundary | Folder 82 JSON/CSV and folder 95 generation script | Reproduce speed-boundary figure. |
| Fig. 6 CRLB/floor | Folder 45/70 lineage | Reproduce compact-aperture floor figure. |
| Method constants | Folder 93 code audit and adopted implementation files | Verify parameters in Section 2. |

## Do not include by default

- local-only handoff files;
- `study_exports/`;
- `.claude/`;
- professor-report summaries;
- unrelated exploratory folders not cited by the manuscript.

## Next packaging task

Create a minimal supplement archive only after deciding the data/code availability policy:

1. public repository / DOI archive;
2. supplementary material ZIP;
3. data/code available on request.
