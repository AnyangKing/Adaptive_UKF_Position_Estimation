# 200. Professor report refresh after moving manuscript update

## 목적

교수님 보고용 로컬 문서 `지도교수_보고_요약.md`의 최상단 현재 상태 스냅샷을 191번 이동 표적 full-range 검증과 198--199번 원고 안정화 작업 기준으로 갱신했다.

보고문서 자체는 root MD이며 로컬 전용이다. GitHub에는 이 200번 폴더만 커밋한다.

## 반영한 최신 내용

- 연구 축이 정지/준정지 중심에서 이동 표적 0--1000 m 검증까지 확장되었음을 명시.
- 191번 독립검증의 핵심 수치 반영:
  - 총 528 paired moving cases
  - transition-aware Adaptive-R vs plain hopping: 평균 RMSE 3.948 m 개선, p=1.585e-22, tail worsened 2.8%
  - transition-aware Adaptive-R vs fixed carrier: 평균 RMSE 4.797 m 개선, p=1.671e-30, improved fraction 69.3%
- 800 m failure-and-recovery 사례 반영:
  - fixed 17.696 m
  - plain hop 22.386 m
  - transition-aware soft-R 10.828 m
- “단순 frequency hopping 단독 성공”이 아니라 “carrier transition-aware Adaptive-R와 결합했을 때 이동 표적 tail-risk를 줄임”이라는 claim boundary 반영.
- 실제 수조/호수/해상 검증 결과, 최종 저널·저자정보 등 아직 지어내면 안 되는 항목을 유지.

## 판단

교수님 보고 시에는 “기존 정지 표적 논문에서 이동 표적 논문으로 방향이 바뀐 것인가?”라는 질문이 나올 수 있다. 답은 다음처럼 정리하는 것이 가장 안전하다.

> 처음 아이디어는 TOA/TDOA/DOA를 UKF로 융합하는 위치추정이었다. 연구 과정에서 병목이 필터보다 얕은 수중 coherent multipath DOA bias임을 확인했고, frequency-agile observation design으로 이를 줄이는 축을 세웠다. 최근에는 이동 표적에서 단순 hopping의 tail 악화를 확인한 뒤, transition-aware Adaptive-R를 결합해 0--1000 m 이동 검증에서 회복 가능성을 보였다.

즉 논문은 “알려진 필터 조합”이 아니라 “수중 다중경로가 관측에 주는 구조적 실패를 어떻게 관측 설계와 UKF 신뢰도 조절로 다루는가”로 가는 것이 맞다.
