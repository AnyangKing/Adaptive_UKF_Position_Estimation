# Search query plan

Use these queries in IEEE Xplore, Google Scholar, Scopus, Web of Science, and the university library.

## Radar frequency agility / glint

Primary queries:

```text
"frequency agility" radar glint angle error
"frequency-agility" "glint" radar tracking error
"pulse-to-pulse frequency agility" radar glint
"frequency agility" "monopulse" "glint"
"radar tracking errors" "frequency agility" "glint"
```

Fallback queries:

```text
Barton radar glint frequency agility
Sherman radar glint frequency agility
"glint pointing error" "frequency agility"
"frequency-agility processing" "radar glint"
```

What to capture:

- exact title
- authors
- venue/year/pages/DOI
- one sentence proving relevance

## Frequency-hopped USBL / acoustic modem source

Primary queries:

```text
"Acoustic positioning using a tetrahedral ultrashort baseline array"
"frequency-hopped sequences" "ultrashort baseline"
"tetrahedral ultrashort baseline" "acoustic modem"
"10.1121/1.2400616"
```

Expected candidate:

```text
Acoustic positioning using a tetrahedral ultrashort baseline array of an acoustic modem source transmitting frequency-hopped sequences
```

What to capture:

- exact JASA metadata
- whether it estimates azimuth/elevation/position
- whether it uses ML or waveform sequence processing

## Costas hopping USBL

Primary queries:

```text
"Optimizing baseline in USBL using Costas hopping"
"Costas hopping" USBL shallow water
"Costas" "ultra-short baseline" navigation precision
"9721736" "USBL" "Costas"
```

What to capture:

- exact IEEE metadata
- whether it is a conference paper or journal paper
- whether it optimizes baseline/correlation/time-delay precision

## Acoustic frequency comb / iUSBL

Primary queries:

```text
"acoustic frequency comb" "ultrashort baseline"
"acoustic frequency comb" "inverted USBL"
"Passive Inverted Ultrashort Baseline" "acoustic frequency comb"
"Integrated Acoustic Frequency Comb Signal" underwater inverted ultra-short baseline
```

What to capture:

- exact title and authors
- system type: USBL or inverted USBL
- role of frequency comb

## Sonar frequency diversity / MIMO transmitting diversity

Primary queries:

```text
"frequency diversity" active sonar radar optimal receiver design
"MIMO sonar" "transmitting diversity smoothing" DOA
"transmitting diversity smoothing" sonar DOA estimation
"frequency diversity" sonar DOA estimation
```

What to capture:

- whether it is about DOA estimation, receiver design, or waveform diversity
- how it differs from our UKF tracking residual whitening

## USBL calibration / installation error

Primary queries:

```text
USBL calibration installation error roll pitch heading
"ultra short baseline" calibration transducer attitude error
"USBL" "installation error" "weighted total least squares"
"USBL calibration" dual transponder
```

Use only if Introduction/Discussion contrasts our residual with conventional installation-error calibration.

## Search logging format

For each source, record:

```text
Query:
Database:
Result title:
Authors:
Venue/year:
DOI/link:
Relevant claim:
Difference from our work:
Use in manuscript:
Verified by:
Date:
```
