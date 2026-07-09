# Safe contribution claims after folder 82

## One-sentence thesis

Frequency-agile pinging whitens carrier-locked coherent multipath DOA bias in shallow-water gated USBL measurements, yielding reproducible static long-range RMSE reduction while exposing a motion-dependent boundary for moving targets.

## Contribution C1 — post-gating bias floor

Safe claim:

> We characterize a long-range elevation-bias floor in compact shallow-water USBL localization that remains after direct-path gating and is amplified by the small array aperture.

Evidence:

- 37--57: repeated blind correction failures and bias-floor diagnosis
- 45: CRLB/excess floor
- 42: array rotation consistency
- 56--57: subgrid/ping-count limits

Avoid:

> The UKF itself is the main novelty.

Reason:

UKF fusion is the vehicle, not the core novelty. The stronger point is the physical bias floor and its mitigation.

## Contribution C2 — carrier-locked coherent mechanism

Safe claim:

> We show that part of the DOA bias is carrier-sensitive and can be explained by the interference phase `phi = 2*pi*f*delta` between the direct and in-gate reflected paths.

Evidence:

- 58: bias changes with carrier frequency
- 75: mechanism draft
- 72: system/mechanism concept figure

Avoid:

> Multipath is fully solved.

Reason:

Frequency agility reduces one coherent carrier-locked component. It does not remove aperture/geometry limits.

## Contribution C3 — static validation

Safe claim:

> With the carrier schedule fixed before validation, independent 600 m static experiments reduced settled RMSE from 13.01 m to 8.87 m (-32%, p = 0.0008).

Evidence:

- 61: static large-scale independent validation
- 76: Static Validation draft

Avoid:

> Sub-meter long-range USBL accuracy was achieved.

Reason:

The verified long-range error remains meter-scale. Sub-meter claims are not supported by the current compact aperture and channel conditions.

## Contribution C4 — moving and quasi-static boundary

Safe claim:

> Moving-target residuals are strongly whitened, but pooled RMSE improvement is not reliable; slow-drift validation supports a continuous quasi-static claim only up to 0.005 m/s under the current protocol.

Evidence:

- 63: lag-1 +0.470 to -0.208, p = 5.6e-10; pooled RMSE gain not significant
- 64--67: moving schedule safety attempts not reproduced
- 82: continuous quasi-static boundary only to 0.005 m/s

Avoid:

> Frequency-agile pinging is validated for quasi-static targets up to 0.100 m/s.

Reason:

82번에서 0.030/0.100 m/s는 양성이지만 0.010/0.050 m/s가 깨졌다. 따라서 0.100 m/s까지 단조적으로 검증됐다는 표현은 부정확하다.

## Prior-art positioning

Safe claim:

> The novelty is not the first use of frequency hopping or frequency diversity in USBL. The novelty is the mechanism-driven use of carrier agility to whiten post-gating coherent multipath DOA bias in a TOA/TDOA/DOA-UKF tracking loop, together with static validation and moving-target boundary analysis.

Must cite / distinguish:

- radar frequency agility / glint literature
- JASA 2007 frequency-hopped acoustic modem USBL
- IEEE 2022 Costas hopping USBL
- acoustic frequency-comb iUSBL / underwater frequency-diversity processing

Avoid:

> First frequency-hopping USBL method.

Reason:

Known prior work makes that claim unsafe.

## Recommended title direction

Strong and safe:

> Frequency-Agile Pinging for Whitening Coherent Multipath DOA Bias in Static Shallow-Water USBL Localization

Broader but still defensible:

> Carrier-Agile Whitening of Coherent Multipath DOA Bias in Shallow-Water USBL Tracking: Mechanism, Validation, and Boundary

Too broad:

> Frequency-Agile USBL Localization for Moving Underwater Targets

Reason:

Moving-target RMSE gain is not validated.
