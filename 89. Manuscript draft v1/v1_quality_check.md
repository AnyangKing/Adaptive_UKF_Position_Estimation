# v1 quality check

## Improvements over v0

- Observation vector equations inserted.
- UKF state and constant-velocity model inserted.
- adaptive-R routing equation inserted.
- carrier phase mechanism inserted.
- static/moving/quasi-static metric equations inserted.
- Fig.1~6 and Table 1~2 callouts inserted.
- claim boundary preserved.

## Claim boundary check

| Claim | Status |
|---|---|
| static long-range is main application | kept |
| quasi-static limited to 0.005 m/s | kept |
| moving RMSE improvement not claimed | kept |
| frequency hopping first-use not claimed | kept |
| sub-meter long-range not claimed | kept |
| carrier phase not presented as full multipath estimator | kept |

## Known limitations

1. Citation placeholders remain.
2. Figures are referenced but actual figure files are not embedded.
3. Equation numbering is not journal-formatted.
4. Section 2 may need more exact implementation detail from code before submission.
5. Table 1 and Table 2 are callouts only; actual table bodies should be assembled next.

## Recommended next folder

90번 후보:

- `90. Tables draft` — Table 1 prior-art differentiation and Table 2 numerical summary 작성.

Alternative:

- `90. Exact citation audit 1차` — DB 접근이 가능하면 citation placeholder를 실제 reference로 일부 치환.
