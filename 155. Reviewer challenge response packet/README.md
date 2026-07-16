# 155. Reviewer challenge response packet

## 목적

현재 원고가 받을 가능성이 높은 심사 질문을 미리 분류하고, 각 질문에 사용할 안전한 답변·근거 폴더·
금지 표현을 연결한다. 이미 닫힌 문제와 실해역 실험 또는 저자 결정 없이는 닫을 수 없는 문제를 구분해
response letter에서 과장하거나 즉흥적으로 답하는 것을 방지한다.

## 실행 검증

```powershell
python "155. Reviewer challenge response packet\validate_packet.py"
```

## 상태

| 상태 | 수 |
|---|---:|
| 현재 증거로 방어 가능 | 6 |
| schedule ablation이 있으면 강화 | 1 |
| 실해역 검증 필요 | 2 |
| 저자 공개정책 결정 필요 | 1 |
| 합계 | 10 |

## 가장 중요한 방어선

1. frequency hopping 자체를 신규 발명이라고 주장하지 않는다.
2. 정지 600 m 개선과 이동 잔차 백색화를 분리한다.
3. moving pooled RMSE 개선은 주장하지 않는다.
4. two-ray 주기는 fitting한 값이 아니라 기하에서 고정한 값이다.
5. 실해역 성능과 transducer calibration은 아직 검증되지 않았다고 명시한다.
6. 30–34 kHz schedule은 frozen validation schedule이며 최적이라고 주장하지 않는다.
