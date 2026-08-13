# English claim diff

## Before

The English manuscript still said:

- moving-target residual correlation improved, but pooled RMSE did not improve reliably;
- moving-target use required future risk-aware scheduling;
- the paper was mainly a static/very-slow-drift observation-design paper.

That was correct for the 63--67 stage but outdated after 191.

## After

The English manuscript now says:

- plain hopping is still tail-prone and cannot be claimed as a general moving-target solution;
- the frozen transition-aware Adaptive-R rule passed an independent 0--1000 m moving-target validation;
- the moving claim is simulation-level and limited to the validated transition-aware protocol.

## Inserted numerical evidence

| Result | Value |
|---|---:|
| total paired cases | 528 |
| softR gain vs hop | +3.95 m |
| softR gain vs fixed | +4.80 m |
| p vs hop | 1.59e-22 |
| p vs fixed | 1.67e-30 |
| softR tail worsened vs hop | 0.028 |

## Still forbidden

- “validated in real water”
- “plain hopping solves moving USBL tracking”
- “works for arbitrary AUV motion”
- “frequency hopping itself is novel”

