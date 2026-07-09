# v1 assembly checklist

## Step 1 — create manuscript_draft_v1.md

Copy:

```text
85. Manuscript draft v0/manuscript_draft_v0.md
```

into a new v1 working file in the next manuscript folder.

## Step 2 — replace sections

Use `v1_section_blocks.md` to replace or expand:

- Section 2
- Section 4
- Section 5
- Section 6
- Section 7

## Step 3 — add figure/table callouts

Use `figure_callouts.md`.

Minimum callouts required:

- Fig. 1 in Section 2/4
- Fig. 2 in Section 4
- Fig. 3 in Section 6
- Fig. 4 in Section 7.1
- Fig. 5 in Section 7.2
- Table 1 in Introduction/Discussion
- Table 2 at the end of Results

## Step 4 — preserve claim boundary

Verify:

- static long-range is the main claim
- quasi-static is limited to 0.005 m/s
- moving RMSE improvement is not claimed
- frequency hopping first-use is not claimed

## Step 5 — citation placeholders

Do not remove placeholders until 86번 audit is actually completed.

Allowed:

- keep `[RADAR_FREQ_AGILITY_REF]`
- keep `[FH_USBL_REF]`
- keep `[COSTAS_USBL_REF]`
- keep `[FREQ_COMB_REF]`

Not allowed:

- invent exact references from memory
- cite unverified titles as final

## Step 6 — numerical consistency

Check every occurrence:

- 13.01 m
- 8.87 m
- -32%
- p = 0.0008
- +0.470 to -0.208
- p = 5.6e-10
- -0.10 m, p = 0.301
- 11.98 m to 10.49 m
- p = 8.00e-05
- 0.005 m/s boundary

## Step 7 — final v1 quality gate

The v1 draft is acceptable when:

- equations are inserted
- figure callouts exist
- claim boundary is consistent
- citation placeholders are explicit
- no new unsupported claim is introduced
