# 121. Submission readiness dashboard

## 목적

115~120번에서 교수님 부재 중 진행 가능한 논문 마감 보강을 순서대로 수행했다. 121번은 그 결과를
한 장짜리 상태판으로 묶어, 다음 AI나 사용자/교수님이 바로 현재 위치를 이해할 수 있게 만든다.

## 현재 판정

**논문은 “과학적 결과·재현성·claim boundary·선행연구 방어·future validation plan”까지 정리된 상태다.**
남은 것은 대부분 사람 결정이다.

- 저자/소속/교신저자/ORCID
- Funding / Conflict / Data availability 문구
- 목표 저널
- simulation 중심 투고 vs real-water 선행 여부
- 보충자료 공개 정책

## 115~120 결과 요약

| 폴더 | 주제 | 결과 |
|---|---|---|
| 115 | Reproducibility package audit | 핵심 claim→JSON/코드/그림 매핑 완료 |
| 116 | Manuscript claim boundary audit | 원고 claim 안전성 확인, `paper/` 로컬 원고 소규모 패치 |
| 117 | Related work table finalization | FH USBL/Costas/comb/radar glint 방어표와 reviewer response 정리 |
| 118 | Real-water validation plan | 수조/호수/해상 3-tier 검증 프로토콜 작성 |
| 119 | Carrier schedule ablation plan | 30–34 kHz schedule을 “최적”이 아닌 frozen validation schedule로 방어 |
| 120 | Supplement archive dry run | raw data 없이 해시 manifest/ZIP 구조/수집 절차 정리 |

## GitHub 상태

115~121 같은 numbered folder만 push 대상이다. `paper/`, 루트 운영 MD, 교수님 보고서, study files,
raw results는 기본적으로 GitHub에 올리지 않는다.

## 다음 권장

지금 당장 추가 연구를 계속한다면 122번 후보는 둘 중 하나다.

1. `122. Journal target decision matrix`
   - 교수님 없이도 각 저널의 장단점·field validation 요구 수준·template 부담을 비교.
2. `122. Final local paper build check`
   - `paper/`의 현재 LaTeX를 로컬에서 다시 빌드하고, 116번 로컬 패치 후 PDF 상태 확인.

내 추천은 **Final local paper build check**다. 116번에서 원고를 아주 작게 고쳤기 때문에, paper는 GitHub에
올리지 않더라도 로컬 PDF가 깨지지 않는지 확인해두는 편이 깔끔하다.
