# Table 2 draft: Numerical results summary

## Manuscript caption draft

Table 2. Summary of positive and negative validation results. Positive RMSE gains are reported as fixed-carrier RMSE minus carrier-agile RMSE; positive values therefore favor carrier agility.

## Table body draft

| Regime / test | Baseline | Carrier-agile or tested condition | Main metric | Result | Decision for manuscript |
|---|---|---|---|---|---|
| Static, 600 m independent validation | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Settled RMSE | 13.01 m to 8.87 m; gain +4.14 m; p = 0.0008 | Main positive performance claim. |
| Static, 600 m median behavior | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Median settled RMSE | 13.97 m to 7.96 m | Supports robust static improvement, but keep mean/p-value as primary. |
| Moving target, 600 m pooled RMSE | Fixed 32 kHz | Frequency-agile schedule | Pooled RMSE gain | gain -0.10 m; p = 0.301 | Do not claim moving-target RMSE improvement. |
| Moving target mechanism check | Fixed 32 kHz | Frequency-agile schedule | Elevation residual lag-1 correlation | +0.470 to -0.208; p = 5.56e-10 | Mechanism whitening is supported even when RMSE gain is not. |
| Moving target adaptive/sparse schedules | Fixed 32 kHz | R-inflation, jump gate, anchor-hop, condition-aware schedules | RMSE / tail behavior | No reproducible general-purpose moving improvement across 64--67 | Keep as limitation/future work. |
| Quasi-static sweep, all speeds pooled | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 11.98 m to 10.49 m; gain +1.49 m; p = 8.00e-05 | Useful supporting result, but not a broad speed-boundary claim. |
| Quasi-static mechanism sweep | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Elevation residual lag-1 correlation | +0.220 to -0.100; p = 9.17e-08 | Confirms whitening across the sweep. |
| Quasi-static 0.000 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 11.95 m to 8.62 m; gain +3.32 m; p = 0.0134 | Static/near-static validated. |
| Quasi-static 0.005 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 11.14 m to 9.72 m; gain +1.42 m; p = 0.0447 | Conservative continuous quasi-static boundary. |
| Quasi-static 0.010 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 12.13 m to 12.35 m; gain -0.22 m; p = 0.2031 | Boundary not supported. |
| Quasi-static 0.030 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 10.18 m to 8.19 m; gain +1.99 m; p = 0.0022 | Positive but non-continuous; discuss as geometry-dependent recovery, not speed boundary. |
| Quasi-static 0.050 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 12.35 m to 12.39 m; gain -0.04 m; p = 0.4498 | Not supported. |
| Quasi-static 0.100 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 14.12 m to 10.75 m; gain +3.38 m; p = 0.0048 | Positive but non-continuous; do not present as "validated to 0.1 m/s." |
| Long-range floor comparison | Empirical CRLB-scale reference | Routed UKF / NLS | Error scale at 600 m | CRLB-scale 11.80 m; routed UKF 12.29 m; NLS 13.38 m; residual floor about 3.45 m | Explains why sub-meter 600 m performance is not expected with the compact aperture. |

## Text to use below the table

The non-monotonic quasi-static results are important. They show that the carrier-agile schedule can remain beneficial beyond 0.005 m/s in some geometries, but the present evidence does not support a continuous speed boundary above 0.005 m/s. The manuscript should therefore describe the validated operating region as static to very slow drift, with higher-speed recoveries treated as geometry-dependent observations.

