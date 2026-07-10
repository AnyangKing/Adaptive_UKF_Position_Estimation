# v2 to v3 change log

## Applied from folder 93

### P1: Implementation parameters

Added a new Section 2.1 that records the code-audited implementation:

- eight-element two-ring USBL array,
- 33 mm ring radius and 79 mm vertical separation,
- 30 m receiver depth in a 100 m waveguide,
- 1500 m/s sound speed,
- 10 ms LFM chirp, 12 kHz bandwidth, 192 kHz sampling,
- direct + first-order surface/bottom image-source channel with Thorp absorption, Doppler, and colored ambient noise,
- matched-filter TOA, GCC-PHAT TDOA, SRP-PHAT DOA on the 5 ms gate,
- UKF `alpha=0.3`, `beta=2`, `kappa=0`, `dt=1 s`, process noise, initial covariance, and base measurement covariance.

### P2: Adaptive-R correction

Replaced the v2 binary covariance rule

```math
R_0 \; \mathrm{vs.} \; R_{\mathrm{inflated}}
```

with the actual two-stage implementation:

1. `s_k = min(100, 1 + (g_k/2)^2)` from GCC/SRP DOA disagreement.
2. DOA/TDOA block routing depending on the `5 deg` threshold.
3. Per-block NIS inflation using `chi^2_0.99` thresholds:
   - TOA-range: 6.63,
   - TDOA: 18.48,
   - DOA: 9.21.

This removes the only narrative/code mismatch identified in folder 93.

### P3: 5 ms gate

Added the missing 5 ms direct-path gate detail in two places:

- Section 2.1 observation extraction,
- Section 4 mechanism explanation.

The mechanism text now links the long-range carrier-locked bias to the fact that the surface-reflected excess delay falls inside the 5 ms gate at 600 m but not at shorter 100--200 m ranges.

### P4: Validation protocol details

Added protocol details without changing headline numbers:

- static validation: 20 pings, final 10-ping settled window, n=20 at 600 m, 100/200/400 m also run under the frozen protocol,
- moving validation: four motion conditions x 16 geometries = n=64,
- quasi-static sweep: static 12 + five speeds x two directions x 12 geometries = 132 paired trials,
- all validation experiments use the canonical direct+surface+bottom channel.

## English tightening

Light tightening was applied while inserting P1--P4:

- replaced vague "signal-consistency indicator" language with code-specific GCC/SRP disagreement wording,
- converted the mechanism paragraph into a gate/range explanation,
- turned protocol details into concise manuscript sentences rather than separate internal notes.

## Not changed

- Main title.
- Abstract claims.
- Static 600 m result: 13.01 m to 8.87 m, p = 0.0008.
- Moving result boundary: whitening yes, pooled RMSE gain no.
- Quasi-static continuous boundary: 0.005 m/s.
- Citation placeholders.
- Figure set and table bodies.

