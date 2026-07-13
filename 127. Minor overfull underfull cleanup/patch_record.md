# Patch record

## Overfull cleanup

변경 전:

```latex
residual entering TOA/TDOA/DOA-UKF fusion
```

변경 후:

```latex
residual entering UKF fusion
```

이유:

- prior-art table의 좁은 column에서 slash/hyphen 조합이 줄바꿈을 방해했다.
- 해당 행은 already present-work row이므로, TOA/TDOA/DOA 세부는 본문과 abstract에서 충분히 설명된다.
- 표에서는 “UKF fusion”으로 줄여도 과학적 claim 손실이 없다.

## Underfull cleanup

변경 전:

```latex
The fixed-carrier baseline uses $f_k=32~\mathrm{kHz}$.
The frequency-agile policy uses a frozen 20-ping linear sweep ...
```

변경 후:

```latex
The baseline uses a fixed 32~kHz carrier, whereas the frequency-agile policy uses a frozen 20-ping
linear sweep ...
```

이유:

- 짧은 문장과 수식형 주파수 표기가 IEEE 2단 column에서 어색한 spacing을 만들었다.
- 같은 의미를 더 자연스러운 문장으로 바꿔 underfull warning을 제거했다.

## Claim safety

보존된 내용:

- fixed 32 kHz baseline.
- frozen 20-ping 30--34 kHz sweep.
- receiver-side TOA/TDOA/DOA observation vector unchanged.
- adaptive-R UKF backbone unchanged.
- performance difference is attributed to residual temporal structure, not a different estimator.

