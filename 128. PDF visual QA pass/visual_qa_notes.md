# Visual QA notes

## Render method

PDF page images were rendered from:

```text
paper/manuscript.pdf
```

using MiKTeX `pdftoppm`:

```powershell
pdftoppm -png -r 120 paper\manuscript.pdf C:\Users\HOSEO\.codex\visualizations\2026\07\02\019f21b9-3f85-75f0-b1a2-5de8de263b8c\pdf_qa_128\page
```

Output images:

```text
page-1.png
page-2.png
page-3.png
page-4.png
page-5.png
page-6.png
page-7.png
```

These images are QA artifacts only and are not committed.

## Page findings

### Page 1

Good:

- IEEEtran heading style is active.
- Title and abstract fit cleanly.
- Section numbering appears as `I. Introduction`, `II. Related Work and Problem Statement`,
  `III. System Model and UKF Fusion`.

Needs later:

- Author names and affiliations are placeholders.
- Draft footer remains.

### Page 2

Good:

- Table I does not overflow.
- Text resumes normally below table.

Concern:

- Table I consumes much of the page and visually feels heavy.
- It is still defensible because novelty positioning is central to the paper.

### Page 3

Good:

- Fig.1 and Fig.2 are near the relevant model/mechanism discussion.
- IV장 Proposed Method begins cleanly.

### Page 4

Good:

- Fig.3 is near the carrier-sensitivity discussion.
- Section V begins naturally.

### Page 5

Good:

- Fig.4, Fig.5, Fig.6 are now located near the validation/boundary discussion.
- This page most clearly shows the success of the float-layout patch.

### Page 6

Good:

- Table II is readable and does not create overfull issues.
- Conclusion, back matter, and references start normally.

Needs later:

- Placeholder back matter should be removed or finalized before submission.

### Page 7

Good:

- Table III is readable.
- References finish without overflow.

Concern:

- Page has large empty area after the final reference.
- For submission polish, Table III should be shortened, moved to supplement, or converted to
  Discussion prose to reduce the manuscript to 6 pages.

