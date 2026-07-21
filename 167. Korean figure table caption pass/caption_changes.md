# Caption changes (before/after)

`paper/manuscript_ko.tex`의 그림/표 캡션 10개에 대한 정확 diff.
정책과 근거는 `caption_policy.md`·`caption_claim_audit_table.md` 참조. 원고 본문·표 body·라벨은
바꾸지 않았다.

## 1. Table `tab:claims` (line 71)

Before:
```
본 논문의 주장 범위와 금지 표현. 한글 원고에서는 이 표를 기준으로 claim boundary를 먼저 잠근 뒤 영어 원고에 반영한다.
```

After:
```
본 논문의 주장 범위와 금지 표현. 표 자체가 claim boundary이며, 원고 본문·그림/표 캡션·초록은 모두 이 표의 부분집합 안에서만 서술한다. 정지/이동/준정지의 경계 구분과 ``frequency hopping USBL 최초'' 표현 금지가 핵심이다.
```

이유: 이 표를 다른 캡션들이 참조할 anchor로 쓰기 위해 "부분집합 원칙"을 캡션에 명문화.

## 2. Figure `fig:system` (line 104)

Before:
```
논문 전체 개념도. 소형 USBL 배열은 TOA/TDOA/DOA를 추출해 UKF에 넣고, 얕은바다 표면반사는 직접파 gate 안에 남아 DOA 편향을 만든다. Carrier-agile pinging은 필터 구조가 아니라 송신 반송파를 바꿔 관측 오차의 시간상관을 낮추는 설계이다.
```

After:
```
시스템 개념도. 8센서 소형 USBL 배열이 TOA/TDOA/DOA를 추출해 conditional adaptive-$R$ UKF로 3차원 위치를 추정하는 기존 파이프라인 위에, 송신 반송파를 ping마다 바꿔 관측 오차의 시간상관을 낮추는 layer가 추가된다. 그림은 방법의 위치를 시각화하기 위한 것이며, 개별 성능 수치의 근거로 사용되지 않는다.
```

이유: 그림이 무엇을 보여주는지 명확히 하고, 개념도가 정량 근거로 오독되지 않게 미주장 문장 추가.

## 3. Figure `fig:floor` (line 155)

Before:
```
소형 배열 장거리 오차 바닥의 요약 그림. 이 결과는 본 연구가 단순히 필터를 더 복잡하게 만드는 방향에서, 관측 오차 구조를 바꾸는 방향으로 이동한 근거이다.
```

After:
```
장거리 위치 RMSE와 CRLB 계열 하한의 비교. 600 m 조건에서 routed UKF RMSE와 경험적 CRLB 사이에 수 m 규모의 gap이 남으며, 이 잔여 성분이 본 논문이 다루는 post-gating coherent multipath DOA bias floor에 해당한다. 이 그림은 sub-meter 장거리 성능이 달성됨을 의미하지 않으며, 하한을 완전히 제거한다는 주장의 근거로 사용되지 않는다.
```

이유: 원본이 자평 문장뿐이고 "무엇을 보여주는지"가 없었다. 45번 원천 결과에 맞춰 그림의 실제 내용을
설명하고, sub-meter/floor 완전제거 미주장 문장 추가.

## 4. Figure `fig:tworay` (line 186)

Before:
```
Two-ray 해석모델과 관측된 elevation bias의 대응. 직접파와 gate 안 표면반사 성분의 상대 위상이 반송파에 따라 달라지며, 이 변화가 DOA 편향 변화를 설명한다.
```

After:
```
Two-ray 해석모델과 관측된 elevation bias의 대응. 반사 지연 $\delta$를 기하에서 계산해 고정한 상태에서 진폭·위상·상수만 fit한 예측 곡선과 측정 편향이 함께 그려진다. 그림은 편향의 반송파 의존이 gate 내 두 성분 간섭이라는 해석과 정합함을 보이지만, two-ray 모델은 단순화된 근사이며 실제 얕은바다 채널의 모든 편향을 대체한다고 주장하지 않는다.
```

이유: "설명한다"는 단정을 "정합함을 보인다"로 완화, delta-fixed prediction임을 캡션에서 명시,
모델의 근사 성격 미주장.

## 5. Figure `fig:bias` (line 193)

Before:
```
반송파 변화에 따른 장거리 DOA bias 민감도. 이 그림은 carrier agility가 임의의 heuristic이 아니라, carrier-locked coherent bias를 건드리는 설계변수임을 보여준다.
```

After:
```
반송파 변화에 따른 장거리 elevation bias 민감도(58번 실험 기반). 동일 기하에서 반송파를 30--34 kHz 범위로 미세하게 바꾸면 관측되는 DOA 편향이 함께 변한다. 이 그림은 편향이 반송파-locked coherent 성분을 포함함을 보이는 근거이며, 반송파를 바꾸는 것만으로 위치 RMSE가 개선된다는 주장의 직접 근거로 사용되지 않는다(위치 성능 근거는 Fig.~\ref{fig:static}).
```

이유: 자평("임의 heuristic이 아니라 설계변수") 대신 데이터 조건을 서술하고, 위치 RMSE 근거가
아님을 명시해 mechanism/performance 근거 혼동을 차단.

## 6. Table `tab:validation` (line 216)

Before:
```
핵심 검증 결과 요약. 이 표는 영어 원고의 Results section으로 옮길 때 중심 표 역할을 한다.
```

After:
```
핵심 검증 결과 요약. 정지·이동·준정지·CRLB 계열 결과가 서로 다른 지위(중심 성능 근거, 기전 evidence·성능 미주장, 제한된 안전선, 하한 존재의 증거)로 배치된다. 표의 어떤 행도 다른 행의 지위로 확장되어 해석되지 않는다.
```

이유: "중심 표 역할" 자평 대신 각 행의 지위 차이를 캡션에서 잠금. 이동 행이 성능 근거로 읽히는
위험 차단.

## 7. Figure `fig:static` (line 239)

Before:
```
정지 600 m 독립 검증. Fixed 32 kHz 대비 carrier-agile schedule의 settled RMSE가 유의하게 낮아졌으며, 이 결과가 본 논문의 중심 성능 근거이다.
```

After:
```
정지 600 m 독립 검증(61번). 20개 독립 seed geometries에서 fixed 32 kHz와 동결된 carrier-agile schedule을 paired 비교한 결과, settled RMSE 평균이 13.01 m에서 8.87 m로 감소했다(paired improvement 4.14 m, $p=0.0008$). 이 결과는 본 논문의 중심 성능 근거이지만, 정지 600 m 조건에 한정되며 다른 거리·이동 표적·real-water 조건으로 이 개선이 그대로 이전된다고 주장하지 않는다.
```

이유: 자평 유지하되(정당함), 조건 한정 미주장 문장 추가. 수치는 본문에 이미 있는 것만 재확인.

## 8. Figure `fig:moving` (line 263)

Before:
```
이동 표적에서의 residual whitening과 성능 경계. Carrier agility는 DOA residual의 시간상관을 낮췄지만, pooled RMSE 개선으로 이어진다는 주장은 재현되지 않았다.
```

After:
```
이동 표적에서의 residual whitening과 성능 경계(63번). Carrier agility가 DOA elevation residual의 lag-1 자기상관을 fixed 조건 대비 크게 낮췄다(전형값 $+0.470 \rightarrow -0.208$). 이 그림은 mechanism evidence로만 사용되며, 이동 표적에서의 pooled RMSE 개선 근거로 사용되지 않는다. 실제로 이동 pooled RMSE gain은 재현되지 않았고, 이는 본문에서 성능 개선이 아닌 적용 경계로 서술된다.
```

이유: 이미 잘 되어 있었으나 "mechanism evidence로만 사용된다"를 명시적으로 못박아 지위 오독 차단.

## 9. Figure `fig:quasistatic` (line 277)

Before:
```
준정지 속도 경계. 전체 평균 개선과 whitening은 재확인되지만, 속도별 결과가 비단조이므로 continuous quasi-static claim은 0.005 m/s까지로 제한한다.
```

After:
```
준정지 속도 경계(82번, 132 paired trials). 600 m 조건 전체 평균에서는 fixed 11.98 m가 agile 10.49 m로 개선되고 residual whitening도 재확인되지만, 속도별로는 결과가 단조롭지 않다. 0.010/0.050 m/s는 개선을 보이지 않고, 0.030/0.100 m/s의 양성 결과도 속도 단조 효과가 아니라 기하와 tail 조건에 의존하는 회복으로 해석된다. 이 그림은 연속적인 quasi-static 안전선을 0.005 m/s까지로 제한하는 근거이며, 이보다 빠른 속도로 일반적 개선을 확장하지 않는다.
```

이유: 원본이 이미 좋았으나 82번 원천의 정확 수치와 비단조 해석을 캡션에서도 볼 수 있게 확장.
0.100 m/s를 "validated"로 오독하는 위험 원천 차단.

## 10. Table `tab:limitations` (line 310)

Before:
```
실패와 한계 결과의 논문 내 배치. 실패 실험을 숨기지 않되, 검증 수준에 맞게 본문 claim과 분리한다.
```

After:
```
실패·한계 실험 결과의 논문 내 배치. 이 표의 어떤 행도 본문 성능 claim의 근거가 되지 않는다. 특히 160번 four-carrier schedule과 162번 transition TOA guard는 각각 독립검증 실패와 post-hoc pilot 상태이므로, 본문 성능 claim에 사용하는 것을 금지한다.
```

이유: 160/162 지위를 캡션에서 재확인. 이 표를 근거로 성능을 낚아채는 서술이 없도록 원천 차단.

## 검증

- 정책 6개 항목 (stand-alone / 주장+미주장 / post-hoc 명시 / 새 수치 금지 / 초과 금지 /
  anti-campaigning): 10개 캡션 모두 만족.
- 원본 대비 수치는 본문에 이미 있는 값만 재확인 (13.01, 8.87, 4.14, $p=0.0008$, $+0.470/-0.208$,
  $0.005$~m/s, $11.98/10.49$). 새 수치 없음.
- 라벨 변경 없음.
- 본문·수식·표 body 변경 없음.
