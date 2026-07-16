# Patch record

## 1. Related Work hbox cleanup

변경 위치:

```text
Direction-of-arrival estimation paragraph
```

변경 내용:

- 긴 `broadband, reverberant, multipath-rich acoustics---closer ...` 문장을 짧게 분할.
- SRP-PHAT/GCC-PHAT 설명을 두 문장으로 나누어 줄바꿈 여지 확보.

Claim 영향:

- 없음. 선행연구와 방법 선택 설명은 유지.

## 2. Estimator Comparison hbox cleanup

변경 위치:

```text
Baseline Tracking Performance / Estimator Comparison
```

변경 내용:

- 하나의 긴 문단을 두 문단으로 분할.
- `identical TOA/TDOA/DOA measurements`를 `same acoustic observations`로 완화.
- EKF/NLS/UKF 수치와 해석은 유지.

Claim 영향:

- 없음. EKF collapse, NLS snapshot, UKF backbone justification 모두 유지.

## 3. Overfull equation cleanup

변경 위치:

```text
two-source glint bias equation
```

변경 전:

```latex
\begin{equation}
b(f)=...=\Delta\varepsilon\,\frac{...}{...},\qquad \phi=...
\end{equation}
```

변경 후:

```latex
\begin{align}
b(f)&=... \nonumber\\
&=\Delta\varepsilon\,\frac{...}{...},\\
\phi&=...
\end{align}
```

Claim 영향:

- 없음. 수식 의미는 동일하고 line break만 개선.

