# 123. IEEE section structure alignment

## 목적

사용자가 지적한 “장마다 번호와 분량이 IEEE 양식에 맞는가” 문제를 반영하여, 로컬
`paper/manuscript.tex`의 본문 section 구조를 IEEE 논문지에서 흔히 쓰는 흐름으로 정리했다.

논문 파일 자체는 `paper/` 아래에 있으며 Git에는 올리지 않는다. 이 폴더는 변경 근거와 점검 기록만
보존한다.

## 적용 결과

기존 본문은 9개 primary section이었다.

1. Introduction
2. System and Signal Model
3. Post-Gating DOA Bias Floor
4. Carrier-Sensitive Coherent Interference Mechanism
5. Frequency-Agile Whitening Method
6. Static Validation
7. Whitening Evidence and Applicability Boundary
8. Discussion
9. Conclusion

수정 후 본문은 7개 primary section이다.

1. Introduction
2. Related Work and Problem Statement
3. System Model and UKF Fusion
4. Proposed Carrier-Agile Whitening Method
5. Experimental Validation and Applicability Boundary
6. Discussion
7. Conclusion

세부 진단/기전/스케줄/검증 내용은 subsection으로 내려서 논문 흐름을 정리했다.

## IEEE 기준 해석

IEEE Editorial Style Manual for Authors는 article 구성 순서를 대략
Title Page, Abstract, Index Terms, optional Nomenclature, Introduction, Body, Conclusion,
Appendix, Acknowledgment, References 순으로 제시한다. 또한 primary section heading은 Roman numeral로
enumeration되는 형식이 바람직하다고 설명한다.

따라서 본 원고에서는 수동 번호를 넣지 않고 `\section{}`과 `\subsection{}`만 사용한다. IEEEtran이
최종 PDF에서 `I.`, `II.`, `A.` 형식의 번호를 자동 부여한다.

## 판단

이번 변경은 claim이나 실험 수치를 바꾸지 않는다. 논문 독자가 보는 구조만 조정한 것이다.

- 관련연구와 문제정의는 별도 II장으로 분리했다.
- 기존 Bias Floor / Mechanism / Method 3개 장은 IV장 Proposed Method 아래 subsection으로 묶었다.
- 기존 Static Validation / Whitening Boundary 2개 장은 V장 Results/Boundary 아래 subsection으로 묶었다.
- Discussion과 Conclusion은 IEEE 관례대로 독립 primary section으로 유지했다.

## 남은 조판 작업

다음 작업은 `124. IEEE float layout patch`로 진행하는 것이 좋다.

- 그림 6개가 아직 Conclusion 뒤에 몰려 있으므로 첫 언급 근처로 이동해야 한다.
- full-width `table*` 3개는 분량 압박이 크므로 일부 축약 또는 supplement 이동 후보를 정해야 한다.
- MiKTeX 빌드는 사용자 승인 후 최신 PDF로 재확인해야 한다.

