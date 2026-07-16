# Final PDF QA checklist

Use this after the next manuscript build, especially if patches from `patch_suggestions.md` are applied.

## Build checks

- [ ] `pdflatex` / `latexmk` completes.
- [ ] unresolved references: 0.
- [ ] unresolved citations: 0.
- [ ] overfull hbox: 0.
- [ ] underfull hbox: acceptable / none severe.
- [ ] underfull vbox: inspect visually if present.

Current known build state before this folder:

- PDF: 12 pages.
- Overfull hbox: 0.
- Underfull hbox: 0.
- Remaining warning: one `Underfull \vbox (badness 10000)`.

## Visual checks

- [ ] Title/abstract fit cleanly on page 1.
- [ ] `tab:priorart` appears near Related Work and does not split awkwardly.
- [ ] Fig. concept appears after System Model introduction and before too much method detail.
- [ ] `tab:estimators` and `tab:routing` remain readable in one column.
- [ ] CRLB table and CRLB floor figure appear in the floor subsection or close to it.
- [ ] `fig_tworay_fit.png` appears near the two-ray model paragraph.
- [ ] `fig2_frequency_agile_bias.png` appears near carrier sensitivity discussion.
- [ ] static/moving/quasi figures appear in the validation section.
- [ ] `tab:results`, `tab:quasi`, and `tab:limitations` do not drift too far from first mention.
- [ ] References start cleanly and do not leave a nearly empty final page.

## Claim checks

- [ ] Moving target text does not claim RMSE improvement.
- [ ] Quasi-static text says continuous support only to 0.005 m/s.
- [ ] Frequency hopping novelty is framed as mechanism/application/boundary, not invention of frequency hopping.
- [ ] Static result remains the main performance claim: 13.01 m → 8.87 m, +4.14 m, p=0.0008.
- [ ] Two-ray values match 135: 400 m δ=1.337 ms/R²=0.995; 600 m δ=1.875 ms/R²=0.750.

## Packaging checks

- [ ] `paper/` remains local-only unless user explicitly changes policy.
- [ ] Numbered folders only are committed.
- [ ] No `git add .`.
- [ ] If a numbered folder intentionally includes ignored `results/`, add exact files with `git add -f --`.
