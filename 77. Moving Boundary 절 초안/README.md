# 77. Moving Boundary 절 초안

## 목적

63~67번 이동표적 결과를 논문 한계/적용경계 절로 정리한다.

## 핵심 메시지

- 이동 표적에서도 frequency agility는 DOA residual lag-1 자기상관을 크게 낮춘다.
- 하지만 pooled RMSE 이득은 재현되지 않았다.
- 이유는 target motion 자체가 `δ(t)`를 바꾸면서 fixed carrier에서도 일부 self-whitening을 만들기 때문이다.
- 64~67번의 adaptive-R, gating, sparse/condition-aware schedule도 general-purpose moving improvement로는 미재현됐다.
- 따라서 moving target schedule은 future work이고, 본 논문 핵심 주장은 static/quasi-static long-range validation이다.

## 다음 단계

78번은 `Discussion 절 초안`이 자연스럽다. Fig.7 CRLB floor, sub-meter 기대 정리, 실해역 검증 계획, 레이더 glint와의 차이를 묶으면 된다.
