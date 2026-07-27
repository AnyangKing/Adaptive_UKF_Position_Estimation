# 174. Korean manuscript visual PDF spot check

## Purpose

This pass visually checks the current local Korean manuscript PDF:

`paper/manuscript_ko.pdf`

The PDF and rendered page images are local-only and were not staged or pushed.

## Rendering

The 11-page PDF was rendered to PNG page images with:

```powershell
pdftoppm -png -r 110 paper/manuscript_ko.pdf <temp>/page
```

A contact sheet was generated for visual inspection.

## Result

Status: pass for Korean review-draft use.

No blocking visual issue was found:

- all 11 pages rendered;
- title/abstract page is readable;
- tables are contained within the page margins;
- all seven figures appear;
- no figure appears clipped;
- captions are readable;
- final Korean manuscript notes are visible;
- page numbers are present.

## Minor notes

These are not blockers:

- Page 6 is close to a figure-only page with wide margins, but the figure and
  caption are readable and not clipped.
- Page 11 shows red boxes around table references. These are hyperref link
  boxes, not missing references. For the final English/IEEE version, use
  `hidelinks` or the journal-appropriate hyperlink style.
- The Korean manuscript remains a review/reference draft, not the final
  submission layout.

## Repository rule

`paper/` remains local-only and ignored.

Temporary visual QA images were generated outside the repository under the user
temp directory.

Only this numbered folder is committed.

## Next recommended step

175 should be:

`175. Korean manuscript final local handoff package`

Recommended scope:

- summarize the current Korean manuscript status for the user;
- list exact local files to open/read;
- list remaining human decisions before English port;
- avoid editing scientific content unless a clear inconsistency is found.
