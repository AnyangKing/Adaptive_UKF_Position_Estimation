# 133. 저자 인계 체크리스트 (원고 마무리용)

## 목적

130~132로 원고의 **AI가 채울 수 있는 부분(레이아웃·참고문헌·수치정합)**은 마무리됐다. 이 문서는
**사람(저자/지도교수)만 채울 수 있는 것**을 `paper/manuscript.tex`의 정확한 위치와 함께 짚어,
저자가 5분 안에 무엇을 어디에 넣어야 하는지 알 수 있게 한다.

## ✅ AI가 완료한 것 (검증됨)

- 원고: IEEEtran journal, **9쪽**, 컴파일 정상(미해결 인용/참조 0, overfull 0). `cd paper && latexmk manuscript.tex`.
- 그림 6종·표 3종 전부 첫 언급 근처 배치, 전 페이지 시각 QA 통과(130).
- 참고문헌 **10편**, 전부 Crossref 검증(131). 방법(GCC/SRP/UKF/Thorp)+선행연구.
- 헤드라인 수치 초록·본문·표·캡션 전수 정합, 불일치 1건 수정(132).
- claim 경계 무결(sub-meter 미주장·first-FH 미주장·moving 개선 미주장).
- 선행연구 원문 대조 완료(논문_초고_구조.md 노벨티 섹션): novelty 안전.

## ★ 사람이 채워야 할 것 (paper/manuscript.tex 위치)

| 항목 | 위치(행) | 현재 상태 → 저자가 넣을 것 |
|---|---|---|
| 저자명·소속·교신저자·ORCID | `\author{}` **~29행** | "to be completed" → 실제 저자/소속 |
| Author Contributions | **~732행** | "decision required" → CRediT 등 기여 문구 |
| Funding | **~735행** | placeholder → 펀딩 문구(없으면 저널 무펀딩 문구) |
| Data Availability | **~739행** | 초안 문구 → 실제 URL/DOI 또는 접근정책 확정 |
| Acknowledgments | **~745행** | placeholder → 감사문(없으면 삭제 가능) |
| Conflicts of Interest | **~749행** | placeholder → 무충돌 문구 등 |

## ★ 결정만 하면 되는 것 (원고 밖)

1. **목표 저널** — 미정. 정해지면 그 저널 양식으로 전환(IEEEtran은 범용 작업양식). 후보·비교는
   지도교수_보고_요약.md.
2. **투고 전 실해역/수조 검증 여부** — 현재 시뮬 기반. 118번에 3-tier 검증계획 있음.
3. **데이터/코드 공개 정책** — GitHub/Zenodo·Figshare DOI/supplementary/요청시 중 택1.

## 저자가 원고 열어보는 법

```
cd paper
latexmk manuscript.tex     # → manuscript.pdf (9쪽)
```
PDF만 빠르게 보려면 `paper/manuscript.pdf`(빌드 후 생성). MiKTeX 없으면 지도교수_보고_요약.md의
수치·그림으로도 검토 가능.

## 판정

**원고는 "저자 정보/저널만 채우면 투고 준비 완료" 상태.** AI가 사람 개입 없이 할 수 있는 원고
내적 작업은 130~133으로 소진. 다음 실질 진전은 위 사람 결정 사항 입력이 필요하다.
