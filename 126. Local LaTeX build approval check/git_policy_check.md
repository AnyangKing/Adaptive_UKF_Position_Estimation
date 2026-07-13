# Git policy check

## 확인 사항

이번 빌드로 `paper/` 내부의 다음 파일들이 갱신되었다.

- `manuscript.pdf`
- `manuscript.log`
- `manuscript.aux`
- `manuscript.bbl`
- 기타 LaTeX auxiliary files

하지만 `paper/`는 Git ignored 상태다.

확인 출력:

```text
!! paper/
```

## 적용 원칙

이번 commit/push 대상은 126번 기록 폴더뿐이다.

논문 원고, PDF, aux/log 산출물은 GitHub에 올리지 않는다.

