# LaTeX warning triage

## 사용자 질문

LaTeX Workshop으로 빌드하면 Problems 창에 약 15개 문제가 뜬다. 신경 써야 하는가?

## 답

현재 프로젝트 로그 기준으로는 대부분 신경 쓰지 않아도 된다.

영문 논문 `paper/manuscript.tex`의 최종 로그에서는 다음이 확인됐다.

| 항목 | 상태 |
| --- | --- |
| fatal error | 없음 |
| undefined citation | 없음 |
| undefined reference | 없음 |
| overfull hbox | 없음 |
| PDF output | 성공 |
| remaining warning | underfull vbox only |

한글 독해본은 긴 영어 용어와 수식이 한글 문장 안에 섞여 있어 `Underfull \hbox`가 더 많이 뜬다. 이것은 한글 독해용 파일의 줄나눔 문제에 가깝고, 영문 제출 원고의 치명적 문제는 아니다.

## 실제로 위험한 경고

아래 메시지는 무시하지 않는다.

```text
! LaTeX Error
Undefined control sequence
Citation ... undefined
Reference ... undefined
Overfull \hbox (... too wide)
File `...' not found
```

## 현재 유지할 방침

- Problems 창에 underfull만 뜨면 논문 독해/수정은 계속 진행한다.
- 최종 투고 직전에는 Problems 창보다 `manuscript.log`에서 fatal/undefined/overfull 여부를 기준으로 판단한다.
- 그림은 PDF/vector-first workflow를 유지한다.
