# Precommit verification

Verification run for folder 102 before committing.

## Checks

- `manuscript_clean_source_fig1_updated.md` exists.
- The old Fig. 1 manifest note `concept draft; final visual polish pending` is no longer present in the folder-102 manuscript source.
- The folder-102 manuscript source points to `fig1_system_concept_polished.svg` and `.png`.
- The updated Fig. 1 caption mentions:
  - 5 ms DOA-processing gate;
  - compact eight-sensor array;
  - fixed-carrier phase locking;
  - TOA/TDOA/DOA-UKF fusion;
  - unchanged receiver-side estimator.
- No Fig. 2--6 manifest entries were changed.

## Commit scope rule

Only `102. Manuscript figure manifest update/` should be staged for this commit.
