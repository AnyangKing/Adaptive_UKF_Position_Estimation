# Page notes

## Rendered QA images

PDF image rendering:

```powershell
pdftoppm -png -r 120 paper\manuscript.pdf C:\Users\HOSEO\.codex\visualizations\2026\07\02\019f21b9-3f85-75f0-b1a2-5de8de263b8c\pdf_qa_130\page
```

Rendered pages:

```text
page-01.png ... page-12.png
```

Contact sheets:

```text
contact_1.png  pages 1--4
contact_2.png  pages 5--8
contact_3.png  pages 9--12
```

These QA images are not committed.

## Page 1

Good:

- Title, abstract, keywords, and Introduction fit cleanly.
- Full manuscript title has enough weight.

Needs later:

- Author information is still placeholder-like.
- Header says Ocean Engineering submission draft. If journal remains undecided, this should be
  changed back to journal-neutral before external sharing.

## Page 2

Good:

- Related Work and System Model flow is natural.
- The longer explanation makes the research motivation more credible.

## Page 3

Good:

- Table I is readable.
- It supports novelty defense.

Concern:

- Table I is visually heavy and consumes a large part of the page.
- Keep for now, but it remains a compression candidate if page pressure returns.

## Page 4

Good:

- Fig.1 appears close to system/model discussion.
- Implementation parameters and baseline tracking performance begin naturally.

## Page 5

Good:

- Estimator comparison and conditional adaptive-R tables make the development path more visible.

Concern:

- Two tables on one page make this page dense.
- This is acceptable for draft review, but final polish may need spacing/placement adjustment.

## Page 6

Good:

- Floor analysis and Fig.2 are clear.
- Mechanism section begins without looking abrupt.

Concern:

- This page is a likely source of the remaining underfull vbox due to float/text balancing.

## Page 7

Good:

- Mechanism equations and Fig.3 make the carrier-whitening explanation much more convincing than the
  7-page skeleton.

## Page 8

Good:

- Schedule/protocol/static validation flow is good.
- Experimental protocol subsection makes the Results section feel self-contained.

## Page 9

Good:

- Static and moving result figures are close to their text.
- The method boundary is visually clear.

## Page 10

Good:

- Discussion is now substantial.
- Robustness and practical deployment discussion strengthen SCI-readiness.

## Page 11

Good:

- Table V and Table VI are readable.
- Conclusion begins on the same page and does not feel too thin.

Concern:

- Table density is high.

## Page 12

Good:

- References fill the page well.
- The final page no longer looks empty.

