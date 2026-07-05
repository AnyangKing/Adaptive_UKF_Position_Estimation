"""진단 B·C 러너: run_bias.py가 저장한 bias_raw.json을 읽어 편향의 결정론성(B)과
blind 식별성(C)을 계산한다. 무거운 신호 재합성 없이 편향 원자료만 재사용한다.
"""

from pathlib import Path
import json

from identifiability import diagnose_B, diagnose_C


def run():
    root = Path(__file__).resolve().parent / "results"
    raw = json.loads((root / "bias_raw.json").read_text(encoding="utf-8"))
    validation = raw["raw"]["validation"]
    test = raw["raw"]["test"]

    payload = {
        "note": "B=참기하 oracle 상한, C=blind 관측 feature. residual_reduction>0이면 편향 설명력 존재",
        "B_geometry_oracle": diagnose_B(validation, test),
        "C_blind_signal": diagnose_C(validation, test),
    }
    (root / "identifiability.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
