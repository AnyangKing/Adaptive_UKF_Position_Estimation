# Cut strategy

## 현재 상태

- 영문 원고: 13쪽 PDF
- 한글 원고: 13쪽 PDF
- 지금은 IEEE 공용 양식이며, 최종 저널/쪽수 제한은 아직 확정되지 않았다.

## 원칙

분량을 줄일 때 결과를 약하게 만드는 방향으로 자르지 않는다. 대신 다음 순서로 자른다.

1. 중복 요약표
2. 상세 ablation 표
3. 상세 프로토콜 반복 문장
4. 부가 진단 그림
5. 마지막에만 문헌리뷰 세부 문장

## 12쪽 이하 목표일 때

권장:

- compact summary table을 supplement 후보로 이동
- quasi-static 상세표를 supplement 후보로 이동
- 본문에는 핵심 평균, p-value, boundary 문장만 유지

효과:

- 본문 논리 손실이 작다.
- moving full-range 핵심 그림은 보존 가능하다.

## 10쪽 이하 목표일 때

권장:

- empirical-CRLB 상세표를 supplement로 이동
- baseline 상세표를 축약
- Method의 구현 파라미터 일부를 supplement protocol table로 이동

주의:

- related-work positioning과 mechanism figure는 유지하는 편이 낫다.
- 이 둘을 빼면 novelty 방어력이 빠르게 약해진다.

## 8쪽 이하 목표일 때

권장하지 않는다.

이 연구는 실패/한계/경계까지 같이 보여줘야 설득력이 생기는 구조다. 8쪽 이하로 줄이면 “알려진 기법 조합 + 시뮬레이션 성능표”처럼 보일 위험이 커진다.

만약 반드시 8쪽 이하가 필요하면, 짧은 conference paper가 아니라 journal full paper의 preliminary version으로 포지셔닝해야 한다.
