# Manuscript positioning for carrier schedule

## 현재 원고에서 안전한 문장

> The frequency-agile policy uses a simple frozen 20-ping linear sweep over 30–34 kHz. The schedule
> is used to test the carrier-locked residual-whitening mechanism; it is not claimed to be globally
> optimal.

## Discussion에 넣을 수 있는 문장

> The 30–34 kHz schedule was deliberately kept simple and frozen before validation. Future work
> should ablate hop span, number of carriers, deterministic versus randomized ordering, and sparse
> anchor-hop schedules to separate mechanism robustness from schedule-specific effects.

## Reviewer response

If reviewer asks why 30–34 kHz:

> We selected a narrow band around the 32 kHz baseline so that the receiver-side processing and
> array operating regime remained unchanged while the direct/reflected interference phase was
> rotated across pings. We do not claim this span is optimal; the validation tests whether a frozen
> carrier-agile schedule can whiten the residual and improve static long-range tracking. Schedule
> optimization is treated as an ablation/future-work item.

## What not to write

- “30–34 kHz is the optimal frequency schedule.”
- “The schedule is universally best.”
- “Moving-target schedule optimization is solved.”
- “Costas-like inter-ping hopping is our final method” without independent validation.

## Relation to current paper claim

The paper’s scientific contribution does not require proving that 30–34 kHz linear sweep is optimal.
It only needs to show that a frozen carrier-agile schedule can change the residual statistics and
produce reproducible static 600 m improvement. The ablation plan is a reviewer-safety and future-work
upgrade, not a prerequisite for the current manuscript.
