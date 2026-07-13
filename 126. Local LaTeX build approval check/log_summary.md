# Log summary

## Final log extraction

검색 패턴:

```powershell
Select-String -LiteralPath "manuscript.log" -Pattern "Output written|Overfull|Underfull|float-only|undefined|Rerun|Warning|Citation|Reference"
```

중요 출력:

```text
Overfull \hbox (3.29744pt too wide) in paragraph at lines 140--140
Underfull \hbox (badness 1742) in paragraph at lines 319--325
Package rerunfilecheck Info: File `manuscript.out' has not changed.
Output written on manuscript.pdf (7 pages, 1708038 bytes).
```

## 해석

### Good

- PDF 생성 성공.
- 7쪽 유지.
- `float-only` warning 없음.
- unresolved citation/reference 없음.
- rerun 필요 없음.

### Remaining minor warnings

1. `Overfull \hbox (3.29744pt too wide) in paragraph at lines 140--140`
   - 위치: prior-art table의 끝부분.
   - 원인 후보: `TOA/TDOA/DOA-` 같은 긴 slash/hyphen 조합.
   - 위험도: 낮음. 3.3pt 수준.
2. `Underfull \hbox (badness 1742) in paragraph at lines 319--325`
   - 위치: Frequency-Agile Transmission Schedule subsection 첫 문단.
   - 원인 후보: 수식/주파수 표기와 짧은 문장 조합.
   - 위험도: 낮음.

## 결론

현재 원고는 “빌드 가능 + 7쪽 유지 + float-only 해소” 상태다. 다음 단계에서는 두 개의 잔여 hbox warning만
처리하면 된다.

