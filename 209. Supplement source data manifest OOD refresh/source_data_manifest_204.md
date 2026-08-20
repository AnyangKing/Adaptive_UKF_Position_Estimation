# Source-data manifest for 204 OOD moving validation

## Manuscript claim supported

204 supports the following limited claim:

> In the current signal-level simulator, the frozen transition-aware soft-R protocol improves aggregate OOD moving-target robustness relative to fixed carrier and plain hopping, as measured by mean RMSE, P90 RMSE, and divergence rate.

It does not support:

- real-water performance,
- arbitrary-motion performance,
- hardware frequency-response robustness,
- a claim that plain carrier hopping alone solves moving-target tracking.

## Source folders and files

| item | local source | role |
|---|---|---|
| OOD runner | `203. Overnight OOD validation runner/` | checkpoint/resume execution harness and raw run outputs |
| OOD aggregate result | `204. Overnight OOD validation aggregate result/compact_metrics.json` | authoritative aggregate metrics |
| OOD result summary | `204. Overnight OOD validation aggregate result/result_summary.md` | human-readable summary |
| OOD interpretation | `204. Overnight OOD validation aggregate result/interpretation.md` | claim boundary and interpretation |

## Manuscript table mapping

| manuscript entry | source value |
|---|---:|
| fixed mean RMSE | 10.832 m |
| fixed P90 RMSE | 22.339 m |
| fixed divergence | 0.049 |
| plain hop mean RMSE | 10.691 m |
| plain hop P90 RMSE | 21.611 m |
| plain hop divergence | 0.057 |
| soft-R mean RMSE | 7.809 m |
| soft-R P90 RMSE | 15.936 m |
| soft-R divergence | 0.006 |
| soft-R vs hop mean gain | 2.881 m |
| soft-R vs hop p-value | 9.076e-22 |
| soft-R vs fixed mean gain | 3.023 m |
| soft-R vs fixed p-value | 1.015e-18 |

## Protocol metadata

- OOD families: accelerating radial, curved arc, mixed radial+tangential, vertical sine maneuver.
- Distances: 0, 100, ..., 1000 m.
- Repeats: 12 seeds per distance/family.
- Total: 528 paired cases.
- Policies: fixed carrier, plain hop, transition-aware soft-R.
- Pairing: same trajectory, channel, and noise seeds across policies.
