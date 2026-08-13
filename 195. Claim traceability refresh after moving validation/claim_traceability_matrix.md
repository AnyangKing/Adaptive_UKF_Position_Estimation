# Claim traceability matrix

| Manuscript claim | Evidence folder | Status | Notes |
|---|---|---|---|
| Static 600 m fixed 13.01 m -> agile 8.87 m, gain 4.14 m, p=0.0008 | `61. 정지표적 도약 대규모 독립검증` | supported | Main static performance claim. |
| Carrier-agile residual is carrier-sensitive and mechanism is coherent/two-ray-like | `58`, `137`, `145`, `188` | supported with limits | Mechanism evidence, not a formal complete ocean-acoustic proof. |
| Plain hopping reduces positive moving lag-1 residual correlation but does not prove moving RMSE gain | `63`, `64--67` | supported | Kept as failure/boundary result. |
| Transition-aware Adaptive-R improves 600 m moving target after frozen validation | `181. Transition aware Adaptive R independent moving validation` | supported | Precursor to 191 full-range validation. |
| Transition-aware Adaptive-R improves 0--1000 m moving validation: +3.95 m vs hop, +4.80 m vs fixed, n=528 | `191. Moving full range transition aware independent validation` | supported | Current moving-target simulation performance claim. |
| 800 m is a failure-and-recovery example: fixed 17.70, hop 22.39, softR 10.83 m | `191. Moving full range transition aware independent validation` | supported | Good figure/caption anchor. |
| Quasi-static continuous boundary is only up to 0.005 m/s | `82. 준정지 속도 경계 검증 실행` | supported | Higher-speed positive cases are non-continuous and not generalized. |
| Direct-path-only controls prevent over-attributing all gain to explicit multipath | `185`, `187` | supported | Keeps mechanism claim cautious. |
| Schedule is frozen and not globally optimal | `189`, `191 config` | supported | 30--34 kHz is validated, not claimed optimal. |
| Runtime claim: UKF update cost is small relative to observation extraction | `177` | supported | Simulation generation excluded from online filter timing. |

## Claims still forbidden

- Validated in real water.
- Guaranteed for arbitrary AUV trajectories.
- Plain hopping alone solves moving-target USBL tracking.
- Frequency hopping itself is first proposed here.
- CRLB-excess reference is a formal bias floor.
- 162 post-hoc guard pilot is an independent performance claim.

