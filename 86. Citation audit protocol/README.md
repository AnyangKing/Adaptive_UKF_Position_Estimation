# 86. Citation audit protocol

## 목적

85번 원고 v0에 남아 있는 citation placeholder를 안전하게 치환하기 위한 audit protocol을 만든다.

이번 폴더는 “최종 참고문헌 확정”이 아니다. 검색/DB 접근이 불안정하거나 원문 접근이 필요한 상태에서 임의로 citation을 확정하면 reviewer risk가 커진다. 따라서 86번은 다음 작업자가 IEEE Xplore, Google Scholar, Scopus, Web of Science, 학교 도서관 DB에서 정확히 검증할 수 있도록 후보 문헌, 검색어, 확인 항목, 원고 치환 위치를 정리한다.

## 포함 파일

- `citation_audit_matrix.md`: placeholder별 후보 문헌과 검증 항목
- `search_query_plan.md`: DB별 검색어
- `placeholder_replacement_plan.md`: 원고 v0에서 어디를 어떤 종류의 citation으로 바꿀지
- `bibtex_stub.md`: 검증 전 임시 BibTeX stub

## 핵심 원칙

1. 확인되지 않은 문헌은 final reference로 쓰지 않는다.
2. radar frequency agility와 USBL frequency-hopping prior art는 반드시 먼저 인정한다.
3. 우리 novelty는 “frequency hopping 자체”가 아니라 post-gating coherent multipath DOA-bias whitening mechanism, UKF tracking validation, boundary analysis다.
4. DOI, page, venue, author spelling은 원문/DB로 확인한다.

## 다음 단계

87번에서는 실제 DB 접근이 가능하면 exact citation audit을 수행하고, 가능하지 않으면 Introduction/Related Work 문장을 placeholder-safe 형태로 유지한 채 원고 v1을 진행한다.
