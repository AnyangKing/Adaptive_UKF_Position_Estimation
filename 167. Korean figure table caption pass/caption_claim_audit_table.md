# Caption claim audit table

`paper/manuscript_ko.tex`의 그림/표 캡션 10개를 감사한다.
각 캡션의 근거 폴더·현재 주장·리스크·정책 위반 여부를 표기하고, 개정 필요 여부를 결정한다.
정책은 `caption_policy.md` 참조.

## 감사 결과 요약

| # | 라벨 | 종류 | 근거 폴더 | 현재 주장 요약 | 리스크 | 개정 여부 |
|---|---|---|---|---|---|---|
| 1 | tab:claims | 표 | 166 claim audit, 원고 전체 | claim boundary 표 자체 (문법 안내) | 낮음 (166에서 이미 좁힘) | minor: "이 표를 기준으로 boundary를 잠근다" 서술 강화 |
| 2 | fig:system | 그림 | 원고 개념도 | 논문 개념도, 방법 위치 | 낮음. 자평 표현 없음 | minor: 스탠드얼론 안내 강화 |
| 3 | fig:floor | 그림 | 45번 CRLB, 37-57 한계 | "관측 오차 구조로 이동한 근거" | **정량 없음**·"근거"라는 자평. 캡션이 그림 내용을 설명 안 함 | 개정: 무엇을 보여주는지 + sub-meter 미주장 명시 |
| 4 | fig:tworay | 그림 | **145 two-ray closure + 138** | "직접파와 반사 성분의 상대 위상 변화가 편향 변화를 설명" | 캡션이 "설명" 단정. 기하 fixed / fit R² 언급 없음 | 개정: 기하-fixed prediction임을 명시, 근사·범위 언급 |
| 5 | fig:bias | 그림 | 58번 | "carrier agility가 임의의 heuristic이 아님" 자평 | 자평 문장이 실제 데이터 설명을 밀어냄 | 개정: 데이터 소스·비교 조건 명시, 자평 축소 |
| 6 | tab:validation | 표 | 61/63/82/45 | 핵심 결과 요약 | "중심 표" 자평·미주장 문장 없음 | 개정: 미주장 문장 한 줄, 이동/준정지 경계 문구 |
| 7 | fig:static | 그림 | 61번 | "본 논문의 중심 성능 근거" | **자평 O·미주장 X**. 정지 600 m 한정을 캡션에서 다시 잠글 필요 | 개정: 거리·독립검증 명시, "다른 거리·이동으로 확대하지 않음" |
| 8 | fig:moving | 그림 | 63번 | whitening 확인, RMSE 미재현 | 좋음 (미주장 이미 있음) | minor: "이 결과는 성능 개선 근거가 아니다" 명시 강화 |
| 9 | fig:quasistatic | 그림 | 82번 | 비단조 + 0.005 m/s 제한 | 좋음 | minor: "0.030/0.100 양성은 기하 의존 회복" 짧게 |
| 10 | tab:limitations | 표 | 37-57, 64-67, 160, 162 | 실패 배치 표 | 좋음 (162 post-hoc, 160 tail 명시됨) | minor: 162 "본문 성능 claim 금지" 문구 캡션에서도 재확인 |

## 개정 계획

핵심 개정 대상은 **fig:floor, fig:tworay, fig:bias, tab:validation, fig:static** 다섯이다.
공통 방향은:

1. **자평 문장을 데이터 설명 문장으로 대체**
2. **미주장 문장 추가** (정지=거리 한정, 이동=RMSE 미주장, 준정지=경계, 기전=근사)
3. **post-hoc/개발표본/근사 표시**
4. **수치는 본문에 이미 있는 것만, 재확인 문장에서만 사용**

세부 diff는 `caption_changes.md`에 before/after로 기록한다.

## 원천 대조 근거 (166과 정합)

- 61번: 600 m fixed 13.01 → agile 8.87, paired +4.14, p=0.0008, 20 geometries 독립 seed
- 63번: lag-1 +0.470 → -0.208, pooled RMSE gain -0.10 m p=0.301
- 82번: 132 paired, 11.98 → 10.49 m, p=8.00e-5, continuous safe 0.005 m/s
- 45번: 600 m routed UKF 12.29 m vs 경험적 CRLB 11.80 m, 잔여 bias floor ≈ 3.45 m
- 138/145: two-ray fit, 기하 기반 delta prediction, 진동 근사
- 160: four-cycle 신규 20기하에서 1/20 발산, 개선 미유의 (본문에서 사용 불가)
- 162: post-hoc guard pilot, 독립검증 전
