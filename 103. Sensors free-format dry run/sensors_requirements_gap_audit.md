# Sensors free-format requirements gap audit

Source checked: official Sensors Instructions for Authors, 2026-07-12.

## Official requirements used

- Sensors asks authors to use the Word or LaTeX template when preparing manuscripts, but it also accepts free-format submission.
- Free-format submissions still need required sections: author information, abstract, keywords, introduction, materials and methods, results, conclusions, figures and tables with captions, funding information, author contributions, conflict of interest and other ethics statements.
- Research manuscripts should include front matter, research sections, and back matter including supplementary materials, author contributions, funding, data availability statement, acknowledgments, conflicts of interest, and references.
- Sensors states that full experimental details must be provided for reproducibility.
- It encourages sharing research data, code, software, algorithms, protocols, raw/processed data, and study material where possible.
- Figures should be inserted in the main text after first citation when using Word.
- Equations should remain editable, not image-only.

## Current manuscript gap table

| Requirement | Current evidence | Status | Action |
|---|---|---|---|
| Title | Present | OK | Keep, but may shorten after journal choice. |
| Author information | Not present | Missing | Human authors must provide names, affiliations, corresponding author, ORCID if used. |
| Abstract | Present | OK / check length | Confirm <= about 200 words if targeting Sensors. |
| Keywords | Added in folder-103 candidate | Drafted | Human review for 3--10 keywords. |
| Introduction | Present | OK | Keep novelty wording conservative. |
| Materials and Methods | Present as System/Signal Model + Method | Needs mapping | Rename or map Sections 2 and 5 into Materials and Methods if using Sensors template. |
| Results | Present as Sections 3, 6, 7 | Needs mapping | Keep Section 3 as diagnostic/result background or move parts to Results. |
| Discussion | Present | OK | Keep limitations explicit. |
| Conclusions | Present | OK | Fine for Sensors even though optional. |
| Figures and captions | Present | Mostly OK | Fig. 1 updated in folder 102; final package needs Fig.1 from 101 and Fig.2--6 from 95. |
| Tables | Present in Markdown | Needs conversion | Convert Markdown tables to Word/LaTeX-native tables. |
| Funding | Added placeholder | Missing human decision | Fill exact funding/no-funding statement. |
| Author Contributions | Added placeholder | Missing human decision | Human authors must assign roles. |
| Data Availability Statement | Added dry-run placeholder | Needs final decision | Choose public repository/DOI, supplementary material, or access-on-request statement. |
| Acknowledgments | Added placeholder | Missing human decision | Fill or omit depending on journal rules. |
| Conflicts of Interest | Added placeholder | Missing human decision | Fill no-conflict/conflict statement. |
| References | Present | Style pending | Convert to selected reference style. |
| Editable equations | Markdown math present | Needs conversion | Convert fenced math to editable Word/LaTeX equations. |
| Reproducibility details | Strong method detail present | Needs asset packaging | Bundle scripts/config/results as supplement or archive. |

## Dry-run verdict

The manuscript is scientifically ready for a free-format-style dry run, but not ready for final submission. The remaining blockers are mostly submission infrastructure rather than scientific content:

1. human author/funding/conflict metadata;
2. data/code availability decision;
3. editable equation conversion;
4. native table conversion;
5. final figure package assembly.
