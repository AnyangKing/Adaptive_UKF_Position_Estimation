# Next patch queue

이 파일은 116번에서 당장 고치지는 않았지만, 다음 원고 정리 때 검토할 선택사항이다.

## P1. Title 범위

현재 제목:

> Carrier-Agile Whitening of Coherent Multipath DOA Bias in Static Shallow-Water USBL Tracking

안전하다. 다만 quasi-static 결과도 보조로 들어가므로, 저널/교수님 판단에 따라 아래처럼 넓힐 수 있다.

> Carrier-Agile Whitening of Coherent Multipath DOA Bias in Static and Very-Slow-Drift Shallow-Water USBL Tracking

권고: 지금은 기존 제목 유지. 제목이 길어지고 0.005 m/s 경계 설명 부담이 커진다.

## P2. Abstract novelty 문장

현재 abstract의 novelty 문장은 안전하다.

> The novelty is therefore not frequency hopping itself, but the mechanism, validation, and boundary ...

더 보수적으로 가려면 다음처럼 바꿀 수 있다.

> The contribution is therefore not frequency hopping itself, but a mechanism-level characterization and bounded validation ...

권고: 현재 문장 유지 가능. 리뷰어 공격이 걱정되면 “novelty” 대신 “contribution”으로 바꾼다.

## P3. Data availability

현재 문장:

> will be made available through a public repository, archived release, supplementary material, or author-approved access-on-request route.

아직 정책 미정이라 안전하다. 투고 직전에는 반드시 하나로 고정해야 한다.

권고: 교수님/저널 확정 전까지 그대로 둔다.

## P4. 110번 latexmk 문서와 현재 paper 빌드 상태

110번은 과거 루트 LaTeX + `latexmk` 단일 명령 기준이 남아 있다. 현재는 `paper/` 위치이며 이 PC에서
`latexmk`가 Perl 부재로 실패할 수 있다.

권고: 115번에 이미 현재 재현 명령을 남겼으므로 충분하다. 110번 자체를 수정해 Git에 올릴 필요는 없다.
