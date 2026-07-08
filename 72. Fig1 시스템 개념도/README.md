# 72. Fig1 시스템 개념도

## 목적

논문 Fig. 1 후보를 만든다. 70번의 정량그림과 달리, 이 그림은 독자가 연구 메커니즘을 처음 이해하도록 돕는 개념도다.

## 그림이 설명하는 것

- 얕은바다 USBL에서 직접파와 표면반사가 동시에 들어온다.
- 5 ms gated SRP/DOA 처리를 해도 장거리에서는 표면반사 누설이 gate 안에 남을 수 있다.
- 고정 반송파에서는 직접파-반사파 상대위상 `phi = 2π f δ`가 ping마다 거의 고정되어 coherent DOA bias가 생긴다.
- 반송파를 ping마다 바꾸면 같은 배열/같은 필터에서도 위상이 회전해 잔차 편향이 백색화된다.
- 최종 위치추정 중심축은 그대로 `TOA/TDOA/DOA → UKF position`이다.

## 생성 파일

- `figures/fig1_system_concept.png`
- `figures/fig1_system_concept.svg`

## 재현 방법

```powershell
python "72. Fig1 시스템 개념도/generate_fig1_concept.py"
```

## 다음 단계

이 그림은 1차 도식이다. 최종 논문용으로는 지도교수 피드백 후 다음을 조정할 수 있다.

- 수심/배열/표적 아이콘을 더 논문스럽게 단순화
- `5 ms gate`를 실제 신호 시간축 inset으로 바꾸기
- Fig. 2와 색상 체계를 맞추기
- 최종 캡션을 71번 문서와 연결하기
