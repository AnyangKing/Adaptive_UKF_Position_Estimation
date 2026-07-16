# Citation key audit

## Missing / unused / duplicate

| Check | Result |
|---|---|
| Cited keys missing from `refs.bib` | none |
| Duplicate BibTeX keys | none |
| Unused BibTeX entries | `Delano1953TargetGlint` |
| Repeated citations in text | expected; method/prior-art keys are cited in both prose and tables |

Repeated citation keys:

- `Beaujean2007FrequencyHoppedUSBL`
- `Do2010SRPPHAT`
- `Julier2004Unscented`
- `Knapp1976GCCPHAT`
- `Loomis1974FrequencyAgilityGlint`
- `Nhat2022CostasUSBL`
- `Qian2025FrequencyCombIUSBL`
- `Tong2019USBLError`
- `Zhang2024DifferentialUSBL`

These repeats are not problems. They correspond to items cited once in related prose and again in the prior-art table or method details.

## Novelty-defense core citations

| Key | Role | Status |
|---|---|---|
| `Loomis1974FrequencyAgilityGlint` | radar frequency agility / glint heritage | cited |
| `Blunt2016WaveformDiversity` | broader radar waveform diversity | cited |
| `Beaujean2007FrequencyHoppedUSBL` | frequency-hopped acoustic modem USBL prior | cited |
| `Nhat2022CostasUSBL` | Costas hopping USBL closest underwater waveform prior | cited |
| `Qian2025FrequencyCombIUSBL` | acoustic frequency-comb/iUSBL prior | cited |
| `Zhang2024DifferentialUSBL` | USBL calibration/differential correction prior | cited |
| `Delano1953TargetGlint` | classical radar target glint background | present in bib but not cited |

## Recommendation for `Delano1953TargetGlint`

Two safe options:

1. Keep it in `refs.bib` as a back-pocket source but do not worry about it until final style cleanup.
2. Add it next to Loomis in the radar glint sentence if the final manuscript can spare one more citation.

Suggested insertion if used:

```tex
Radar literature has long treated target glint and used frequency agility to decorrelate
glint-like angular errors~\cite{Delano1953TargetGlint,Loomis1974FrequencyAgilityGlint,
Blunt2016WaveformDiversity}.
```

Do not add it if the reference list length becomes a constraint.
