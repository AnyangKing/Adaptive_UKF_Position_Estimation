# Table conversion plan

The current manuscript has three manuscript-facing tables plus one internal Figure File Manifest.

## Table inventory

| Table | Location | Role | Conversion decision |
|---|---|---|---|
| Table 1 | Introduction | Prior-art positioning and novelty boundary | Keep in main text, but compress or rotate if needed. |
| Table 2 | Section 7 | Positive and negative validation outcomes | Keep in main text if page budget allows; otherwise split into performance and boundary tables. |
| Table 3 | Discussion | Limitations and follow-up work | Optional; move to supplement or convert to prose if page limit is tight. |
| Figure File Manifest | End matter | Internal package metadata | Remove from final article body; keep in submission checklist or supplement package notes. |

## Table-specific risks

### Table 1

Risk:

- very wide;
- many text-heavy columns;
- likely to overflow two-column formats.

Preferred fix:

- split into two conceptual blocks:
  1. prior frequency-diverse methods;
  2. what this paper adds.

Alternative:

- keep as landscape / full-width table if the journal supports it.

### Table 2

Risk:

- dense and long;
- mixes static, moving, quasi-static, and CRLB/floor entries.

Preferred fix:

- keep static/moving/quasi-static headline rows in the main article;
- move adaptive/sparse schedule negative row and detailed speed rows to supplement if page constrained.

Do not remove:

- moving-target negative RMSE result;
- quasi-static 0.005 m/s conservative boundary;
- "do not present 0.100 m/s as validated boundary" warning.

### Table 3

Risk:

- useful for planning but may look too internal for a final journal article.

Preferred fix:

- compress into a Discussion paragraph for short formats;
- keep as supplementary limitations table for long formats.

## Native table conversion checklist

- Convert Markdown pipes to actual Word/LaTeX tables.
- Preserve units in cells.
- Preserve p-values exactly.
- Keep "Decision for manuscript" wording conservative.
- Avoid automatic line wrapping that hides the negative results.
- Verify table captions remain above or below tables according to target journal style.
