# Supplement v2.1 figure-script delta

152번 dry run의 `figure_scripts/reproduce_tworay_fit.py`는 145번 JSON/SVG evidence를 재생성하지만,
원고용 세로 2패널 PNG 자체는 만들지 않는다.

실제 보충자료 조립 시 다음 두 스크립트를 모두 포함한다.

| archive path | source | 역할 |
|---|---|---|
| `figure_scripts/reproduce_tworay_evidence.py` | `145. Two-ray mechanism evidence closure/reproduce_tworay_fit.py` | claim JSON과 compact SVG 재현 |
| `figure_scripts/generate_tworay_fit_figure.py` | `138. 이론-실측 오버레이 그림/generate_tworay_fit_figure.py` | 원고용 300 dpi PNG 재현 |

따라서 실제 package 후보는 152번의 90개에서 138번 PNG generator 1개를 추가한 **91개**다.
152번 manifest는 당시 dry-run snapshot으로 보존하고, 실제 ZIP 조립 시 이 delta를 적용한다.
