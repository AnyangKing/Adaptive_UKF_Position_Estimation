# 결과 metadata 표준

## 목적

다음 numbered 실험부터 결과 JSON이 단순 수치 저장이 아니라 claim 방어용 provenance가 되도록 표준 key를 둔다.

## 권장 `config` schema

```json
{
  "stage": "development | validation | independent_validation | post_hoc_diagnostic | pilot",
  "protocol_frozen_before_execution": true,
  "automatic_manuscript_update_allowed": false,
  "distance_m": 600.0,
  "distances_m": [100, 200, 400, 600],
  "steps": 20,
  "settle_start": 10,
  "trajectory_count": 20,
  "motion_conditions": [],
  "seed_roots": {
    "geometry": 0,
    "ping": 0,
    "channel": 0,
    "bootstrap": 0
  },
  "common_random_ping_seeds": true,
  "usbl_protocol": {
    "source_type": "one_way_synchronized_beacon",
    "toa_mode": "one_way_absolute_toa",
    "common_clock_bias_model": "not_included_in_canonical_validation",
    "per_sensor_hardware_delay_model": "not_included_in_canonical_validation"
  },
  "array": {
    "sensor_count": 8,
    "ring_radius_m": 0.033,
    "vertical_spacing_m": 0.079
  },
  "signal": {
    "sample_rate_hz": 192000,
    "carrier_hz_or_schedule_hz": [],
    "chirp_bandwidth_hz": 12000,
    "pulse_duration_s": 0.010,
    "direct_path_gate_s": 0.005
  },
  "channel": {
    "sound_speed_m_s": 1500,
    "water_depth_m": 100,
    "receiver_depth_m": 30,
    "paths": ["direct", "surface", "bottom"],
    "snr_db_values": [10, 20, 30]
  },
  "truth_usage": "truth is not used for measurement extraction or adaptive decisions",
  "claim_allowed": "exact allowed claim",
  "claim_forbidden": "exact forbidden claim"
}
```

## 필수 summary metric

- mean RMSE
- median RMSE
- P90 또는 tail metric
- divergence rate 또는 div50 rate
- paired gain
- bootstrap confidence interval
- paired test p-value
- improved fraction
- condition별 breakdown

## 현재 결과에 대한 gap

| 결과 | 상태 | gap |
|---|---|---|
| 61 static hop | 핵심 수치/CI/p-value 있음 | seed roots, P90, truth_usage가 JSON config에 명시적으로 부족 |
| 63 moving hop | 2026-08-11 복구 및 metadata 일부 보강 | P90/divergence는 없음. mechanism용 결과이므로 성능 claim에는 사용 금지 |
| 82 quasi-static | seed roots, P90, divergence 포함 | usbl_protocol/truth_usage key는 다음 재실행 때 보강 권장 |
| 160 four-carrier | independent validation metadata 우수 | 실패 결과 유지 |
| 162 TOA guard pilot | pilot/claim 금지 metadata 우수 | 독립검증 전 성능 claim 금지 |

