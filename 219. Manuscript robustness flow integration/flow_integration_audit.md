# Flow integration audit

## Main storyline retained

The primary paper story remains:

1. compact USBL has a post-gating coherent DOA residual problem;
2. carrier agility decorrelates the carrier-locked component;
3. static 600 m validation proves a bounded positive case;
4. plain hopping fails as a general moving-target estimator;
5. transition-aware soft-R is the validated moving-target estimator;
6. OOD results support simulation-level robustness while preserving boundaries.

## Placement decision for 215/216

| Folder | Manuscript placement | Reason |
|---|---|---|
| 215 | Results discussion, limitations, compact results table, supplement statement | Directly answers hardware-response sensitivity but is not measured hardware validation. |
| 216 | Results discussion, compact results table, conclusion, supplement statement | Expands tested OOD family coverage but is not arbitrary-motion proof. |

## Abstract decision

Do not add 215/216 to the abstract at this stage.

Reason: the abstract should not make supplementary robustness checks look like primary claims. The abstract already states the strongest validated main results: 191 structured moving validation and 204 OOD validation.

## Table decision

Add compact table rows because readers and reviewers often use the results table as a claim map. The rows explicitly state the evidence boundary.
