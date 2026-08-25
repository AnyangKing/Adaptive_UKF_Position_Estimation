# 축별 지표 finite-n 설명 반영 보고

## 문제

239번 result summary에서 3D RMSE 비교는 528 cases를 사용하지만, horizontal/vertical/radial/cross-range paired-gain 비교는 511 cases로 표시된다.

## 원인

빠진 17개는 모두 `distance=0 m`의 near-vertical degenerate 조건이다. 발산 trial 제외가 아니라, 축별 settled metric이 유한하게 계산되지 않은 케이스가 paired-gain 검정에서 제외된 것이다.

## 조치

영문/한글 원고의 `tab:consistencyaxis` caption에 다음 경계를 추가했다.

- 축별 paired-gain 통계: 511 finite cases
- 전체 3D RMSE/divergence validation: 528 cases

## 검증

`audit_finite_n_clarification.py`로 영어/한글 원고 marker와 한글 caption 중복 여부를 확인한다.

