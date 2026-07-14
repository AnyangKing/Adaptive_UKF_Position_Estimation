# 135. 검증실험 원고 통합 대확장

## 목적 (사용자 지시)

"연구한 것들이 있는데 왜 안 쓰냐 — 다 원고에 넣어줘." 원고가 9쪽으로 얇았던 근본 원인은 43~82번에서
**검증까지 끝낸 실험들이 원고에 안 들어가 있었기 때문**(원고를 105번 압축요약본에서 조립). 이 폴더
에서 그 검증 실험들을 `paper/manuscript.tex`에 정확한 수치·caveat 그대로 편입했다(새 실험 0, 과장 0).

## 편입한 실험 (전부 기존 검증 데이터)

| 폴더 | 편입 위치 | 내용 |
|---|---|---|
| **43** | 신설 §Baseline/Estimator Comparison + **Table II** | EKF/UKF/NLS 비교(EKF 장거리 발산 31/25%·RMSE 17.25m, UKF 강건 승자, NLS RMSE 최저지만 속도·일관성 없음, 전 추정기 NEES≫3=미모델링 편향) |
| **44·46** | 신설 §Baseline/Adaptive-R Routing + **Table III** | 라우팅 ablation −17%(200m −47%)·발산 5→0%·NEES 341→27; 160궤적 대규모 확정 +1.04m CI[+0.42,+1.86] p=0.0006 |
| **45** | §Post-Gating Bias Floor + **Table IV** | 경험적 CRLB 효율(η 1.57/1.38 다중ping 이득, 600m η=0.92), **bias floor √(12.29²−11.80²)=3.45m** 유도 |
| **48** | 신설 §Robustness | 음속 ±15m/s +25%·±30 +50%(graceful, 발산≤3%), 클럭 1ms +6%(TDOA 상쇄·DOA 면역) |
| **54** | §Carrier-Agile Schedule | 30–34kHz 대역 선택 근거: 32kHz=λ/2 최적, 48/64kHz 공간 aliasing P90 12–17° |
| **58** | §Mechanism | 장거리 편향의 78–92%가 반송파-진동 성분, 게이트 기하 정합(600m 게이트 안↔100m 밖), hop평균 600m 0.632°→0.053° |
| **64–67** | §Discussion | 이동표적 안전화 4시도(R팽창·jump gate·anchor-hop·조건분기) 전부 미재현 — 정직한 음성결과로 경계 방어 |
| **82** | §Motion Boundary + **Table (quasi)** | 준정지 속도별 전표(0/0.005 validated, 0.010/0.050 not, 비단조) |

## 결과 (2026-07-13)

- **원고 9쪽 → 11쪽.** 표 3개 신설(추정기·라우팅·CRLB) + 준정지 표 + 강건성 절 + 기전 정량 + 음성결과.
- `cd paper && latexmk manuscript.tex` → **미해결 인용/참조 0, overfull 0, 11쪽.** 새 라벨
  (sec:model·sec:floor)·표참조(tab:estimators/routing/crlb/quasi) 모두 해결. 하드코딩 섹션참조 없음.
- 페이지 렌더 확인: Table II/III/IV IEEE 스타일 정상 조판, CRLB 유도식 본문 정상.

## 판정

**검증실험 통합 완료 — "연구는 충실한데 논문이 얇다"는 병목 해소.** 원고가 이제 baseline 신뢰성
(추정기 비교·라우팅 ablation·대규모 통계)·이론 근거(CRLB floor)·강건성·설계근거(주파수)·기전 정량·
정직한 음성결과까지 갖춘 풀 렝스에 근접.

## 남은 것 (정직하게)

여전히 **실해역 검증은 없음**(시뮬 기반, 사용자가 나중에 실측 예정) — IEEE JOE major-revision
리스크의 핵심은 그대로. 추가로 **문헌 리뷰가 아직 얇음**(참고문헌은 131에서 10편으로 늘렸으나
Related Work 서술은 더 확장 필요) — 이건 "안 쓴 연구"가 아니라 새 문헌조사라 별도 작업. 다음 후보:
Related Work 확장(문헌 20~40편 규모) + 기전 해석모델.
