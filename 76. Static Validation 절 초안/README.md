# 76. Static Validation 절 초안

## 목적

61번 정지표적 대규모 독립검증과 70번 Fig.3을 논문 Results/Validation 절 문장으로 정리한다.

## 핵심 메시지

- 가장 강한 성능 결과는 정지/준정지 600 m다.
- fixed 32 kHz 평균 RMSE 13.01 m → frequency-agile 8.87 m.
- 평균 paired improvement +4.14 m, p=0.0008.
- median 13.97 m → 7.96 m.
- 이 결과는 moving target 일반 개선이 아니라 static/quasi-static long-range regime 검증이다.

## 다음 단계

77번은 `Moving Boundary 절 초안`이 자연스럽다. 63번의 lag-1 whitening과 RMSE 미재현, 64~67번 schedule 실패를 한계/경계 절로 묶으면 된다.
