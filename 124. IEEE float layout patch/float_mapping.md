# Float mapping

## Figure relocation table

| Figure | First reference after patch | Figure environment after patch | 판단 |
|---|---:|---:|---|
| Fig.1 `fig:concept` | line 206 | line 208 | System/observation model 설명 직후 배치. |
| Fig.6 `fig:floor` | line 251 | line 261 | bias floor 근거 문단 직후 배치. |
| Fig.2 `fig:bias` | line 297 | line 308 | carrier-sensitive mechanism 설명 직후 배치. |
| Fig.3 `fig:static` | line 350 | line 357 | static validation 핵심 수치 직후 배치. |
| Fig.4 `fig:moving` | line 381 | line 385 | moving whitening boundary 문단 직후 배치. |
| Fig.5 `fig:quasi` | line 402 | line 405 | quasi-static speed boundary 문단 직후 배치. |

## 변경 전 문제

변경 전에는 모든 figure block이 Conclusion 이후, back matter 이전에 있었다.

```text
Conclusion
Fig.1
Fig.2
Fig.3
Fig.4
Fig.5
Fig.6
Supplementary Materials
...
References
```

이 구조는 LaTeX가 float를 자동 배치하더라도 다음 문제가 생기기 쉽다.

1. 본문 첫 언급과 실제 그림 사이의 거리가 길어진다.
2. IEEE 2단 양식에서 후반부 float-only page warning이 생기기 쉽다.
3. Conclusion 직전/직후의 논리 흐름이 그림 묶음에 의해 끊긴다.

## 변경 후 의도

그림을 “결과가 설명되는 곳”에 가깝게 배치했다. LaTeX가 반드시 그 위치에 고정하지는 않지만,
float 후보 위치가 본문 흐름 안으로 들어왔기 때문에 PDF 조판 가능성이 좋아진다.

