# BibTeX field and formatting audit

## Required-field scan

Every BibTeX entry has the basic required fields for its entry type:

- `article`: author, title, journal, year
- `inproceedings`: author, title, booktitle, year
- `incollection`: author, title, booktitle, publisher, year

Every entry also has a DOI.

## Entries with article-number style pages

Some journals use article numbers rather than traditional page ranges. In the current BibTeX these appear under `pages`, which is common but should be checked against the final journal style.

| Key | Current pages field | Note |
|---|---:|---|
| `Zhang2024DifferentialUSBL` | 117984 | Ocean Engineering article number |
| `Tong2019USBLError` | 4373 | Sensors article number |
| `Li2019UnderwaterSRUKF` | 740 | Entropy article number |
| `RaviKumar2021HybridUKF` | 165813 | Optik article number |

No action is required now. Final copyedit may choose `eid` instead of `pages` depending on the bibliography style, but IEEEtran generally tolerates article-number-like page fields.

## Title capitalization protection

Current BibTeX protects important acronyms in several titles:

- `{USBL}`
- `{Costas}`
- `{SRP-PHAT}`
- `{AUV}`

Potential optional improvements:

- Protect `UKF` in titles if it appears in a title field.
- Protect `DOA`, `TDOA`, or `GCC-PHAT` if added later.

No current broken capitalization was observed in the generated reference page during visual QA.

## Local-only limitation

This audit did not re-check DOI correctness on the web. Existing comments in `refs.bib` say many entries were Crossref-verified on 2026-07-13. If the final target journal requires strict bibliographic accuracy, perform a final DOI/metadata check with web or library access.
