# Discussion and conclusion changes

## 1. Scope of the method was narrowed

Before:

`Carrier-agile pinging bypasses this limitation.`

After:

`Carrier-agile pinging targets the carrier-locked component of this limitation.`

Reason: the manuscript should not imply that the method solves the whole
long-range floor. The verified target is the carrier-locked coherent component.

## 2. Bias-removal language was softened

Before:

`The method lowers the temporal correlation of the bias and changes it into a
form that the UKF can average.`

After:

`The method lowers the temporal correlation of the observation residuals and
changes them into a form that the UKF can average more easily.`

Reason: the filter observes residuals. Saying that the bias itself is removed
would be stronger than the evidence supports.

## 3. Folders 160--162 were placed as limitations and future work

The manuscript now treats the later schedule experiments as evidence about
schedule-design risk, not as additional performance claims.

In particular:

- four-carrier sparse cycling failed independent static validation because one
  geometry diverged badly;
- sparse schedules may reduce some variance but can amplify tail risk;
- the transition TOA guard is a post-hoc pilot and must remain future work.

## 4. Real-water validation remains open

The Discussion now states that the current results come from controlled
shallow-water channel simulation. Real use would add sound-speed structure,
surface-state changes, synchronization error, and platform attitude variation.

Therefore, tank or real-water validation remains a professor-level decision:
either add it before submission or frame it as future work.

## 5. Conclusion wording was made claim-safe

Before:

`The main cause of the long-range error floor was confirmed to be post-gating
coherent multipath DOA bias.`

After:

`The long-range error floor was confirmed to be linked to post-gating coherent
multipath DOA bias.`

Reason: this avoids over-claiming that the whole floor has a single cause.

## Validation checklist

- No new number was introduced.
- No new performance claim was introduced.
- Moving-target RMSE improvement is not claimed.
- The quasi-static boundary is not expanded beyond 0.005 m/s.
- Results from folders 160--162 are not promoted into performance claims.
- No real-water performance result is claimed.
