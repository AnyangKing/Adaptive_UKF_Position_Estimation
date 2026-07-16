# 공부 노트: 주파수 도약은 DOA만 바꾸지 않는다

처음의 기전은 carrier phase가 게이트 안 표면반사와 직접파의 코히어런트 DOA 편향을 바꾸고,
여러 carrier 평균이 이를 상쇄한다는 것이었다. 161번은 같은 carrier 변화가 matched-filter TOA의
우세 peak/path branch도 바꿀 수 있음을 보여줬다.

중요한 차이는 span과 total variation이다. linear sweep과 four-carrier cycle은 모두 geometry 2에서
3.557 m의 TOA branch 차이를 경험했다. 하지만 linear는 경계를 한 번만 넘었고, cycle은 아홉 번
왕복했다. 결과적으로 total variation은 3.558 m와 32.013 m로 갈렸고, 후자만 53 m tail을 만들었다.

따라서 schedule은 carrier 집합의 폭만으로 설계할 수 없다. carrier 순서가 DOA residual correlation뿐
아니라 TOA branch boundary 재방문 횟수까지 결정한다. 다음 필터는 carrier transition과 TOA innovation을
공동으로 보고 반복적인 range update만 격리해야 한다.
