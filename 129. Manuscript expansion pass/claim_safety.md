# Claim safety check

## 바꾸지 않은 핵심 claim

129번 확장은 원고를 길게 만들었지만, 헤드라인 claim은 바꾸지 않았다.

유지한 claim:

- Main method: TOA/TDOA/DOA observation vector + adaptive-R UKF backbone + transmit-side carrier
  agility.
- Main positive result: static 600 m settled RMSE 13.01 m to 8.87 m, 32% improvement,
  $p=0.0008$.
- Moving target caution: residual whitening은 강하지만 pooled moving RMSE gain은 신뢰할 수 없음.
- Quasi-static boundary: continuous conservative support는 0.005 m/s.
- Novelty framing: first frequency hopping claim이 아니라 post-gating coherent DOA-bias whitening
  mechanism, USBL transfer, validation, and boundary.
- No sub-meter 600 m claim.

## 새로 강해진 부분

추가된 문단들은 claim을 키우기보다 방어력을 키운다.

- 왜 단순 UKF tuning 논문이 아닌지.
- 왜 channel model이 이 연구에 충분한지.
- 왜 moving target 결과를 positive claim으로 쓰지 않는지.
- 왜 frozen schedule이 더 정직한 검증인지.
- 왜 real-water validation은 static/very-slow-drift부터 가야 하는지.

## 주의

129번 이후 원고는 9쪽이 되었지만, 아직 최종 투고본은 아니다.

남은 placeholder:

- author names and affiliations
- funding
- author contributions
- data availability
- conflicts of interest

