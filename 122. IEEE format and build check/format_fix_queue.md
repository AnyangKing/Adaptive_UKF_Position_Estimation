# Format fix queue

## P1. 최신 PDF 재빌드

우선순위: 최상

116번에서 `paper/manuscript.tex`가 소규모 수정되었으므로 기존 PDF는 최신이 아니다. 사용자 승인 후 아래
명령으로 재빌드한다.

```powershell
cd "C:\Users\HOSEO\OneDrive - 호서대학교\나는 개인이요\석사생\논문\Adaptive UKF 위치추정\paper"
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

## P2. Figure 위치 재배치

우선순위: 높음

현재 Fig.1~Fig.6이 모두 Conclusion 뒤에 몰려 있다. 다음 패치에서 각 figure environment를 첫 언급 이후로
이동한다.

권장:

- Fig.1: System and Signal Model 끝 또는 Mechanism 앞.
- Fig.2: Carrier-Sensitive Mechanism section 내부.
- Fig.3: Static Validation section 내부.
- Fig.4/Fig.5: Boundary section 내부.
- Fig.6: Bias Floor section 또는 Discussion 첫 부분.

## P3. Table 분량 축약

우선순위: 중간~높음

`table*` 3개는 IEEE 7쪽 내외 원고에서 부담이 크다.

권장 축약:

- Limitations table은 5행에서 3~4행으로 축약하거나 supplement로 이동.
- Results table은 quasi-static speed별 행을 Fig.5와 supplement로 넘기고 본문 표는 summary만 남길 수 있다.
- Prior art table은 열 제목과 문장을 짧게 다듬는다.

## P4. Back matter 정리

우선순위: 목표 저널 확정 후

현재 back matter는 placeholder다. IEEE 계열이면 Author Contributions/Funding/Data Availability 등이
현재 형태 그대로 필요하지 않을 수 있다. 저널 확정 전에는 지우지 말고, 제출 직전 템플릿에 맞춘다.

## P5. Page budget 목표

현재 기존 PDF는 7쪽이었다. IEEE 계열에서 일반적으로 6~8쪽 수준이면 초안으로는 괜찮지만, full-width 표와
float-only page warning이 있으므로 목표는 다음과 같다.

- 1차 목표: 7쪽 유지, float-only page 제거.
- 2차 목표: 필요 시 6쪽대 축약.
- 절대 금지: claim 안전문장 제거로 분량 줄이기.

## P6. 번호/장 제목 정책

IEEEtran이 자동으로 I, II, III 번호를 붙인다. 따라서 장 제목에 `1. Introduction`처럼 수동 번호를 넣지
않는다.
