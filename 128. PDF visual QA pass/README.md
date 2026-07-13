# 128. PDF visual QA pass

## 목적

127번까지의 LaTeX 조판 패치가 실제 PDF 화면에서 교수님께 보여줄 만한 수준인지 확인했다.

확인 대상:

- IEEE 장 번호 생성 상태
- figure/table 배치
- 마지막 페이지 상태
- draft/placeholder 잔여 요소
- 교수님 보고 가능 여부

## 결론

현재 PDF는 **교수님께 “현재 논문 초안/진행본”으로 보여줄 만한 상태**다.

다만 투고 직전 완성본은 아니다. 남은 주요 보완점은 다음과 같다.

1. 저자명/소속 placeholder.
2. Funding, Author Contributions, Data Availability 등 back-matter placeholder.
3. 7쪽 마지막 페이지가 Table III와 참고문헌 1개만 남아 비어 보이는 문제.
4. Table I이 novelty 방어에는 유용하지만 시각적으로 무거운 문제.

## 페이지별 판단

| Page | 판단 |
|---:|---|
| 1 | 제목, 초록, Index Terms, I--III 장 번호 정상. 저자 placeholder와 draft footer는 남아 있음. |
| 2 | Table I이 상단 대부분을 차지해 무겁지만 깨지지는 않음. novelty 방어용이라 현재는 유지 가능. |
| 3 | Fig.1/Fig.2가 System/Method 설명 근처에 배치되어 자연스러움. IV장 진입도 좋음. |
| 4 | Fig.3가 mechanism 설명 근처에 배치됨. V장 Results로 넘어가는 흐름 자연스러움. |
| 5 | Fig.4--Fig.6가 결과/경계 설명 근처에 배치되어 가장 개선 효과가 큼. Discussion 진입 자연스러움. |
| 6 | Table II, Conclusion, back matter, References가 깨지지 않음. Placeholder는 투고 전 정리 필요. |
| 7 | Table III와 마지막 참고문헌만 남아 페이지가 많이 비어 보임. 보여줄 수는 있지만 투고 전 압축 후보. |

## 보여줄 만한가?

Yes.

이유:

- PDF는 7쪽으로 정상 빌드됨.
- LaTeX active warning은 0개 상태다.
- IEEE 장 번호 `I`--`VII`가 정상 표시된다.
- 그림들이 첫 언급 또는 해당 결과 근처로 이동해 논문 흐름이 크게 좋아졌다.
- 교수님께 “현재 논문 구조와 claim이 이렇게 잡혔다”라고 보여주기에는 충분하다.

## 여기서 목표를 멈추는 이유

사용자 요청에 따라 “보여줄 만하다고 생각되면 목표 멈춤”으로 판단한다.

다음 단계 후보는 있지만, 이것은 별도 지시 후 진행하는 것이 맞다.

- Table III를 Discussion 문단으로 흡수하거나 supplement로 이동해 6쪽화.
- Table I caption/column을 더 줄여 페이지 2의 시각 밀도 완화.
- back matter placeholder 정리.
- 저자/소속 확정 후 title page 정리.

