# Table 3 draft: Limitations and future-work map

## Manuscript caption draft

Table 3. Limitations and corresponding follow-up work. The items are separated into submission-critical fixes, experimental validation, and future algorithmic extensions.

## Table body draft

| Limitation / open item | Current evidence | Risk if unresolved | Follow-up action | Paper placement |
|---|---|---|---|---|
| Exact citation metadata still pending for several placeholders | Folder 86 defines the audit protocol but does not close all references | Reviewer may challenge novelty framing | Verify publisher metadata for radar glint/frequency agility, JASA FH USBL, IEEE Costas USBL, frequency-comb/iUSBL | Before submission; Related Work |
| No real-water lake/sea experiment yet | Simulation and signal-level validation only | External validity remains limited | Run static 600 m and slow-drift trials in controlled water before strong applied claims | Discussion / Future Work |
| Moving-target RMSE gain not established | Whitening is strong, but pooled RMSE gain is not reproducible | Overclaiming would weaken the paper | Keep moving result as mechanism/boundary; develop risk-aware schedule only after tail predictors pass a diagnostic test | Results + Future Work |
| Frequency schedule ablation incomplete | 30--34 kHz schedule is frozen and validated, but alternatives remain underexplored | Reviewer may ask if schedule is arbitrary | Add or propose ablation over hop span, hop period, pseudo-random vs deterministic schedules | Future Work or supplemental |
| Compact aperture imposes meter-scale floor | CRLB-scale and empirical errors remain around meter-to-10 m scale at 600 m | Sub-meter expectation is unrealistic under current geometry | Present aperture/floor analysis clearly; avoid sub-meter claims | Discussion |
| Environmental model still simplified | Surface reflection and coherent multipath are modeled, but real underwater variability is broader | Field deployment may show additional noise modes | Extend to bathymetry, sound-speed gradients, platform motion, and hardware timing uncertainty | Future Work |
| Citation/claim language must remain conservative | Frequency hopping and radar frequency agility are not new | "Novelty" may be rejected if framed too broadly | Claim mechanism, underwater USBL transplantation, validation, and boundary; not first frequency hopping | Introduction + Related Work |

## Short future-work paragraph draft

Future work should move in three directions. First, the citation audit should be closed with exact publisher metadata so that the novelty claim remains precise rather than overstated. Second, the validated static and very-slow-drift regimes should be tested in lake or sea trials with the same compact eight-sensor geometry. Third, moving-target use should not be extended by intuition alone; any risk-aware adaptive hopping schedule should first prove that its runtime indicators predict tail degradation before being evaluated for RMSE improvement.

