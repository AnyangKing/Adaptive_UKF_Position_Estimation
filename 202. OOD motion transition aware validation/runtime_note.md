# Runtime note

## Initial plan

The first OOD design used:

$$
5 \text{ distances} \times 4 \text{ OOD conditions} \times 1 \text{ seed}
= 20 \text{ paired cases}
$$

In the current execution environment this was too slow for an interactive Codex turn.

## Measured runtime

A representative OOD case with all three policies took about 19 seconds.

Therefore:

$$
20 \times 19 \text{ s} \approx 380 \text{ s}
$$

The run was interrupted and resized.

## Final run

The final first-pass OOD probe used:

$$
3 \text{ distances} \times 4 \text{ OOD conditions} \times 1 \text{ seed}
= 12 \text{ paired cases}
$$

Distances:

- 400 m
- 800 m
- 1000 m

This keeps the test focused on mid/long-range conditions where compact USBL DOA errors matter most.

## Future full-scale option

For a larger OOD validation, add checkpoint/resume support so each completed case is written immediately. Then run the full design outside an interactive turn or overnight.
