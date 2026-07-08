# 69. 논문 그림 생성 준비

## 목적

68번에서 선행연구 포지셔닝을 정리했으므로, 다음 단계는 논문 그림 생성이다. 이 폴더는 실제 그림을 그리기 전, `논문_초고_구조.md`의 그림 후보 7종이 어떤 원천 데이터에 의존하는지 감사하고 고정한다.

## 실행

```powershell
python audit_figure_sources.py
```

생성 파일:

- `figure_source_manifest.json`

## 그림 후보별 원천 데이터 상태

| 그림 | 내용 | 원천 | 상태 |
|---|---|---|---|
| Fig. 1 | 시스템 + 게이트-내 표면반사 누설 개념도 | 원고 도식 + channel model | 수동 도식 필요 |
| Fig. 2 | bias vs carrier 곡선 | 58번 `results/agility.json` | 사용 가능 |
| Fig. 3 | 정지 600 m fixed vs hop paired RMSE | 61번 `results/static_hop_validation.json` | 사용 가능 |
| Fig. 4 | lag-1 자기상관 fixed vs hop | 63번 `results/moving_validation.json` | 사용 가능 |
| Fig. 5 | 정지/이동 × fixed/hop 2×2 요약 | 59/61/63 README + JSON | 부분 가능 |
| Fig. 6 | 배열 회전대칭 편향 상관 | 42번 `results/geometry_diversity.json` | 사용 가능 |
| Fig. 7 | CRLB vs 실측 + bias floor | 45번 `results/crlb.json` | 사용 가능 |

## 추출된 핵심 수치

### Fig. 2: bias vs carrier

- 400 m hop 평균 편향 감소율: 78.35%
- 600 m hop 평균 편향 감소율: 91.57%
- 600 m 32 kHz median abs bias: 0.632 deg
- 600 m hop-average median abs bias: 0.053 deg

### Fig. 3: 정지 600 m paired RMSE

- fixed mean RMSE: 13.0065 m
- hop mean RMSE: 8.8698 m
- mean improvement: +4.1368 m
- Wilcoxon p: 0.000845
- fixed median: 13.9663 m
- hop median: 7.9577 m

### Fig. 4: moving-target whitening boundary

- 이동 표적 pooled RMSE gain: -0.103 m
- pooled p: 0.301
- lag-1 fixed mean: +0.470
- lag-1 hop mean: -0.208
- lag-1 p: 5.56e-10

### Fig. 7: CRLB vs floor

- 600 m empirical CRLB: 11.800 m
- 600 m routing UKF RMSE: 12.292 m
- 600 m bias floor: 3.446 m

## 70번 권장 작업

다음 폴더는 `70. 논문 그림 1차 생성`으로 잡는 것이 좋다.

권장 순서:

1. Fig. 2 `bias vs carrier`
2. Fig. 3 `static paired RMSE`
3. Fig. 4 `lag-1 whitening`
4. Fig. 7 `CRLB vs RMSE`
5. Fig. 6 `array rotation bias correlation`
6. Fig. 5 `static/moving 2×2 summary`
7. Fig. 1 conceptual diagram

먼저 정량 그림 4개(Fig. 2, 3, 4, 7)를 만들면 원고 본체의 설득력이 빠르게 올라간다.

## 주의

- `results/` 폴더는 `.gitignore`에 의해 GitHub에는 올라가지 않는 경우가 많다. 하지만 로컬에는 현재 주요 JSON이 남아 있다.
- 그림 생성 스크립트는 원천 JSON이 없을 때 README 수치를 fallback으로 쓰기보다, 가능한 한 JSON에서 직접 읽어야 한다.
- 59번 데이터는 Fig. 5에 필요하지만 JSON 원천이 명확하지 않으므로 70번에서 README 수치 사용 또는 재실행 여부를 결정해야 한다.
