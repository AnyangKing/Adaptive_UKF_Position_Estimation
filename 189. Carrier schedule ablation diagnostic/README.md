# Carrier schedule ablation diagnostic

## Purpose

The review correctly noted that the phase-coverage rule \(\Delta F\delta \gtrsim 1\) is only a heuristic for a finite ping schedule. The paper therefore needs evidence that carrier count, span, and order are not being silently overclaimed.

This folder runs a compact paired 600 m static diagnostic:

- fixed 32 kHz
- linear20 30--34 kHz
- reverse20 34--30 kHz
- shuffled20 using the same carrier set
- narrow20 31--33 kHz
- sparse5 30--34 kHz repeated over 20 pings

## Claim boundary

Allowed:

> In this diagnostic seed set, the selected schedule is or is not robust to finite-schedule order/span/count changes.

Forbidden:

> The optimal carrier schedule has been solved.

This folder informs the next validation design; it is not the final schedule-optimization study.

