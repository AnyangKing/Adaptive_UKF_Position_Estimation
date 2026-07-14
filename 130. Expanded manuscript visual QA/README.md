# 130. Expanded manuscript visual QA

## 목적

129번에서 원고를 7→9쪽으로 확장했으므로, 페이지별 그림/표 배치와 조판이 다시 자연스러운지
`paper/manuscript.tex`를 빌드해 전 9쪽을 렌더·육안 점검했다. 원고는 로컬 `paper/` 전용, 이 폴더는
QA 기록만.

## 방법

`cd paper && latexmk manuscript.tex` → `pdftoppm -png -r 70` 전 9쪽 렌더 → 페이지별 육안 점검.

## 빌드/품질 (2026-07-13)

- 9쪽, PDF 1.73 MB. **미해결 인용/참조 0, active overfull 0, active underfull 0**(underfull vbox 1건, 무해).

## 페이지별 판정

| 쪽 | 내용 | 판정 |
|---:|---|---|
| 1 | 제목·초록·Index Terms·서론(드롭캡)·Related Work & Problem Statement | 정상(저자 placeholder는 예정대로) |
| 2 | System Model & UKF Fusion, 수식 (1)~(12) | 정상 |
| 3 | **Table I**(선행연구 차별, 전폭) + implementation parameters | 정상·가독(무겁지만 novelty 방어용이라 유지) |
| 4 | **Fig.1**(기전 개념도) + Post-Gating Bias Floor + Proposed Method | 그림이 System/Method 근처 — 자연스러움 |
| 5 | **Fig.2·3**(CRLB floor·반송파 감도) + Mechanism 수식 (13)~(17) + Schedule | 그림-설명 근접, 자연스러움 |
| 6 | **Fig.4**(정지 600m 검증) + Experimental Validation + 수식 (18)(19) | 정상 |
| 7 | **Fig.5·6**(이동 백색화·준정지 경계) + quasi-static + Discussion 진입 | 정상 |
| 8 | **Table II**(검증 요약, 전폭) + Discussion + Conclusion + back matter 시작 | 정상 |
| 9 | **Table III**(한계, 전폭) + Data Availability·Ack·Conflicts + References [1]~[4] | 정상 — 7쪽 시절 "마지막 페이지 비어보임" 문제 해소됨 |

## 판정

**시각 QA 통과. 129 확장이 레이아웃을 깨지 않았고, 오히려 마지막 페이지 공백 문제가 해소됨.**
그림 6종은 전부 첫 언급 근처, 표 3종은 전폭 배치로 가독. 조판 수정 필요 없음. 저자·back-matter
placeholder만 남음(사람 결정).

## 다음 (판단)

조판은 깨끗하나 **참고문헌이 [1]~[4] 4편뿐이라 SCI 기준 얇다.** 앞선 선행연구 대조(논문_초고_구조.md
노벨티 섹션)에서 확보한 인용 후보를 refs.bib에 추가하고 Related Work에서 인용하면 참고문헌 보강 +
차별화 서술 강화가 동시에 된다. 후보(브라우저로 실재 확인함): Blunt & Mokole 2016(radar waveform
diversity 리뷰), Henderson 1985(JASA broadband DF), Zhang et al. 2024(Ocean Eng, differential USBL
보정). → 131번 후보 = "참고문헌·Related Work 보강"(정확 서지 검증 후 추가). 그 외 남은 것은 사람 결정
(저자·Funding·저널).
