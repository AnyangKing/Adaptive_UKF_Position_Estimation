# 공부 노트: figure lineage는 hash와 pixel 비교를 함께 써야 한다

같은 그림이라도 PNG metadata, 압축 수준, 라이브러리 버전 때문에 SHA256이 달라질 수 있다. 따라서
figure lineage 감사에서는 두 단계를 구분해야 한다.

1. byte identity: 파일 전체 SHA256이 동일한가.
2. pixel identity: RGBA 픽셀 배열이 동일한가.

byte identity는 배포 파일이 정확히 같은지 보여주고, pixel identity는 metadata만 달라진 경우에도
시각적·수치적 그림이 같은지 확인한다. 또한 그림 파일만 비교하면 생성 경로를 설명할 수 없으므로,
generator와 입력 JSON/CSV의 SHA256도 함께 기록해야 한다.

이번 프로젝트에서는 Fig.1~6이 기존 패키지 PNG와 byte-identical했고, two-ray PNG는 138번 생성기를
임시 출력으로 실행해 원고 파일을 덮어쓰지 않고 재현 여부를 검사한다.
