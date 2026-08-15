# Runtime note

## Attempted full-grid execution

The initial plan was a full 528-case sensitivity grid:

$$
528 \text{ cases} \times 9 \text{ variants}
$$

That was too slow in the current Windows/Codex execution environment. A 15-minute execution did not complete.

## Measured cost

A single case with all 9 variants took about 9.5 seconds. Therefore:

$$
528 \times 9.5 \text{ s} \approx 5016 \text{ s} \approx 84 \text{ min}
$$

This explains why the full-grid run was not practical inside the current turn.

## Adopted compromise

The final 201 run uses a first-pass subset:

$$
6 \text{ distances} \times 4 \text{ conditions} \times 1 \text{ seed}
= 24 \text{ cases per variant}
$$

This is enough to detect an obvious parameter brittleness signal, but not enough to replace a full robustness validation.

## Future full-scale option

If a full sensitivity result is needed later, the right path is not to keep blocking Codex turns. Instead:

1. add checkpoint/resume to the script,
2. write partial results after each case,
3. run overnight or in a separate terminal,
4. aggregate once all variants finish.
