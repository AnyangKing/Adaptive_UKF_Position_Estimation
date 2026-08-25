# 242. DOI bibliography verification

## 목적

원고의 참고문헌 22편에 DOI가 실제로 존재하는지, 그리고 논문 방어 구조에서 중요한 고위험 문헌의 서지·역할이 현재 `paper/refs.bib` 및 Related Work 서술과 맞는지 감사했다.

이 작업은 원고 내용 패치와 성격이 다르므로 241번과 분리했다.

## 결론

- 현재 `paper/refs.bib` 기준으로는 “DOI 0개”가 아니다.
- 22개 BibTeX entry 모두 DOI 필드가 있다.
- 핵심 고위험 문헌 9개에 대해 DOI marker를 자동 감사 대상으로 고정했다.
- `Zhang2019USBLCalib`의 page range는 출판사 페이지 기준 `254--262`가 맞아 로컬 `paper/refs.bib`를 보정했다.
- `Qian2025FrequencyCombIUSBL`은 frequency-hopping USBL 선행연구가 아니라 acoustic frequency-comb / iUSBL integrated waveform 선행연구로만 사용해야 한다. 현재 Related Work 표의 문구는 이 경계 안에 있다.

## 감사 방법

1. `paper/refs.bib`를 기계 파싱해 entry 수와 DOI 누락 여부를 확인했다.
2. 논문 방어 구조에 직접 걸리는 고위험 문헌을 웹/출판사/색인 페이지로 대조했다.
3. DOI와 page marker를 `audit_refs_bib_doi.py`에 고정해 이후 회귀를 잡도록 했다.

## 실행

```powershell
python "242. DOI bibliography verification\audit_refs_bib_doi.py"
```

예상 결과:

```text
PASS: refs.bib has 22 entries, 22 DOI fields, and checked high-risk DOI/page markers.
```

## Git 규칙

커밋 대상은 이 번호 폴더만이다.

- `git add -- "242. DOI bibliography verification"`
- commit message: `242. DOI bibliography verification`

`paper/refs.bib` 보정은 원고/논문 파일과 같은 로컬 전용 작업물이며, 사용자 지시 전에는 GitHub에 올리지 않는다.
