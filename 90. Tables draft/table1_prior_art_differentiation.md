# Table 1 draft: Prior-art differentiation

## Manuscript caption draft

Table 1. Positioning of the present work relative to related frequency-diverse and USBL localization literature. The distinction claimed here is not the first use of frequency hopping in USBL, but the identification and validation of carrier-agile whitening for post-gating coherent multipath DOA bias in a TOA/TDOA/DOA-UKF tracking loop.

## Table body draft

| Literature family | Frequency diversity used? | USBL positioning? | Main purpose in prior work | Post-gating coherent DOA-bias whitening? | TOA/TDOA/DOA-UKF tracking boundary quantified? | How this paper differs |
|---|---:|---:|---|---:|---:|---|
| Radar frequency agility / glint reduction | Yes | No | Decorrelate radar angular/glint tracking errors | Partly analogous, but not underwater USBL multipath | No | We cite this as the closest physical analogy, then narrow the claim to shallow-water USBL and surface-reflection-induced coherent DOA residuals. |
| Frequency-hopped acoustic modem USBL | Yes | Yes | Use frequency-hopped acoustic modem sequences for positioning | Not established as the target mechanism | No | Prior existence prevents a "first FH USBL" claim; our contribution is the residual-whitening mechanism and validation boundary. |
| Costas / hopped USBL shallow-water designs | Yes | Yes | Improve correlation, time-delay, or navigation precision | Not the stated mechanism | No | Related waveform diversity exists, but does not isolate carrier-locked post-gating DOA bias entering a UKF tracker. |
| Acoustic frequency-comb / iUSBL approaches | Yes | Often iUSBL or related positioning | Use comb/frequency-diverse signals for positioning or processing | Not the stated mechanism | No | Frequency diversity is used, but the system role and residual mechanism differ. |
| USBL calibration / installation-error correction | Usually no | Yes | Estimate mounting, alignment, or calibration errors | No | No | Calibration removes static system errors; here the residual remains tied to carrier-sensitive propagation/interference after gating. |
| Present work | Yes, ping-to-ping carrier agility | Yes, compact 8-sensor USBL | Change the temporal structure of the residual entering TOA/TDOA/DOA-UKF fusion | Yes | Yes | Static 600 m improvement is validated; moving/quasi-static boundary is explicitly reported, including negative results. |

## Required citation placeholders

- `[RADAR_FREQ_AGILITY_REF]`
- `[FH_USBL_REF]`
- `[COSTAS_USBL_REF]`
- `[FREQ_COMB_REF]`
- optional USBL calibration reference

## Reviewer-defense note

If a reviewer says "frequency agility is old," the answer should be:

> Correct. The paper does not claim frequency agility itself is new. It uses that prior principle as a starting point and contributes an underwater USBL-specific mechanism, a static long-range validation, and a moving/quasi-static applicability boundary.

