# Paper scan findings

## 스캔 대상

- `paper/manuscript.tex`
- 85. Manuscript draft v0
- 89. Manuscript draft v1
- 92. Manuscript v2 통합
- 94. Manuscript v3
- 105. Abstract and back-matter tightening

## 사용한 위험 키워드

`first`, `novel`, `validated`, `prove`, `guarantee`, `all`, `moving`, `quasi`, `0.100`, `0.1 m/s`,
`sub-meter`, `Ocean Engineering`, `elsarticle`, `frequency hopping`, `frequency-agile`, `RMSE`,
`whiten`

## 발견 결과

### 안전한 점

현재 `paper/manuscript.tex`는 주요 위험을 이미 잘 막고 있다.

- “The novelty is therefore not frequency hopping itself”라고 명시.
- Related Work table에서 FH USBL, Costas USBL, frequency-comb/iUSBL 선행을 인정.
- moving target은 “residual whitening”과 “RMSE gain not reliable”로 분리.
- quasi-static은 continuous boundary를 0.005 m/s로 제한.
- 0.030/0.100 m/s는 geometry-dependent recovery로 표현.
- sub-meter long-range claim을 부정.
- real-water/tank validation이 필요하다고 명시.

### 로컬 패치 1: 위치 주석

원고 상단 주석:

```tex
%% Living document. Lives at project root; edited in place across folders.
```

현재 실제 위치는 `paper/`이므로 다음으로 수정했다.

```tex
%% Living document. Lives in local paper/ folder; edited in place across numbered work folders.
```

### 로컬 패치 2: prove 완화

Future work 문장:

```tex
any risk-aware adaptive hopping schedule should first prove that its runtime indicators predict tail degradation
```

논문 톤상 `prove`는 과도하므로 다음으로 완화했다.

```tex
any risk-aware adaptive hopping schedule should first show that its runtime indicators predict tail degradation
```

## 남은 주의점

현재 원고는 안전하지만, 저널 변환이나 초록 압축 과정에서 위험 문장이 다시 생길 수 있다. 특히 다음
세 문장은 어떤 버전에도 들어가면 안 된다.

1. “This is the first frequency-hopping USBL method.”
2. “The method improves moving-target localization.”
3. “The method is validated for quasi-static targets up to 0.1 m/s.”

## 판정

116번 감사 기준으로 원고 claim boundary는 통과. 다음 작업은 Related Work 표/문장 최종화가 더 가치 있다.
