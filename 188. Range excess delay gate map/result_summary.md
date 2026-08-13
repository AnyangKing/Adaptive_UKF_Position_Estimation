# Range--excess-delay--gate result summary

| range m | direct ms | surface excess ms | surface in 5 ms gate | bottom excess ms | bottom in 5 ms gate | 184 hop gain m |
|---:|---:|---:|:---:|---:|:---:|---:|
| 0 | 6.67 | 40.00 | no | 80.00 | no | -0.534 |
| 100 | 67.00 | 14.38 | no | 42.34 | no | 0.195 |
| 200 | 133.50 | 7.76 | no | 25.52 | no | 0.083 |
| 300 | 200.11 | 5.26 | no | 17.86 | no | 1.076 |
| 400 | 266.75 | 3.97 | yes | 13.65 | no | 0.716 |
| 500 | 333.40 | 3.18 | yes | 11.02 | no | -1.698 |
| 600 | 400.06 | 2.66 | yes | 9.23 | no | 7.387 |
| 700 | 466.71 | 2.28 | yes | 7.93 | no | 5.408 |
| 800 | 533.37 | 2.00 | yes | 6.95 | no | 4.797 |
| 900 | 600.04 | 1.78 | yes | 6.19 | no | 6.380 |
| 1000 | 666.70 | 1.60 | yes | 5.58 | no | 8.755 |

## Interpretation

In this representative geometry, the surface reflection is outside the 5 ms DOA gate at 0--300 m and enters the gate by about 400 m. This is consistent with the diagnostic pattern from folder 184: carrier agility is weak or unstable at short/medium ranges and becomes strongly beneficial beyond about 600 m.

The bottom reflection remains outside the 5 ms gate throughout 0--1000 m in this representative geometry. Thus the dominant in-gate coherent reflection expected from this simple image-source map is the surface path, not the bottom path.

Because source depth is randomized in the simulations, this table should be used as a representative mechanism map rather than a replacement for per-trial metadata.
