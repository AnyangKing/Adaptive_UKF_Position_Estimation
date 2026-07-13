# 122. IEEE format and build check

## 목적

사용자가 지적한 대로, 현재 원고는 과학 내용만이 아니라 **IEEE 양식의 장 번호, 분량, float 배치**를
확인해야 한다. 122번은 로컬 `paper/manuscript.tex`를 대상으로 IEEEtran 관점의 정적 포맷 감사와 빌드
상태를 기록한다.

## 결론

원고는 IEEEtran 문법상 numbered section을 자동 생성하는 구조이지만, 투고형 조판 관점에서는 보완할 점이
남아 있다.

1. `\section{}`는 자동으로 I, II, III 번호가 붙는다. 수동 번호를 넣으면 안 된다.
2. 현재 본문 numbered section은 Introduction부터 Conclusion까지 9개로, IEEEtran이 자동 번호를 붙인다.
3. `Author Contributions`, `Funding`, `Data Availability`, `Acknowledgments`, `Conflicts of Interest`는
   `\section*{}` back matter placeholder이며, IEEE 공용 저널 양식에서는 목표 저널 확정 후 제거/축약/이동
   판단이 필요하다.
4. Fig.1~Fig.6이 모두 Conclusion 뒤쪽에 몰려 있어, IEEE 제출 전에는 각 그림을 첫 언급 근처로 옮기는
   float 배치 정리가 필요하다.
5. `table*`가 3개라 분량 압박이 크다. 최소 1개는 축약하거나 supplement로 이동할 수 있다.

## 빌드 상태

최신 `paper/manuscript.tex`는 2026-07-13 12:30에 수정되었고, 기존 `manuscript.pdf`는 2026-07-13 10:55
산출물이다. 즉 PDF는 최신 tex보다 오래되었다.

이번 턴에서 `pdflatex → bibtex → pdflatex ×2`를 실행하려 했지만, 샌드박스 안에서는 MiKTeX가
`C:\Users\HOSEO\AppData\Roaming\MiKTeX\2.9`를 만들지 못해 실패했다. 승인 권한 실행은 자동 검토에서
거부되어 최신 PDF 재빌드는 완료하지 못했다.

따라서 122번의 빌드 판정은 다음과 같다.

- 기존 PDF: 7 pages, 1,705,396 bytes.
- 기존 로그: unresolved citation/reference 없음, Overfull 1건(3.29744pt), Underfull 1건, page 6 float-only warning.
- 최신 tex 기준 PDF 재생성: **사용자 승인 후 필요**.

## 산출물

- `ieee_structure_audit.md`: section/table/figure/back-matter 구조 감사.
- `format_fix_queue.md`: 다음 원고 패치 우선순위.
- `build_status.md`: 빌드 시도와 현재 한계.

## 다음

사용자 승인이 가능하면 다음은 `paper/`에서 실제 빌드 재확인이다. 승인 없이 계속한다면 123번에서
`IEEE float/layout patch plan`을 만들고, 그림·표 위치를 옮기는 로컬 원고 패치를 준비하는 것이 좋다.
