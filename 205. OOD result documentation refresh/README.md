# 205. OOD result documentation refresh

## 목적

204번 OOD moving full validation 결과를 프로젝트 운영 문서와 보고 문서에 반영했다.

## 반영한 핵심 결과

- 조건: accelerating radial, curved arc, mixed radial+tangential, vertical sine maneuver.
- 거리: 0--1000 m, 100 m 간격.
- 규모: 총 528 paired OOD cases.
- fixed mean RMSE: 10.832 m, P90: 22.339 m, divergence: 0.049.
- plain hop mean RMSE: 10.691 m, P90: 21.611 m, divergence: 0.057.
- transition-aware soft-R mean RMSE: 7.809 m, P90: 15.936 m, divergence: 0.006.
- soft-R vs hop: +2.881 m, p=9.076e-22.
- soft-R vs fixed: +3.023 m, p=1.015e-18.

## 해석 경계

- 204번은 transition-aware soft-R의 OOD motion simulation robustness를 지지한다.
- plain carrier hopping 단독은 여전히 moving target solution이 아니다.
- 실해역, rough/random surface, hardware frequency response, high-fidelity ray model, arbitrary motion 일반화는 아직 검증하지 않았다.

## GitHub 규약

이 폴더만 커밋한다. 실제 root MD와 `paper/` 원고 변경은 로컬 전용이며 사용자 지시 없이 stage하지 않는다.
