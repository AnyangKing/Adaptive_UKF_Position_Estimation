# 129. Manuscript expansion pass

## 목적

사용자가 지적한 “우리가 연구한 양에 비해 6--7쪽은 너무 적어 보인다”는 문제를 반영하여,
로컬 `paper/manuscript.tex`를 SCI 저널용 full manuscript에 가깝게 1차 확장했다.

논문 파일 자체와 PDF는 `paper/` 아래 로컬 전용이며 GitHub에는 올리지 않는다. 이 폴더는 변경 근거와
검증 기록만 보존한다.

## 핵심 결과

| 항목 | 변경 전 | 변경 후 |
|---|---:|---:|
| LaTeX source size | 33,039 bytes | 47,859 bytes |
| PDF length | 7 pages | 9 pages |
| active overfull hbox | 0 | 0 |
| active underfull hbox | 0 | 0 |
| underfull vbox | 0 | 1 |
| unresolved references/citations | 0 | 0 |

## 적용한 확장

원고에 다음 내용을 실제로 추가했다.

1. Related Work/Problem Statement에 연구 질문 3개와 negative experiment의 역할 추가.
2. System Model에 compact aperture 한계와 shallow-water image-source channel 수식 추가.
3. TOA/TDOA/DOA 관측 생성 설명 추가.
4. adaptive-R UKF가 해결하는 것과 해결하지 못하는 것의 경계 추가.
5. 5 ms DOA gate가 pure direct path 보장이 아니라는 설명 추가.
6. Proposed Method에 “filter tuning study에서 observation-design study로 전환된 이유” 추가.
7. carrier phase rotation 식 $\Delta\phi=2\pi(f_b-f_a)\delta_k$ 추가.
8. frozen schedule이 post-hoc optimized schedule이 아니라는 점 추가.
9. Evaluation Protocol and Statistical Testing subsection 신설.
10. mechanism evidence와 localization evidence를 분리하는 해석 추가.
11. moving/quasi-static negative result를 boundary로 해석하는 문단 추가.
12. Discussion에 novelty claim을 좁게 읽어야 하는 이유와 실험 계획상 의미 추가.
13. carrier agility의 practical cost, frequency-dependent calibration 필요성 추가.

## 판단

현재 9쪽 원고는 7쪽 skeleton보다 SCI 저널 논문 초안에 더 가깝다.

아직 최종 full manuscript로는 더 확장 가능하다. 특히 실제 투고 전에는 다음 영역을 더 보강할 수 있다.

- 수조/호수 실험 계획 또는 예비 실험이 생기면 별도 validation section 추가.
- schedule ablation 결과가 추가되면 method/results 확장.
- 선행연구 원문 대조가 더 늘어나면 Related Work 확장.
- 실제 저널 template이 정해지면 back matter와 reference style 정리.

## 다음 후보

다음 자동 목표를 잡는다면 `130. Expanded manuscript visual QA`가 좋다.

129번 확장으로 9쪽이 되었으므로, 페이지별 그림/표 배치가 다시 자연스러운지 확인해야 한다.

