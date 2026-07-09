# Placeholder replacement plan

## Manuscript v0 placeholders

`85. Manuscript draft v0/manuscript_draft_v0.md` currently contains:

- `[RADAR_FREQ_AGILITY_REF]`
- `[FH_USBL_REF]`
- `[COSTAS_USBL_REF]`
- `[FREQ_COMB_REF]`

## Replacement rule

Do not replace a placeholder with a final citation until:

1. exact metadata is verified from publisher/DB,
2. the source's actual claim is checked,
3. distinction from our work is written in the audit matrix,
4. BibTeX entry is created.

## Suggested replacement positions

### Introduction paragraph 3

Current sentence:

> Radar literature has long used frequency agility to decorrelate glint-like angular errors [RADAR_FREQ_AGILITY_REF], and underwater localization literature includes frequency-hopped acoustic modem USBL, Costas-based USBL design, acoustic frequency-comb approaches, and other frequency-diversity methods [FH_USBL_REF], [COSTAS_USBL_REF], [FREQ_COMB_REF].

After audit:

> Radar literature has long used frequency agility to decorrelate glint-like angular errors [A1], [A2], and underwater positioning has used frequency-hopped acoustic modem USBL [B1], Costas-hopping USBL designs [C1], and acoustic frequency-comb or other frequency-diverse approaches [D1], [D2].

### Discussion paragraph 2

Add explicit difference sentence:

> Unlike these waveform- or radar-origin frequency-diversity uses, the present work treats carrier agility as an observation-design tool for whitening a post-gating coherent DOA residual before TOA/TDOA/DOA-UKF fusion.

## BibTeX key naming

Use stable keys:

```text
radar_freq_agility_glint_YYYY
beaujean_fh_usbl_jasa_2007
costas_usbl_baseline_2022
freq_comb_iusbl_YYYY
mimo_sonar_tds_YYYY
usbl_calibration_installation_YYYY
```

If author/year are verified, use author-year keys instead.

## If exact old radar citation remains unavailable

Use a safer sentence:

> Frequency agility is a well-established radar/sonar waveform-diversity concept, including applications to angle-error decorrelation and tracking robustness [verified handbook or review].

This is weaker but safer than citing an unverified old IEEE title.

## If JASA/IEEE USBL prior art is verified

Include it prominently. This strengthens the paper because it shows we are not hiding prior frequency-hopping USBL.

Suggested sentence:

> Prior USBL work has already used frequency-hopped or Costas-type acoustic signals, but primarily for waveform coding, time-delay precision, or baseline/navigation design; our focus is the carrier-locked coherent DOA-bias residual that remains after direct-path gating.

## If a source appears too close

If any prior source explicitly uses frequency hopping to whiten multipath DOA bias in USBL tracking, then revise novelty:

1. reduce novelty to independent validation + boundary analysis,
2. move mechanism claim to confirmation rather than invention,
3. strengthen 82 boundary and negative results as differentiator.
