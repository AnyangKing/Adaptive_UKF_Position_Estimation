# Manuscript reference patch

Target manuscript:

- `94. Manuscript v3/manuscript_draft_v3.md`

## Placeholder replacement map

| Placeholder | Replace with citation key |
|---|---|
| `[RADAR_FREQ_AGILITY_REF]` | `[Loomis1974FrequencyAgilityGlint]` |
| `[FH_USBL_REF]` | `[Beaujean2007FrequencyHoppedUSBL]` |
| `[COSTAS_USBL_REF]` | `[Nhat2022CostasUSBL]` |
| `[FREQ_COMB_REF]` | `[Qian2025FrequencyCombIUSBL]` |

Optional:

- If a general radar-glint background sentence is added, cite `[Delano1953TargetGlint]`.

## Suggested Introduction sentence

Current:

> Radar literature has long used frequency agility to decorrelate glint-like angular errors [RADAR_FREQ_AGILITY_REF], and underwater positioning literature includes frequency-hopped acoustic modem USBL, Costas-based USBL design, acoustic frequency-comb approaches, and other frequency-diversity methods [FH_USBL_REF], [COSTAS_USBL_REF], [FREQ_COMB_REF].

Replace with:

> Radar literature has long used frequency agility to reduce glint-like angular pointing error [Loomis1974FrequencyAgilityGlint], and underwater positioning literature includes frequency-hopped acoustic modem USBL [Beaujean2007FrequencyHoppedUSBL], Costas-hopping USBL design [Nhat2022CostasUSBL], and acoustic frequency-comb iUSBL approaches [Qian2025FrequencyCombIUSBL].

## Suggested References section replacement

Replace the placeholder reference list with the BibTeX entries in `bibtex_entries.md` or with the target journal's formatted style.

## Important wording guard

Keep the current novelty sentence:

> The contribution here is not the first use of frequency hopping.

This is now directly supported by the verified Beaujean 2007 and Nhat 2022 references.

