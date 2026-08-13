# Moving full-range diagnostic result summary

## Overall paired comparisons

| comparison | mean gain | p | improved frac | tail worsened | n |
|---|---:|---:|---:|---:|---:|
| softR_vs_hop | 4.186 | 4.188e-06 | 0.424 | 0.038 | 132 |
| softR_vs_fixed | 4.255 | 1.16e-07 | 0.682 | 0.152 | 132 |
| hop_vs_fixed | 0.069 | 0.1706 | 0.523 | 0.258 | 132 |

## Distance breakdown

| distance | fixed | hop | softR | hop gain vs fixed | softR gain vs hop | softR gain vs fixed | softR tail worsened vs hop |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.480 | 1.937 | 1.937 | -0.457 | -0.000 | -0.457 | 0.000 |
| 100 | 1.525 | 1.561 | 1.578 | -0.036 | -0.016 | -0.052 | 0.000 |
| 200 | 5.412 | 5.935 | 3.652 | -0.523 | 2.283 | 1.760 | 0.000 |
| 300 | 13.774 | 10.255 | 6.096 | 3.519 | 4.159 | 7.678 | 0.083 |
| 400 | 7.809 | 8.035 | 6.883 | -0.226 | 1.152 | 0.926 | 0.000 |
| 500 | 12.588 | 13.941 | 7.147 | -1.353 | 6.793 | 5.440 | 0.083 |
| 600 | 10.358 | 10.723 | 9.002 | -0.366 | 1.721 | 1.356 | 0.083 |
| 700 | 21.114 | 21.106 | 12.858 | 0.008 | 8.248 | 8.256 | 0.083 |
| 800 | 15.666 | 22.763 | 12.516 | -7.097 | 10.247 | 3.151 | 0.000 |
| 900 | 22.025 | 17.028 | 12.564 | 4.997 | 4.465 | 9.462 | 0.000 |
| 1000 | 24.566 | 22.275 | 15.286 | 2.291 | 6.989 | 9.280 | 0.083 |

## Interpretation boundary

This is a low-n distance diagnostic. It should guide the next independent validation grid, not replace it.

## Actual finding

This diagnostic supports continuing the moving-target line.

- Plain carrier hopping did not materially improve the moving target overall:
  - hop vs fixed mean gain: +0.069 m
  - p = 0.1706
  - tail worsened fraction = 0.258
- The folder-181 transition-aware softR rule improved over hop:
  - softR vs hop mean gain: +4.186 m
  - p = 4.188e-06
  - tail worsened fraction = 0.038
- The same softR rule also improved over fixed overall:
  - softR vs fixed mean gain: +4.255 m
  - p = 1.16e-07
  - tail worsened fraction = 0.152

The distance pattern is also important:

- 0--100 m: softR does not help and can be slightly worse. These near-range cases should not be used as positive evidence.
- 200--600 m: softR tends to recover some of the hop/fixed degradation, but the gains are uneven.
- 700--1000 m: softR produces the largest mean gains, especially where plain hop becomes tail-prone.

## Consequence for the paper

The current moving-target story should be:

> Plain carrier agility is not a reliable moving-target solution. However, a transition-aware Adaptive-R rule using only runtime-observable quantities is a promising recovery mechanism, and the first 0--1000 m diagnostic shows the strongest benefit at long range.

It should not yet be:

> Moving-target 0--1000 m performance is finally validated.

The next required step is a larger independent validation with at least n=12 per distance/condition, or a reduced high-value range set if runtime is too large.
