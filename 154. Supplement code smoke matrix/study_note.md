# 공부 노트: manifest 검증과 실행 검증은 다르다

파일의 SHA256이 맞다는 사실은 “논문에 사용한 파일이 바뀌지 않았다”는 뜻이다. 하지만 코드가 현재
환경에서도 실행된다는 뜻은 아니다. 의존성, import 경로, API 변화 때문에 hash가 같은 코드도 실행에
실패할 수 있다.

따라서 재현성 패키지는 두 층으로 검사해야 한다.

1. content integrity: 파일 존재, 크기, SHA256.
2. execution integrity: 독립 프로세스에서 diagnostic test 실행.

154번은 두 번째 층을 담당한다. 전체 Monte Carlo를 매번 재실행하면 비용이 크므로, 핵심 계산과
불변식을 빠르게 확인하는 smoke test를 먼저 사용하고, 최종 release나 major code change에서만 전체
재실행을 수행하는 것이 효율적이다.
