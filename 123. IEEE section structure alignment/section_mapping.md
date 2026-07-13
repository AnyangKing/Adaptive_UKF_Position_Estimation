# Section mapping

## Before to after

| 기존 section | 수정 후 위치 | 이유 |
|---|---|---|
| Introduction | I. Introduction | 유지. 연구 동기와 출발점 설명. |
| System and Signal Model | III. System Model and UKF Fusion | IEEE 논문에서 흔한 system/model 절로 명확화. |
| Post-Gating DOA Bias Floor | IV-A. Post-Gating DOA Bias Floor | 독립 장보다 proposed method의 문제 진단 subsection이 자연스러움. |
| Carrier-Sensitive Coherent Interference Mechanism | IV-B. Carrier-Sensitive Coherent Interference Mechanism | proposed method의 물리 기전 subsection으로 이동. |
| Frequency-Agile Whitening Method | IV-C. Carrier-Agile Transmission Schedule | proposed method의 실제 방법 subsection으로 이동. |
| Static Validation | V-A. Static Long-Range Validation | 결과 section 안의 핵심 positive validation으로 이동. |
| Whitening Evidence and Applicability Boundary | V-B. Whitening Evidence and Motion Boundary | 결과 section 안의 mechanism/boundary subsection으로 이동. |
| Discussion | VI. Discussion | 유지. 해석, novelty boundary, limitation 정리. |
| Conclusion | VII. Conclusion | 유지. IEEE style manual도 Introduction, Conclusion은 singular head로 다룬다. |

## 새로 추가한 primary section

`II. Related Work and Problem Statement`를 추가했다.

기존 Introduction 안에 있던 frequency agility / USBL prior-art positioning 내용과 Table 1은 사실상
related-work boundary 역할을 하고 있었다. 이를 II장으로 분리하면 Introduction이 과밀해지는 것을 줄이고,
리뷰어가 novelty 방어 논리를 더 빨리 찾을 수 있다.

## 최종 구조

```text
I. Introduction
II. Related Work and Problem Statement
III. System Model and UKF Fusion
    A. Implementation Parameters
IV. Proposed Carrier-Agile Whitening Method
    A. Post-Gating DOA Bias Floor
    B. Carrier-Sensitive Coherent Interference Mechanism
    C. Carrier-Agile Transmission Schedule
V. Experimental Validation and Applicability Boundary
    A. Static Long-Range Validation
    B. Whitening Evidence and Motion Boundary
VI. Discussion
VII. Conclusion
```

## 주의

LaTeX source에는 위 번호를 직접 쓰지 않는다. 위 번호는 IEEEtran이 PDF에서 자동 생성할 논리 구조를
설명하기 위한 기록이다.

