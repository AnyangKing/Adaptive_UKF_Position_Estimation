# 114. paper Git untrack

## Purpose

The user clarified that GitHub pushes should include only numbered work folders. Manuscript
workspace files under `paper/` must remain local and must not be published to GitHub.

## Actions

- Added `paper/` to `.gitignore`.
- Removed previously tracked `paper/` files from the Git index with `git rm --cached -r paper`.
- Kept all local manuscript files intact on disk.

## Important rule

Do not use `git add .`.

For future commits, stage only the numbered work folder requested by the user. Do not stage
`paper/`, root operation MD files, study files, or professor-report files unless the user
explicitly changes this rule.
