# 145. Two-ray mechanism evidence closure

## 목적

144번 traceability audit에서 원고의 two-ray mechanism claim이 약한 고리로 확인됐다. 특히 원고에는 다음 수치가 들어가지만, 번호 폴더 안에 이 수치를 직접 가리키는 전용 산출물이 없었다.

- 400 m 대표 기하: `delta=1.34 ms`, `R²=0.99`
- 600 m 대표 기하: `delta=1.87 ms`, `R²=0.75`

이 폴더는 58번 carrier-agility diagnostic의 동일 계산을 대표 기하에 대해 재실행하고, 원고 수치와의 대응을 `results/two_ray_fit.json`으로 명시한다.

## 실행

```powershell
python "145. Two-ray mechanism evidence closure\reproduce_tworay_fit.py"
```

## 산출물

- `results/two_ray_fit.json` — 대표 기하, 환경 파라미터, carrier grid, measured bias, fitted bias, `delta_ms`, `R²`, 원고 rounding 대응
- `results/two_ray_fit.svg` — measured bias-versus-carrier dots와 first-harmonic two-ray fit line

## 현재 판정

실행 결과는 원고 claim과 정상 rounding 수준에서 일치한다.

| case | selected geometry | recomputed delta | recomputed R² | manuscript |
|---|---:|---:|---:|---|
| 400 m | index 1 | 1.337 ms | 0.9947 | 1.34 ms, R² up to 0.99 |
| 600 m | index 5 | 1.875 ms | 0.750 | 1.87 ms, R²=0.75 |

## 원고 반영 권장

원고 claim은 유지 가능하다. 단, 투고 전에는 figure-generation/source-data statement에 이 폴더를 연결하면 좋다.

안전한 caption 문장:

> Representative 400 m and 600 m geometries from the carrier-agility diagnostic yield image-source excess delays of 1.337 ms and 1.875 ms, with first-harmonic two-ray fit statistics of R²=0.995 and R²=0.750, respectively.

논문 본문에는 지금처럼 rounded value를 써도 괜찮다.
