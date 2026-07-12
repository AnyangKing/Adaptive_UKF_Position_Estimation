# Precommit verification

Verification run for folder 103 before committing.

## Checks

- Folder 103 contains a Sensors-style free-format candidate source.
- Keywords were added.
- Back matter placeholders were added:
  - Supplementary Materials;
  - Author Contributions;
  - Funding;
  - Data Availability Statement;
  - Acknowledgments;
  - Conflicts of Interest.
- Fig. 1 remains mapped to the folder-101 polished figure.
- Fig. 2--6 remain mapped to the folder-95 figure package.
- The audit identifies missing human decisions rather than inventing author/funding/conflict metadata.
- The conversion log preserves the scientific claim boundaries.
- The dry-run abstract is about 205 words, so the next English-polishing pass should trim it slightly if Sensors remains the target.

## Commit scope rule

Only `103. Sensors free-format dry run/` should be staged for this commit.
