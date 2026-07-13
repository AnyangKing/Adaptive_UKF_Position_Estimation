# Measurement log template

현장 실험 시 각 block마다 아래 항목을 기록한다. 이 기록이 없으면 fixed/hop 차이를 논문 방어용으로 쓰기 어렵다.

## Session metadata

| 항목 | 기록 |
|---|---|
| 날짜/시간 |  |
| 장소 |  |
| 담당자 |  |
| 실험 tier | Tier 1 / Tier 2 / Tier 3 |
| 수심 |  |
| 수신기 깊이 |  |
| 송신기 깊이 |  |
| 목표 거리 |  |
| ground-truth 방법 | RTK-GPS / depth sensor / mooring geometry / 기타 |
| 수온/음속 |  |
| 표면 상태 | calm / small waves / rough |
| 주변 소음 | vessel / wind / biological / unknown |

## Hardware

| 항목 | 기록 |
|---|---|
| 8센서 배열 ID/배치 |  |
| hydrophone calibration 상태 |  |
| 송신기 모델 |  |
| 수신기/DAQ sample rate |  |
| clock sync 방식 |  |
| 송신 음압/출력 설정 |  |
| LFM bandwidth/duration |  |

## Block log

| block ID | mode | carrier schedule | start time | pings | target state | distance | notes |
|---|---|---|---|---:|---|---:|---|
| B001 | fixed | 32 kHz |  |  | static / drift |  |  |
| B002 | hop | 30–34 kHz linear |  |  | static / drift |  |  |

권장 block 순서:

- ABBA: fixed → hop → hop → fixed
- 또는 randomized fixed/hop blocks

## Analysis fields

각 block 처리 후 아래 값을 저장한다.

| 항목 | 값 |
|---|---|
| TOA valid fraction |  |
| TDOA valid fraction |  |
| DOA valid fraction |  |
| mean RMSE |  |
| median RMSE |  |
| P90 RMSE |  |
| DOA elevation residual lag-1 |  |
| matched-filter SNR |  |
| direct gate late-energy ratio |  |
| gross-error count |  |

## Notes

- 표적이 흔들렸으면 반드시 기록한다.
- fixed/hop 사이에 표면 상태나 배 위치가 달라졌으면 paired 비교에서 제외할 수 있다.
- carrier별 송신 출력이 다르면 whitening 효과와 SNR 효과가 섞이므로 출력 보정 기록이 필요하다.
