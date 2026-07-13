# Manuscript related-work patch suggestions

These are safe text patches for `paper/manuscript.tex`. They are **not** applied in this folder because
the current table is already acceptable and extra text may affect IEEE column layout.

## Suggested replacement: Costas row

Current idea:

> Costas / hopped USBL shallow-water designs ... improve correlation, time-delay, or navigation precision ...

Safer, more specific version:

> Costas / hopped USBL shallow-water designs use intra-ping waveform diversity to sharpen the
> autocorrelation peak and improve TOA/time-delay or baseline-related navigation precision. They do
> not target the temporal correlation of post-gating DOA elevation bias; our method instead changes
> the carrier across pings to rotate the direct/reflected interference phase before UKF fusion.

## Suggested replacement: frequency-comb row

Current idea:

> Frequency diversity is used, but the system role and residual mechanism differ.

Safer, more specific version:

> Acoustic frequency-comb iUSBL uses coherent multi-frequency signals for integrated positioning and
> communication. Its multipath handling is not carrier-agile whitening of DOA residuals; the present
> work uses a simple ping-to-ping carrier schedule to whiten a gated USBL DOA-bias component.

## Suggested Related Work paragraph

Frequency-diverse acoustic signals have already been used in underwater positioning. Frequency-hopped
modem USBL uses communication waveforms for source localization, Costas-based USBL uses intra-ping
waveform diversity to improve correlation and time-delay precision, and frequency-comb iUSBL uses
coherent multi-frequency signals for integrated positioning and communication. These works motivate
frequency diversity in underwater acoustics, but they address different failure modes. The present
study begins from a post-gating error analysis of a compact TOA/TDOA/DOA-UKF USBL tracker and targets
the carrier-locked temporal correlation of coherent multipath DOA bias.

## Do-not-add sentence

Never add:

> Unlike all previous work, this is the first frequency-hopping USBL method.

This would be false and reviewer-fragile.
