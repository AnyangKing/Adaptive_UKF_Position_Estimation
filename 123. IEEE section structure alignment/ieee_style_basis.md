# IEEE style basis

## 확인한 공식 기준

확인일: 2026-07-13

공식 문서:

- IEEE Editorial Style Manual for Authors, updated 29 July 2024.
- IEEE Author Center Journals, Create the Text of Your Article.

핵심 기준:

1. IEEE article body는 일반적으로 Introduction, Body of Article, Conclusion 흐름을 가진다.
2. primary section heading은 Roman numeral로 enumerate되는 형식이 바람직하다.
3. secondary heading은 `A.`, `B.` 형식으로 enumerate된다.
4. Introduction, Conclusion, Acknowledgment는 singular head로 취급한다.
5. 논문 작성자는 수동 번호를 넣기보다 template의 heading command를 써야 한다.

## 본 원고에 적용한 해석

본 연구는 수중 USBL/센서퓨전/신호처리 성격이 강하므로, IEEE Transactions/Journal 계열에서 흔히 보이는
다음 구조가 적합하다.

```text
Introduction
Related Work / Problem Statement
System Model
Proposed Method
Experimental Results
Discussion
Conclusion
```

이번 변경은 이 관례에 맞춰 9개 primary section을 7개 primary section으로 압축한 것이다.

## 왜 7장이 적당한가

6장 구조도 가능하지만, 본 논문은 novelty boundary가 매우 중요하다. frequency hopping 자체가 새롭지
않고, 본 논문의 기여는 “post-gating coherent DOA bias whitening in USBL TOA/TDOA/DOA-UKF”로 좁게
잡아야 한다. 그래서 Related Work and Problem Statement를 독립 II장으로 두는 편이 리뷰어 방어에 유리하다.

8장 이상으로 가면 Bias Floor, Mechanism, Schedule, Static Result, Boundary가 각각 독립 장처럼 보여
짧은 IEEE 논문에서는 산만해진다. 따라서 IV장 Proposed Method와 V장 Results/Boundary 아래 subsection으로
묶는 편이 더 자연스럽다.

