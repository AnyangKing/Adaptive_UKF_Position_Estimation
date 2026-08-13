# No-noise direct-path carrier control

## Question

Folder 185 removed explicit multipath but kept receiver noise. It unexpectedly retained a large carrier-agile gain at 1000 m.

This folder removes both explicit multipath and additive noise:

- `include_multipath = False`
- `include_noise = False`

If carrier hopping still helps, the benefit cannot be attributed only to coherent multipath phase rotation or colored noise. It must involve some carrier-dependent interaction in the measurement extraction / array manifold / numerical conditioning pipeline.

## Claim boundary

This is a mechanism control, not a new performance benchmark.

Allowed conclusion:

> The present simulator does or does not preserve a carrier-dependent long-range effect even when multipath and additive noise are disabled.

Forbidden conclusion:

> The real ocean will show the same no-noise/direct-only behavior.

