# Table source-data manifest

범위: 현재 원고의 `table` 환경과 table-like comparison blocks.

## Table mapping

| Manuscript table | Label | 내용 | Primary source folder | Evidence / notes | Status |
|---|---|---|---|---|---|
| Related-work positioning table | `tab:priorart` | frequency-diverse/radar/USBL prior art와 본 논문 차별점 | `117. Related work table finalization` | `final_related_work_table.md`, `reviewer_response_templates.md`, `citation_priority.md` | traced |
| Estimator comparison table | `tab:estimators` | NLS/EKF/UKF RMSE, divergence, NEES/NIS | `43. 추정기 비교 골격 EKF UKF NLS` | README table: 100/200/400/600/overall; EKF 31%/25% divergence; UKF backbone decision | traced |
| Adaptive-R routing table | `tab:routing` | plain UKF vs conditional adaptive-R routing, single-batch and large-scale | `44. 조건부 adaptive-R 라우팅 ablation`, `46. 대규모 몬테카를로 라우팅 이득 확정`, `93. Method 세부 코드 대조` | 44 README: NEES 341→27, NIS 30→16, 600 m 13.16→12.29; 46 README: divergence 3%→0%, NEES 164→22 | traced |
| CRLB/floor table | `tab:crlb` | empirical CRLB, NLS, routed UKF, efficiency, bias floor | `45. CRLB 이론하한 대비 효율` | README/result JSON: 600 m CRLB 11.80, NLS 13.38, routed 12.29, floor 3.45 | traced |
| Compact validation result summary table | `tab:results` | positive/negative validation summary | `61`, `63`, `82`, `45`, `134` | Static positive from 61; moving whitening/non-RMSE from 63; quasi-static boundary from 82; long-range floor from 45; wording safety from 134 | traced |
| Quasi-static speed sweep table | `tab:quasi` | 132 paired trial speed sweep | `82. 준정지 속도 경계 검증 실행` | README/result_summary: 0.005 validated, 0.010/0.050 not validated, 0.030/0.100 non-monotonic recoveries | traced |
| Limitations and follow-up table | `tab:limitations` | simulation/field/geometry/schedule limitations | `116. Manuscript claim boundary audit`, `118. Real-water validation plan`, `119. Carrier schedule ablation plan`, `134` | claim boundary and future-work docs | traced |

## Tables that are mostly narrative

`tab:priorart` and `tab:limitations` are not generated from numeric JSON. They are still traceable because they depend on literature/claim-boundary review folders rather than simulation output.

For reviewer response, treat them as argumentation tables:

- prior-art table → novelty defense and citation coverage
- limitations table → scope honesty and future work

## Tables that must stay numerically locked

The following tables must not be edited by hand without checking the source folders:

- `tab:estimators`
- `tab:routing`
- `tab:crlb`
- `tab:results`
- `tab:quasi`

If any number changes in the manuscript, rerun a traceability check against 43/44/45/46/61/63/82/93/145.
