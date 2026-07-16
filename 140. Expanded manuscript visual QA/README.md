# 140. Expanded manuscript visual QA

## 목적

129번 이후 확장된 로컬 `paper/manuscript.pdf`를 페이지 이미지로 확인하여, 원고가 더 이상 “연구량에 비해
너무 짧아 보이는 상태”인지 평가했다.

중요: 현재 로컬 PDF는 129번 기록 당시의 9쪽보다 더 확장되어 **12쪽** 상태다. 이 QA는 현재 로컬
`paper/`의 최신 PDF를 기준으로 수행했다.

## 결론

현재 12쪽 원고는 SCI 저널용 full manuscript 초안으로 보기에 분량감이 충분하다.

7쪽 skeleton에서 느껴졌던 “우리가 연구한 양이 너무 적어 보인다”는 문제는 해소되었다. 오히려 이제는
다음 단계가 분량 확장이 아니라 **표/float 밀도와 LaTeX warning 정리**다.

## 빌드 상태

최신 로그 기준:

```text
Output written on manuscript.pdf (12 pages, 1929643 bytes).
```

남은 warning:

```text
Underfull \hbox (badness 4316) in paragraph at lines 100--110
Underfull \vbox (badness 10000) has occurred while \output is active []
Underfull \hbox (badness 10000) in paragraph at lines 371--383
Underfull \hbox (badness 10000) in paragraph at lines 371--383
Underfull \hbox (badness 1931) in paragraph at lines 371--383
Overfull \hbox (6.36058pt too wide) detected at line 604
```

## 시각 QA 요약

| Page range | 판단 |
|---|---|
| 1--2 | 제목, 초록, Introduction/Related Work/System Model 진입이 자연스러움. Ocean Engineering draft 문구는 저널 확정 전 정리 후보. |
| 3--4 | Table I와 Fig.1 배치가 자연스러움. Table I은 여전히 무겁지만 novelty 방어용으로 유지 가능. |
| 5--8 | 연구량이 가장 잘 살아나는 구간. estimator comparison, floor analysis, mechanism 수식, protocol이 들어가 SCI 원고 느낌이 강해짐. |
| 9--10 | Static/moving/quasi-static 결과와 Discussion 흐름이 자연스러움. Fig.5--7 위치도 대체로 좋음. |
| 11--12 | 결과 표, limitations, conclusion, references가 들어가며 마지막 페이지가 예전처럼 비어 보이지 않음. |

## 판단

현재 원고는 교수님께 보여줄 때 다음처럼 말할 수 있다.

> 7쪽 skeleton에서 빠져 있던 채널 모델, 관측 생성, UKF 한계, 실험 프로토콜, negative-result 해석을
> 본문에 복원해 12쪽 full manuscript 초안으로 확장했습니다. 이제 분량은 부족하지 않고, 다음은 표와
> LaTeX 경고 정리 단계입니다.

## 다음 목표

다음 목표는 `141. Expanded manuscript warning cleanup`이 적절하다.

우선순위:

1. Overfull hbox line 604 제거.
2. Underfull hbox lines 100--110, 371--383 완화.
3. Underfull vbox가 실제 빈 공간을 만드는지 확인 후 float 위치 조정.
4. 12쪽은 유지하되, 표가 과도하게 몰린 page 5와 page 11의 밀도만 조정.
