# Direct-only control result summary

| distance | fixed mean | hop mean | mean gain | p | fixed div | hop div |
|---:|---:|---:|---:|---:|---:|---:|
| 600.0 | 6.479 | 6.221 | 0.257 | 0.7266 | 0.000 | 0.000 |
| 800.0 | 12.397 | 12.710 | -0.313 | 0.5273 | 0.000 | 0.000 |
| 1000.0 | 16.057 | 9.635 | 6.422 | 0.01172 | 0.000 | 0.000 |
| overall | 11.644 | 9.522 | 2.122 | 0.06776 | 0.000 | 0.000 |

## Interpretation

If the main carrier-agile benefit is caused by in-gate coherent multipath phase rotation, the direct-only channel should not reproduce the large long-range gains seen in the multipath channel.

This control must be read together with 61/182/184; it is not a new performance claim.

## Actual finding

The direct-only control did not cleanly remove the carrier-agility gain at all ranges.

- 600 m: small and non-significant gain (+0.257 m, p=0.727).
- 800 m: small negative gain (-0.313 m, p=0.527).
- 1000 m: large positive gain (+6.422 m, p=0.0117).
- Overall: positive but not conventionally significant (+2.122 m, p=0.0678).

## Consequence for the paper

This result weakens a pure attribution claim that all long-range carrier-agile gain comes from in-gate coherent multipath phase rotation. At 1000 m, other carrier-dependent effects remain possible even without explicit multipath:

- matched-filter/SRP numerical behavior at different center frequencies,
- colored-noise interaction with the chirp band,
- aperture-in-wavelength and array manifold effects,
- range-dependent DOA conditioning,
- frequency-dependent absorption/SNR differences.

Therefore the manuscript should say:

> Carrier-agile improvement is consistent with coherent multipath phase diversification, but the current simulation also leaves carrier-dependent estimator and noise-response effects that require additional controls.

## Next required controls

1. Frequency-dependent SNR equalization.
2. Phase-randomized reflection control.
3. Fixed-array-manifold or normalized SRP response control.
4. Carrier count/span/order ablation.
