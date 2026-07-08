# 75. Mechanism 절 초안

## 목적

Fig.1, Fig.2, 58번 결과를 연결해 논문의 Mechanism 절 1차 초안을 작성한다.

## 핵심 내용

- 직접파 gate를 적용해도 장거리에서는 표면반사 누설이 DOA gate 안에 남을 수 있다.
- 직접파와 반사파의 상대 위상은 `phi = 2πfδ + theta_r`로 표현할 수 있다.
- 정지 표적 + 고정 반송파에서는 `δ`와 `f`가 모두 고정되어 편향이 phase-locked coherent bias가 된다.
- 반송파 도약은 `f`를 바꿔 `phi`를 ping마다 회전시키고, 이로 인해 DOA bias가 백색화된다.
- 이동 표적은 `δ(t)` 자체가 바뀌므로 fixed carrier에서도 일부 자기백색화가 발생한다. 이 때문에 moving RMSE 이득은 재현되지 않았다.

## 연결 폴더

- 58번: carrier-sensitive bias 진단
- 70번: Fig.2 정량그림
- 72번: Fig.1 개념도
- 74번: Introduction 초안

## 다음 단계

76번은 `Static Validation` 절 초안을 작성하는 것이 자연스럽다. 61번 수치와 Fig.3을 중심으로 쓰면 된다.
