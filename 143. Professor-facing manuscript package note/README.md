# 143. Professor-facing manuscript package note

## 목적

현재 12쪽 IEEE-neutral 원고를 교수님께 보여줄 때 사용할 설명 메모를 작성했다.

이 폴더는 보고용 초안/상태 설명을 담는 numbered process artifact다. 실제 `paper/` 원고와 PDF는 Git에
올리지 않는다.

## 현재 원고 상태

- 형식: IEEEtran journal-format neutral draft.
- 분량: 12 pages.
- 빌드: 성공.
- active warning: underfull vbox 1개만 남음.
- overfull/underfull hbox: 0.
- unresolved citation/reference: 0.
- 저자/소속/Funding/Data Availability/Acknowledgment: 아직 placeholder.

## 교수님께 말할 한 줄

> 기존 TOA/TDOA/DOA-UKF 위치추정 아이디어에서 출발해, 장거리 compact USBL의 핵심 한계가 단순 필터 문제가 아니라 post-gating coherent multipath DOA bias라는 것을 확인했고, 이를 ping-to-ping carrier agility로 whitening하는 bounded observation-design 방법으로 정리했습니다.

## 핵심 수치

| 항목 | 결과 |
|---|---|
| Static 600 m fixed carrier | 13.01 m settled RMSE |
| Static 600 m carrier-agile | 8.87 m settled RMSE |
| Static improvement | 32%, paired gain +4.14 m, p = 0.0008 |
| Moving residual whitening | lag-1 +0.470 to -0.208, p = 5.56e-10 |
| Moving pooled RMSE | gain -0.10 m, p = 0.301; improvement not claimed |
| Quasi-static boundary | conservative continuous support through 0.005 m/s |
| Two-ray mechanism fit | R² up to 0.99 |

## 보고 시 강조할 점

1. “주파수 도약 자체가 novelty”라고 주장하지 않는다.
2. novelty는 shallow-water compact USBL에서 post-gating coherent DOA bias를 carrier-agile whitening으로 줄인 기전, 검증, 한계 규명이다.
3. moving target에서는 residual whitening은 확인했지만 RMSE improvement는 주장하지 않는다.
4. static/very-slow-drift regime부터 실제 수조/호수 실험으로 가는 것이 안전하다.
5. 현재 논문은 12쪽 full manuscript draft 수준이며, 제출 전에는 저자정보/백매터/저널 선택/실험 여부를 확정해야 한다.

## 다음 결정 필요

교수님 또는 사용자가 결정해야 하는 항목:

- 저자명/저자 순서.
- 소속과 교신저자.
- Funding statement.
- Data availability/repository 공개 방식.
- Acknowledgment 여부.
- 실제 목표 저널.
- 수조/호수/해상 실험을 추가할지 여부.
