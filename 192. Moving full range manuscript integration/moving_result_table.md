# 191 moving full-range result table for manuscript

Source: `191. Moving full range transition aware independent validation/result_summary.md`

## Overall paired comparisons

| comparison | mean gain (m) | p | improved fraction | tail worsened | n |
|---|---:|---:|---:|---:|---:|
| softR vs hop | 3.948 | 1.585e-22 | 0.409 | 0.028 | 528 |
| softR vs fixed | 4.797 | 1.671e-30 | 0.693 | 0.131 | 528 |
| hop vs fixed | 0.849 | 1.336e-07 | 0.593 | 0.214 | 528 |

## Distance breakdown

| distance (m) | fixed | hop | softR | softR gain vs fixed |
|---:|---:|---:|---:|---:|
| 0 | 4.445 | 4.700 | 4.700 | -0.255 |
| 100 | 1.733 | 1.656 | 1.581 | 0.152 |
| 200 | 8.935 | 8.792 | 3.959 | 4.976 |
| 300 | 10.086 | 8.758 | 4.513 | 5.573 |
| 400 | 11.840 | 9.802 | 5.511 | 6.329 |
| 500 | 14.140 | 11.302 | 6.342 | 7.798 |
| 600 | 14.738 | 13.252 | 8.381 | 6.358 |
| 700 | 14.821 | 12.594 | 9.110 | 5.711 |
| 800 | 17.696 | 22.386 | 10.828 | 6.867 |
| 900 | 17.420 | 16.671 | 12.292 | 5.128 |
| 1000 | 18.189 | 14.792 | 14.062 | 4.127 |

## Manuscript placement

- 한글 원고에는 새 표 `tab:movingfull`로 삽입했다.
- 영어 원고는 한글 기준 원고 확정 후 별도 패스에서 같은 claim boundary로 반영한다.
- 0 m는 near-vertical degenerate condition이므로 긍정 근거로 강조하지 않는다.
- 800 m는 plain hopping failure-and-recovery example로 적합하다.

