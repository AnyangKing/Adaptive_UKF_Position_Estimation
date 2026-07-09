# Figure caption drafts

## Fig. 1

Conceptual geometry of carrier-agile whitening in compact shallow-water USBL localization. A direct arrival and an in-gate surface-reflected component can remain coherent after time gating. Under fixed-carrier transmission, the relative phase is nearly locked for static geometry, producing a repeatable DOA bias. Ping-to-ping carrier agility rotates the interference phase and whitens part of the residual before TOA/TDOA/DOA-UKF fusion.

## Fig. 2

Carrier sensitivity of the long-range elevation-bias component. The fixed 32 kHz case retains a larger median absolute bias at 600 m, while the 30--34 kHz carrier-agile average strongly reduces the carrier-locked component. This supports the interpretation that the post-gating residual contains a coherent frequency-dependent term.

## Fig. 3

Independent static 600 m validation of the frozen carrier-agile schedule. Mean settled RMSE decreased from 13.01 m under fixed 32 kHz transmission to 8.87 m under the 30--34 kHz ping-to-ping schedule, corresponding to a +4.14 m paired improvement (p = 0.0008).

## Fig. 4

Moving-target residual whitening and performance boundary. Carrier agility changed the elevation residual lag-1 correlation from +0.470 to -0.208 (p = 5.56e-10), but the pooled moving-target RMSE gain was not significant (-0.10 m, p = 0.301). The figure therefore supports a mechanism claim, not a moving-target RMSE-improvement claim.

## Fig. 5

Quasi-static speed sweep at 600 m. Static and 0.005 m/s drift were validated, whereas 0.010 and 0.050 m/s were not supported. Positive results at 0.030 and 0.100 m/s are treated as geometry-dependent recoveries rather than a continuous speed boundary. The conservative continuous boundary is 0.005 m/s under the present protocol.

## Fig. 6

Compact-aperture floor at long range. The 600 m empirical CRLB-scale reference is about 11.80 m, routed UKF is about 12.29 m, and NLS is about 13.38 m, showing that sub-meter long-range performance is not expected under the present geometry and noise assumptions. Carrier agility mitigates one coherent residual component; it does not remove the aperture/geometry floor.

