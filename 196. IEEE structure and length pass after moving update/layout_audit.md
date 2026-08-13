# Layout audit

## Figures and tables

Current English manuscript has:

- 8 figures
- 7 tables
- 13 pages in IEEEtran journal format

The new moving full-range figure is included as:

- `fig7_moving_full_range_rmse.png`
- label: `fig:movingfull`

The gain/tail figure generated in 194 is not inserted into the main manuscript yet:

- `fig8_moving_full_range_gain_tail.png`

Recommendation: keep fig8 as supplementary or reserve it for a later figure-reduction decision. The main manuscript already has enough floats.

## Small cleanup applied

Changed long subsection headings:

- `Plain-Hopping Temporal Decorrelation and Motion Boundary`
  -> `Plain-Hopping Motion Boundary`
- `Transition-Aware Adaptive-$R$ Moving-Target Validation`
  -> display title `Transition-Aware Adaptive-$R$ Moving Validation` with a PDF-bookmark-safe optional title

This removed the earlier hyperref warning caused by math in the subsection title.

## Length judgment

13 IEEEtran pages is not too short for the current depth of the work.  
It is also not yet a final submission length decision because author info, target journal, and final formatting are not fixed.

If the target journal later requires a shorter manuscript, the first candidates to move to supplement are:

1. fig8 gain/tail plot;
2. detailed quasi-static per-speed table;
3. part of the robustness table/limitation table;
4. expanded baseline audit details.

