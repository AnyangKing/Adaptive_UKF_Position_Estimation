# Show-to-professor decision

## Decision

현재 PDF는 교수님께 보여줄 수 있다.

## How to frame it

교수님께 보여줄 때는 “투고 직전 완성본”이 아니라 다음처럼 말하는 것이 적절하다.

> IEEEtran 형식으로 옮긴 현재 논문 초안입니다.  
> 핵심 claim, 선행연구 차별화, Method/Results/Discussion 흐름, 그림/표 배치는 잡혔고,  
> 남은 것은 저자/소속/back matter 확정과 마지막 페이지 압축입니다.

## Strong points to show

1. 연구 라인이 명확하다.
   - TOA/TDOA/DOA-UKF tracking backbone.
   - post-gating coherent multipath DOA bias.
   - carrier-agile whitening.
2. claim boundary가 보수적이다.
   - static 600 m positive.
   - moving RMSE improvement는 미주장.
   - quasi-static continuous boundary는 0.005 m/s로 제한.
3. LaTeX/IEEE 조판이 작동한다.
   - 7 pages.
   - active overfull/underfull/float-only warning 없음.
   - 그림이 결과 근처에 배치됨.

## Weak points to disclose first

1. 저자/소속은 placeholder.
2. back matter는 placeholder.
3. 마지막 7쪽이 비어 보여서 투고 전 6쪽화 또는 Table III 이동이 필요.
4. 실제 수조/호수 실험은 아직 future work.

## Stop condition

사용자가 “보여줄 만하다고 생각되면 목표 멈춰줘”라고 했으므로, 128번 이후 자동 다음 목표로 넘어가지 않는다.

