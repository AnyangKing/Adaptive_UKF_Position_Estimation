# 170. Korean manuscript v3 integration audit

## Purpose

This folder records a full-paper integration audit for the local Korean
manuscript v3:

`paper/manuscript_ko.tex`

The paper file itself remains local-only and is not staged or pushed. This
folder contains only the audit record.

## Audit result

Overall status: pass with one environment caveat.

The abstract, introduction, results, discussion, conclusion, tables, and figure
captions remain inside the same claim boundary:

- headline performance claim is limited to static 600 m;
- moving-target RMSE improvement is not claimed;
- quasi-static claim is limited to very slow drift up to 0.005 m/s;
- folders 160--162 remain limitation/future-work evidence;
- no real-water performance claim is made.

## Mechanical checks

- LaTeX labels found: 10.
- LaTeX references found: 4.
- Missing references: 0.
- Figures referenced in the Korean manuscript: 7.
- Missing figure files: 0.
- Section commands: 11, including unnumbered front/back matter.
- Subsection commands: 11.

## Build caveat

Attempted command:

`latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript_ko.tex`

Result:

MiKTeX stopped before compilation with a fresh-installation setup message. This
is an environment/setup issue, not a manuscript syntax error found by LaTeX.
The previous Korean PDF and log from 2026-07-20 remain in `paper/`, but this
audit does not claim a fresh successful build.

## Important encoding note

Windows PowerShell `Get-Content` printed Korean text as mojibake during this
audit. A direct UTF-8 codepoint check showed the source file contains Korean
characters and no Unicode replacement characters. Therefore, the mojibake was
treated as a console-output false alarm rather than source-file corruption.

For future agents: inspect Korean `.tex` files with a UTF-8-aware reader before
declaring corruption.

## Next recommended step

171 should focus on a narrow local manuscript polish pass:

`171. Korean manuscript method detail readability pass`

Recommended target:

- improve Section 3 implementation/method readability for the user;
- keep all numbers unchanged;
- do not add new claims;
- do not stage or push `paper/`;
- commit only the numbered folder summary.
