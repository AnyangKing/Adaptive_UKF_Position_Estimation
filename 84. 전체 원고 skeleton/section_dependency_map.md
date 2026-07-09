# Section dependency map

## High-level dependency tree

```text
Original idea: TOA/TDOA/DOA + UKF
  -> adaptive-R routing backbone
  -> long-range bias floor diagnosis
  -> carrier-sensitive coherent residual mechanism
  -> frequency-agile pinging method
  -> static validation
  -> moving/quasi-static boundary
  -> bounded SCI paper
```

## Section-to-folder mapping

| Manuscript section | Main folders | Role |
|---|---|---|
| Introduction | 68, 73, 78, 83 | prior-art-safe novelty framing |
| System and signal model | 2, 4, 22, 23, 43 | array/channel/measurement/UKF foundation |
| Post-gating bias floor | 37, 38, 42, 45, 47, 49--57 | why filtering alone is insufficient |
| Carrier-sensitive mechanism | 58, 72, 75 | `phi = 2*pi*f*delta` physical mechanism |
| Frequency-agile method | 58, 60, 61 | frozen carrier schedule and UKF integration |
| Static validation | 60, 61, 76 | primary performance result |
| Moving/quasi-static boundary | 59, 62, 63, 64--67, 77, 82 | mechanism survives, performance boundary |
| Discussion | 78, 79, 82, 83 | prior-art defense, limitation, deployment |
| Conclusion | 80, 83 | bounded conclusion and future work |

## Numerical source of truth

| Number | Value | Folder |
|---|---:|---|
| static fixed 600 m RMSE | 13.01 m | 61 |
| static hop 600 m RMSE | 8.87 m | 61 |
| static improvement | -32%, p = 0.0008 | 61 |
| static median fixed/hop | 13.97 m / 7.96 m | 61 |
| moving lag-1 fixed/hop | +0.470 / -0.208 | 63 |
| moving lag-1 p | 5.6e-10 | 63 |
| moving pooled RMSE gain | -0.10 m, p = 0.301 | 63 |
| quasi-static sweep overall | 11.98 m to 10.49 m, p = 8.00e-05 | 82 |
| continuous quasi-static boundary | 0.005 m/s | 82 |
| empirical CRLB at 600 m | 11.80 m | 45/79 |
| routed UKF at 600 m | 12.29 m | 45/79 |
| residual floor | 3.45 m | 45/79 |

## Claims that require citation before submission

1. Radar frequency agility / glint decorrelation prior art.
2. JASA 2007 frequency-hopped acoustic modem USBL.
3. IEEE 2022 Costas hopping USBL.
4. Acoustic frequency-comb iUSBL.
5. Underwater frequency diversity / MIMO sonar transmitting diversity.
6. General USBL calibration literature for installation error distinction.

## Claims that are internally supported by this project

1. Fixed carrier creates persistent long-range DOA bias in the simulated shallow-water gated USBL setting.
2. Bias is carrier-sensitive.
3. Frequency agility whitens residual DOA error.
4. Static 600 m RMSE reduction is reproducible.
5. Moving-target RMSE improvement is not reliable.
6. Quasi-static continuous boundary is only 0.005 m/s under the 82번 protocol.
