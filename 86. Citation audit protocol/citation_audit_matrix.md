# Citation audit matrix

## Placeholder group A — radar frequency agility / glint

Current manuscript placeholders:

- `[RADAR_FREQ_AGILITY_REF]`

Purpose in manuscript:

- Show that frequency agility as a general principle is not new.
- Protect the paper from “radar already did this” reviewer criticism.

Candidate literature families:

- radar glint reduction by pulse-to-pulse frequency agility
- monopulse angular glint decorrelation
- Barton/Sherman-style radar tracking error references
- public fallback source: radar handbook or JHU/APL technical digest if exact IEEE papers remain inaccessible

Must verify:

| Item | Required evidence |
|---|---|
| exact title | from IEEE Xplore / publisher / library |
| authors | exact spelling |
| year | exact |
| venue | journal/conference/book |
| DOI/pages | if available |
| claim relevance | does it actually state frequency agility reduces angular/glint tracking error? |

Manuscript use:

> Frequency agility has long been used in radar to decorrelate glint-like angular tracking errors ...

Do not use if:

- the paper is only about range resolution or waveform coding and not angular/glint error
- the source is a secondary blog or unsourced PDF

## Placeholder group B — frequency-hopped USBL

Current manuscript placeholders:

- `[FH_USBL_REF]`

Known candidate from prior local audit:

- “Acoustic positioning using a tetrahedral ultrashort baseline array of an acoustic modem source transmitting frequency-hopped sequences”
- reported candidate venue: JASA, 2007
- reported candidate DOI: `10.1121/1.2400616`
- reported candidate authors: Beaujean, Mohamed, Warin

Must verify:

| Item | Required evidence |
|---|---|
| exact title | publisher page |
| authors | publisher page |
| journal volume/issue/pages | publisher page |
| DOI | publisher page |
| method | frequency-hopped acoustic modem source + tetrahedral USBL? |
| distinction | waveform sequence / ML positioning, not our post-gating coherent DOA-bias whitening |

Manuscript use:

> Frequency-hopped acoustic modem signals have previously been used for USBL positioning ...

Do not claim:

> We are the first to use frequency hopping in USBL.

## Placeholder group C — Costas hopping USBL

Current manuscript placeholders:

- `[COSTAS_USBL_REF]`

Known candidate from prior local audit:

- “Optimizing baseline in USBL using Costas hopping to increase navigation precision in shallow water”
- reported candidate source: IEEE Xplore, document 9721736
- reported candidate year: 2022

Must verify:

| Item | Required evidence |
|---|---|
| exact title | IEEE Xplore |
| authors | IEEE Xplore |
| venue | IEEE conference/journal |
| DOI | IEEE Xplore |
| purpose | Costas hopping for baseline/time-delay/correlation precision? |
| distinction | not carrier-agile whitening of post-gating DOA bias in UKF tracking |

Manuscript use:

> Costas-hopping USBL designs have also been explored for shallow-water navigation precision ...

## Placeholder group D — frequency-comb iUSBL / underwater frequency diversity

Current manuscript placeholders:

- `[FREQ_COMB_REF]`

Known candidate families from prior local audit:

- passive inverted USBL based on acoustic frequency combs
- integrated acoustic frequency comb signal for underwater inverted USBL autonomous positioning
- MIMO sonar DOA estimation with transmitting diversity smoothing
- active sonar/radar frequency diversity receiver design

Must verify:

| Item | Required evidence |
|---|---|
| exact title/authors/year | publisher |
| system type | USBL, iUSBL, sonar, radar |
| frequency diversity role | waveform, comb, smoothing, receiver design |
| distinction | not our residual-whitening mechanism/boundary |

Manuscript use:

> Related underwater work has used frequency-diverse waveforms for positioning or sonar processing, but not for the specific post-gating coherent DOA-bias whitening mechanism studied here.

## Placeholder group E — USBL calibration / installation error

Potential citation need:

- Introduction or Discussion when contrasting our bias with installation/mounting error calibration.

Candidate literature:

- USBL calibration with dual transponders
- WTLS / least-squares installation error calibration
- roll/pitch/heading alignment error estimation

Must verify:

| Item | Required evidence |
|---|---|
| exact source | publisher |
| error type | installation/mounting/alignment |
| distinction | our residual remains even when installation error is not the modeled cause |

## Placeholder group F — CRLB / threshold effect

Potential citation need:

- Discussion of CRLB exceeding behavior and threshold/outlier effects.

Candidate literature:

- classical estimation threshold effect in sonar/radar
- bearing-only / TDOA CRLB in underwater localization

Must verify:

- whether the cited source supports threshold/outlier interpretation
- avoid implying our floor is the same as SNR threshold effect

## Audit status summary

| Group | Status | Priority |
|---|---|---|
| A radar frequency agility/glint | needs exact source | high |
| B JASA frequency-hopped USBL | candidate strong, verify original | high |
| C IEEE Costas USBL | candidate strong, verify original | high |
| D frequency-comb/frequency diversity | needs exact source | medium |
| E USBL calibration | needs exact source | medium |
| F CRLB/threshold | optional, if Discussion expands | low/medium |
