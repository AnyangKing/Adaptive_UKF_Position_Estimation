# Carrier schedule ablation result summary

| schedule | mean RMSE | gain vs fixed | p | improved frac | tail worsened |
|---|---:|---:|---:|---:|---:|
| fixed32 | 12.050 | 0.000 |  |  |  |
| linear20_30_34 | 10.471 | 1.579 | 0.2734 | 0.500 | 0.500 |
| reverse20_34_30 | 10.176 | 1.873 | 0.2734 | 0.500 | 0.500 |
| shuffled20_30_34 | 9.891 | 2.159 | 0.2734 | 0.625 | 0.500 |
| narrow20_31_33 | 10.950 | 1.100 | 0.3203 | 0.625 | 0.500 |
| sparse5_30_34_repeat | 10.056 | 1.994 | 0.1914 | 0.625 | 0.375 |

## Interpretation

This is a compact schedule diagnostic at one range, not a final optimization study.

The main question is whether the manuscript should describe the 30--34 kHz linear schedule as a frozen validated schedule, a generally optimal schedule, or only one workable schedule inside a broader design space.

## Actual finding

All tested non-fixed schedules had lower mean settled RMSE than fixed32 in this n=8 diagnostic, but none reached a strong paired significance level.

- linear20 30--34 kHz: +1.579 m mean gain, p=0.273.
- reverse20 34--30 kHz: +1.873 m mean gain, p=0.273.
- shuffled20 same carrier set: +2.159 m mean gain, p=0.273.
- narrow20 31--33 kHz: +1.100 m mean gain, p=0.320.
- sparse5 30--34 kHz repeated: +1.994 m mean gain, p=0.191.

The diagnostic therefore supports a conservative manuscript claim:

> The validated 30--34 kHz linear schedule is one frozen carrier-agile schedule used for controlled comparisons, not an optimized or unique schedule. Finite schedule order, span, and count remain part of the design space.

## Consequence for the paper

The phase-coverage heuristic should stay as a design intuition only. The manuscript must not state that \(\Delta F\delta \gtrsim 1\) guarantees zero-mean residuals or schedule optimality in finite ping windows.
