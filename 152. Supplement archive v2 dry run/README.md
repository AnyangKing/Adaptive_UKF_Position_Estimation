# 152. Supplement archive v2 dry run

## 목적

120번 보충자료 dry run을 현재 12쪽 원고와 145번 two-ray evidence closure 기준으로 갱신한다.
실제 ZIP이나 원본 복사본은 만들지 않고, 투고용 보충자료에 들어갈 후보 파일의 경로·크기·SHA256을
고정해 재현성 패키지의 드리프트를 자동 검사한다.

## 실행

```powershell
python "152. Supplement archive v2 dry run\validate_supplement_v2.py"
```

현재 manifest를 의도적으로 갱신할 때만:

```powershell
python "152. Supplement archive v2 dry run\validate_supplement_v2.py" --write
```

## 포함 범위

- 핵심 결과: CRLB, carrier sensitivity, 정지·이동·준정지 검증, Method facts, two-ray fit.
- 핵심 코드: 45, 58, 61, 63, 82, 93, 145번의 Python·README·result summary.
- 그림: 로컬 `paper/figures/`의 7개 PNG와 two-ray SVG.
- 그림 생성 코드: 70, 95, 101, 145번.
- 문서: claim traceability, figure/table source manifest, submission policy, current state.

## 명시적 제외

- `paper/manuscript.tex`, `paper/manuscript.pdf` 및 LaTeX 부산물.
- 루트 인계·공부·교수 보고 파일.
- `.git/`, `.claude/`, `study_exports/`, `__pycache__/`.
- 실제 ZIP과 원본 파일 복사본.

## 주장 경계

이 패키지는 **simulation-based evidence**를 재현하기 위한 것이다. 이동 표적에서 잔차 백색화는
검증됐지만 pooled RMSE 개선은 주장하지 않으며, 준정지 연속 경계는 0.005 m/s까지만 검증된 상태다.

## 판정

보충자료 공개 범위를 결정하기 전에도 안전하게 실행 가능한 dry run이다. manifest 검사가 통과하면
후속 패키징 시 어떤 파일이 바뀌었는지 즉시 탐지할 수 있다.
