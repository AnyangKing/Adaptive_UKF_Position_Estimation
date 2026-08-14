# Claim boundary check

## 이번 원고 문장이 지지하는 주장

1. 이동 표적 0--1000 m sweep에서 transition-aware soft-R가 fixed 및 plain hopping보다 평균적으로 낮은 RMSE를 보였다.
2. plain hopping은 일부 거리/기하에서 tail 악화를 만들 수 있다.
3. carrier transition을 관측 신뢰도 변화로 해석하고 UKF의 측정 공분산에 반영하면, plain hopping의 failure mode 일부를 줄일 수 있다.
4. 800 m 조건은 성공만 보여주는 사례가 아니라 `fixed -> hop 악화 -> soft-R 회복`이라는 실패-회복 구조를 보여주는 대표 사례다.

## 이번 원고 문장이 주장하지 않는 것

1. frequency agility 자체의 최초 발명.
2. 실제 해상/호수 실험에서 동일한 수치가 나온다는 주장.
3. 모든 이동 궤적, 모든 수심/해저/해면 조건, 모든 SNR에서 성능이 개선된다는 주장.
4. 0 m near-vertical case를 장거리 성능 근거로 사용하는 주장.
5. plain hopping 단독으로 이동 표적 문제가 해결된다는 주장.

## 왜 중요한가

이 논문의 강점은 “TOA/TDOA/DOA + UKF” 자체가 아니라, 얕은 수중 다중경로가 만드는 coherent DOA bias를 송신 설계와 필터 신뢰도 조절로 다루는 것이다. 따라서 원고 문장은 항상 다음 경계를 지켜야 한다.

$$
\text{frequency agility alone} \neq \text{proposed moving-target solution}
$$

제안법의 이동 표적 기여는 다음처럼 써야 안전하다.

$$
\text{frequency agility} + \text{transition-aware measurement covariance routing}
\rightarrow \text{tail-risk reduction in the tested signal-level simulator}
$$
