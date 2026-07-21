# 167.5 caption correction changes

167번 감사 이후 리뷰어 관점에서 지적된 3건을 반영한다.
새 실험·새 수치·새 주장 추가는 없으며, 표현 강도와 문서 정합성만 손본다.

## 1. Figure `fig:floor` 캡션 완화 (paper/manuscript_ko.tex line 155)

리뷰어 지적: "이 잔여 성분이 ... DOA bias floor에 해당한다"는 CRLB-UKF gap 전체가 곧 post-gating
coherent multipath DOA bias인 것처럼 등치시켜 읽힐 수 있어 단정적이다.

Before (167번 감사 후 상태):
```
장거리 위치 RMSE와 CRLB 계열 하한의 비교. 600 m 조건에서 routed UKF RMSE와 경험적 CRLB 사이에 수 m 규모의 gap이 남으며, 이 잔여 성분이 본 논문이 다루는 post-gating coherent multipath DOA bias floor에 해당한다. 이 그림은 sub-meter 장거리 성능이 달성됨을 의미하지 않으며, 하한을 완전히 제거한다는 주장의 근거로 사용되지 않는다.
```

After (167.5):
```
장거리 위치 RMSE와 CRLB 계열 하한의 비교. 600 m 조건에서 routed UKF RMSE와 경험적 CRLB 사이에 수 m 규모의 gap이 남는다. 이 gap은 post-gating coherent multipath DOA bias floor가 장거리 오차에 기여함을 시사하며, gap 전체가 이 성분만으로 구성된다는 주장의 근거로는 사용되지 않는다. 그림은 sub-meter 장거리 성능이 달성됨을 의미하지 않으며, 하한을 완전히 제거한다는 주장의 근거로도 사용되지 않는다.
```

핵심 변경:
- "에 해당한다" → "가 장거리 오차에 기여함을 시사한다"로 강도 완화
- gap 구성에 대한 미주장 문장 추가: "gap 전체가 이 성분만으로 구성된다는 주장의 근거로는
  사용되지 않는다"

## 2. `caption_changes.md` (167 폴더) 문서 정합성 - 다음 세션 지시

167번 폴더의 `caption_changes.md` line 157 "새 수치 없음. 캡션에 등장한 수치는 모두 원고 본문에
이미 존재하는 값의 재확인"은 정확히 말하면 캡션에 새로 등장한 문구가 있다: `20개 독립 seed
geometries` (fig:static), `132 paired trials` (fig:quasistatic). 둘 다 61번·82번 원천에는 있으나
본문 그 자리에는 문자 그대로 있지 않다.

권장 표현 (167 폴더 파일은 이번에 수정하지 않고 지침만 남긴다):
```
원고 본문 또는 원천 실험 폴더(61, 63, 82, 45, 58, 138, 145)에 이미 있던 수치만 재확인.
```

이유:
- 167 폴더는 커밋 완료 상태이므로 소급 수정은 이력을 흐리게 만든다.
- 대신 이 폴더(167.5)에 "다음 세션이 새 감사표를 만들 때 어떤 문구를 쓸지"의 지침으로 남긴다.

## 3. `README.md` (167 폴더) "6원칙" 표기 - 다음 세션 지시

167 폴더 `README.md` line 14는 "캡션 6원칙"이지만, `caption_policy.md`에는 7개 항목이 있다.
다음 세션에서 유사 문서를 만들 때는 정책 문서와 요약 문서의 항목 수를 일치시킨다:
```
캡션 7원칙 (stand-alone / 주장+미주장 / post-hoc 명시 / 새 수치 금지 / boundary 초과 금지 /
anti-campaigning / 캡션만 수정 대상)
```

167 폴더는 이력 보존을 위해 수정하지 않는다.

## 검증

- 이번 수정 대상 파일 1개: `paper/manuscript_ko.tex` (fig:floor 캡션만).
- 새 수치·새 주장 0건. 라벨·본문·다른 캡션 변경 0건.
- 정책 위반 없음. Fig. floor의 문구는 오히려 정책 5번(claim boundary 초과 금지)에 더 잘 맞게
  됐다.
- 원천 근거는 45번(routed UKF 600 m 12.29 m vs 경험적 CRLB 11.80 m, 잔여 ≈ 3.45 m)과 정합.
- 167 폴더 파일 자체는 손대지 않는다(이력 보존).
