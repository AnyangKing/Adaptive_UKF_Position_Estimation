# Weak points and gap list

## P0 — two-ray fit 수치의 직접 산출 근거 부족

현재 원고에는 다음 수치가 들어 있다.

- `R^2` up to 0.99
- 400 m: `delta=1.34 ms`, `R^2=0.99`
- 600 m: `delta=1.87 ms`, `R^2=0.75`

하지만 144번 감사에서 numbered folders를 검색한 결과, 이 exact 수치를 산출한 독립 결과 파일 또는 README는 확인되지 않았다.

58번은 기전상 중요한 근거를 제공한다.

- post-gating surface/direct interference
- `bias(f_c) ≈ a + b cos(2π δ f_c) + c sin(2π δ f_c)`
- `cos_fit_r2`
- 30--34 kHz carrier probing

그러나 58번 README의 집계 R²는 원고의 최신 example-geometry R²와 다르다. 따라서 원고의 mechanism figure에 들어간 최신 수치를 그대로 유지하려면 145번에서 재현 산출물을 만들어야 한다.

권장 조치:

1. 400 m와 600 m 대표 기하를 명시적으로 고정한다.
2. direct/surface path delay difference `delta`를 image-source geometry에서 계산한다.
3. 30--34 kHz carrier grid에서 elevation bias curve를 다시 산출한다.
4. two-ray/cosine fit coefficients, `R^2`, `delta_ms`, selected geometry seed를 `results/two_ray_fit.json`에 저장한다.
5. 원고 figure가 이 JSON에서 재생성되도록 script를 남긴다.

## P1 — robustness 결과는 방향성 claim으로만 쓰기

48번 robustness는 거리당 10개 sweep이라 대규모 검증이라기보다 practical sensitivity characterization이다.

현재 원고 표현은 “tolerates ±15 m/s and millisecond-scale clock offsets” 정도라 적절하지만, 너무 강하게 “field-proven” 또는 “guaranteed robust”로 쓰면 안 된다.

안전 문장:

> In the present simulation protocol, performance degraded gracefully under sound-speed mismatch and was comparatively insensitive to millisecond-scale TOA clock offsets.

## P2 — quasi-static 0.100 m/s 양성 결과 해석 주의

82번에서 0.100 m/s도 validated로 나오지만, 0.010과 0.050 m/s가 깨졌기 때문에 속도 단독의 연속 경계로 해석하면 안 된다.

현재 원고가 “continuous support only through 0.005 m/s”라고 제한하고 있어 안전하다. 향후 편집 중 0.100 m/s까지 된다는 식으로 단순화하면 안 된다.

## P3 — moving target claim은 mechanism-only로 유지

63번은 moving target에서 lag-1 residual whitening을 강하게 보여주지만, pooled RMSE gain은 `-0.10 m`, `p=0.301`로 유의하지 않다.

따라서 moving target에 대해 claim할 수 있는 것은 다음뿐이다.

- frequency agility decorrelates/whitens the DOA residual.
- this does not automatically translate to pooled moving-target RMSE improvement.
- motion self-whitening and geometry-dependent tail behavior limit always-on agility.

## P4 — 실험 전 real-water limitation 유지

현재 연구는 시뮬레이션 기반이다. shallow-water channel이 현실성을 높이지만 tank/lake/sea validation은 아직 없다.

논문/보고서의 안전한 framing:

- “simulation evidence”
- “field validation remains future work”
- “practical deployment requires frequency-dependent calibration”

## P5 — Git/문서 규약 유지

반복 확인:

- `paper/`는 local-only/ignored.
- root 보고서/공부 파일은 GitHub에 올리지 않음.
- numbered research folder만 stage/commit/push.
- `git add .` 금지.
