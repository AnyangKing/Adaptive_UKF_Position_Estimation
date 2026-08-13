# No-noise direct-path control result summary

| distance | fixed mean | hop mean | mean gain | p | fixed div | hop div |
|---:|---:|---:|---:|---:|---:|---:|
| 600.0 | 10.329 | 7.031 | 3.298 | 0.02734 | 0.000 | 0.000 |
| 800.0 | 10.342 | 10.241 | 0.101 | 0.2734 | 0.000 | 0.000 |
| 1000.0 | 9.445 | 10.116 | -0.671 | 0.8086 | 0.000 | 0.000 |
| overall | 10.039 | 9.129 | 0.909 | 0.1146 | 0.000 | 0.000 |

## Interpretation

This control removes both explicit multipath and additive receiver noise.

If a carrier-agile advantage remains here, the manuscript must not attribute all long-range improvement to multipath phase diversification or colored noise.

If the advantage disappears here but remains in folder 185, additive noise / extraction-noise interaction becomes the more likely residual mechanism.

## Actual finding

The large 1000 m direct-only carrier-agile gain observed in folder 185 did **not** survive when additive noise was disabled.

- 600 m: hop improved mean settled RMSE by +3.298 m (p=0.0273), but with only n=8 this is a mechanism clue, not a final performance claim.
- 800 m: nearly neutral (+0.101 m, p=0.273).
- 1000 m: hop was slightly worse (-0.671 m, p=0.809).
- Overall: positive but non-significant (+0.909 m, p=0.115).

## Consequence for the paper

Together with folder 185, this implies that the residual direct-only 1000 m gain is not a deterministic carrier effect in the noiseless direct path. It is more consistent with carrier-dependent interaction between noise, matched-filter/GCC/SRP extraction, and long-range small-aperture conditioning.

Therefore the manuscript should not say:

> Carrier agility improves long-range USBL only by rotating coherent multipath phase.

The safer claim is:

> In the current signal-level simulator, carrier agility changes the temporal/error structure of extracted TOA/TDOA/DOA observations under long-range shallow-water conditions. The dominant improvement is consistent with coherent multipath decorrelation, but direct-only/noisy controls show that carrier-dependent observation-extraction/noise interactions also contribute and must be isolated in future high-fidelity validation.

## Next control implied

The next highest-value control is not another no-noise run. It is a paired carrier schedule ablation:

- same geometry/channel/noise seed,
- same carrier span but different order,
- smaller/larger carrier spans,
- smaller/larger number of hops.

That test targets the reviewer's concern that ΔFδ is only a heuristic and that finite carrier scheduling may matter.
