# IEEE structure audit

## 원고 구조

대상: `paper/manuscript.tex`

정적 스캔 결과:

| 항목 | 수 |
|---|---:|
| 본문 numbered section | 9 |
| subsection | 1 |
| full-width table/table* | 3 |
| figure | 6 |
| unnumbered back-matter section* | 6 |

## Numbered sections

현재 본문 numbered section은 다음 9개다.

1. Introduction
2. System and Signal Model
3. Post-Gating DOA Bias Floor
4. Carrier-Sensitive Coherent Interference Mechanism
5. Frequency-Agile Whitening Method
6. Static Validation
7. Whitening Evidence and Applicability Boundary
8. Discussion
9. Conclusion

주의: 위 목록은 논리상 9개 section이다. IEEEtran에서는 자동으로 Roman numeral 번호가 붙는다. 사용자가
말한 “장마다 번호”는 수동으로 `1.`을 쓰는 방식이 아니라 `\section{}`를 올바르게 쓰면 해결된다.

## Back matter

현재 다음 `\section*{}`가 있다.

- Supplementary Materials
- Author Contributions
- Funding
- Data Availability Statement
- Acknowledgments
- Conflicts of Interest

이들은 IEEE 공용 양식에서 항상 필요한 항목은 아니다. Sensors/MDPI 계열이면 필요하지만, IEEE 계열이면
대개 별도 형태이거나 제거될 수 있다. 목표 저널 확정 전까지 placeholder로 유지하되, 제출 직전 반드시
저널 지침에 맞춰 정리해야 한다.

## Figures

현재 Fig.1~Fig.6은 모두 Conclusion 뒤쪽에 있다.

| Figure | 현재 위치 | 권장 위치 |
|---|---|---|
| Fig.1 concept | Conclusion 뒤 | System/Mechanism 첫 언급 근처 |
| Fig.2 carrier bias | Conclusion 뒤 | Mechanism section 근처 |
| Fig.3 static RMSE | Conclusion 뒤 | Static Validation 근처 |
| Fig.4 moving whitening | Conclusion 뒤 | Boundary section 근처 |
| Fig.5 quasi-static | Conclusion 뒤 | Boundary section 근처 |
| Fig.6 CRLB floor | Conclusion 뒤 | Bias Floor 또는 Discussion 근처 |

IEEE는 float가 자동 배치되지만, 소스상 그림을 전부 뒤에 두면 페이지 후반 float-only 경고가 생기기 쉽다.

## Tables

현재 full-width `table*`가 3개다.

| Table | 역할 | 위험 |
|---|---|---|
| Prior art table | novelty 방어 | 필요하지만 넓음 |
| Results table | positive/negative validation 총괄 | 매우 유용하지만 길다 |
| Limitations table | discussion/future work 정리 | 본문 분량이 빡빡하면 supplement 후보 |

분량을 줄여야 하면 우선순위는 다음과 같다.

1. Limitations table 축약 또는 supplement 이동.
2. Results table 일부 행 축약.
3. Prior art table은 유지하되 열 문구를 짧게.

## Section numbering recommendation

- `\section{}`는 유지.
- 수동 번호 삽입 금지.
- Back matter `\section*{}`는 목표 저널에 따라 정리.
- 논문 본문 구조는 9개 section으로 과도하지 않으나, IEEE 짧은 논문이면 Method/Mechanism/Static/Boundary를
  일부 묶는 축약판도 준비 가능.
