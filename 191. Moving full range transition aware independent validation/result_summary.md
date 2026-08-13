# Moving full-range independent validation result summary

## Overall paired comparisons

| comparison | mean gain | p | improved frac | tail worsened | n |
|---|---:|---:|---:|---:|---:|
| softR_vs_hop | 3.948 | 1.585e-22 | 0.409 | 0.028 | 528 |
| softR_vs_fixed | 4.797 | 1.671e-30 | 0.693 | 0.131 | 528 |
| hop_vs_fixed | 0.849 | 1.336e-07 | 0.593 | 0.214 | 528 |

## Distance breakdown

| distance | fixed | hop | softR | hop gain vs fixed | softR gain vs hop | softR gain vs fixed | softR tail worsened vs hop |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 4.445 | 4.700 | 4.700 | -0.255 | -0.000 | -0.255 | 0.000 |
| 100 | 1.733 | 1.656 | 1.581 | 0.077 | 0.075 | 0.152 | 0.000 |
| 200 | 8.935 | 8.792 | 3.959 | 0.143 | 4.833 | 4.976 | 0.000 |
| 300 | 10.086 | 8.758 | 4.513 | 1.328 | 4.245 | 5.573 | 0.000 |
| 400 | 11.840 | 9.802 | 5.511 | 2.037 | 4.292 | 6.329 | 0.021 |
| 500 | 14.140 | 11.302 | 6.342 | 2.838 | 4.960 | 7.798 | 0.021 |
| 600 | 14.738 | 13.252 | 8.381 | 1.486 | 4.872 | 6.358 | 0.021 |
| 700 | 14.821 | 12.594 | 9.110 | 2.228 | 3.483 | 5.711 | 0.104 |
| 800 | 17.696 | 22.386 | 10.828 | -4.690 | 11.557 | 6.867 | 0.042 |
| 900 | 17.420 | 16.671 | 12.292 | 0.749 | 4.379 | 5.128 | 0.062 |
| 1000 | 18.189 | 14.792 | 14.062 | 3.397 | 0.730 | 4.127 | 0.042 |

## Interpretation boundary

This is an independent full-range validation under the current signal-level simulator. It supports simulation-level moving-target claims only, not real-water generalization.

## Actual finding

The full-range independent moving validation supports the transition-aware Adaptive-R line.

- Plain carrier hopping is only mildly better than fixed overall:
  - hop vs fixed mean gain: +0.849 m
  - p = 1.336e-07
  - tail worsened fraction = 0.214
  - important caveat: hop is strongly harmful at 800 m in this validation set.
- Transition-aware softR is substantially better than plain hopping:
  - softR vs hop mean gain: +3.948 m
  - p = 1.585e-22
  - tail worsened fraction = 0.028
- Transition-aware softR is also substantially better than fixed:
  - softR vs fixed mean gain: +4.797 m
  - p = 1.671e-30
  - improved fraction = 0.693
  - tail worsened fraction = 0.131

## Distance-level reading

- 0 m is a near-vertical degenerate range condition and should not be used as positive evidence.
- 100 m shows only small differences.
- 200--700 m shows stable softR recovery relative to both fixed and hop.
- 800 m is the clearest failure-and-recovery case:
  - fixed: 17.696 m
  - hop: 22.386 m
  - softR: 10.828 m
  - hop worsens fixed by -4.690 m, but softR recovers +6.867 m over fixed.
- 900--1000 m remains positive vs fixed, but the softR-vs-hop gain narrows at 1000 m because hop itself is already better than fixed there.

## Manuscript claim candidate

Allowed after this folder:

> In an independent 0--1000 m moving-target simulation validation with 528 paired cases, plain carrier hopping remained tail-prone, whereas the frozen transition-aware Adaptive-R rule reduced settled RMSE by 3.95 m relative to the hopped baseline and 4.80 m relative to fixed-carrier tracking.

Still forbidden:

> The method is validated in real water.

Still needs care:

> The claim is under the current shallow-water signal-level simulator and the frozen 30--34 kHz carrier schedule. Broader environmental and hardware frequency-response validation remains future work.
