from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "tripo3d"
SCRIPTS = SKILL / "scripts"


def load(name: str):
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def validate_skill() -> None:
    from dcc_mcp_core import validate_skill

    report = validate_skill(str(SKILL))
    assert not report.has_errors, report


def create_payload_contract() -> None:
    mod = load("create_tripo3d_task")
    captured = {}

    def fake_request(method, path, payload):
        captured.update(method=method, path=path, payload=payload)
        return {"data": {"task_id": "task_test"}}

    mod.request = fake_request
    result = mod.main(task_type="text_to_model", prompt="a small wooden chair")
    assert result["success"], result
    assert result["context"]["task_id"] == "task_test"
    assert captured["method"] == "POST"
    assert captured["path"] == "/task"
    assert captured["payload"]["type"] == "text_to_model"
    assert captured["payload"]["prompt"] == "a small wooden chair"


def missing_key_contract() -> None:
    old = os.environ.pop("TRIPO_API_KEY", None)
    try:
        result = load("get_tripo3d_task").main(task_id="task_test")
        assert not result["success"], result
        assert result["context"]["error_type"] == "RuntimeError", result
        if result["error"] == "RuntimeError":
            assert result["_meta"]["dcc.error"]["type"] == "RuntimeError", result
            assert result["_meta"]["dcc.error"]["message"] == "TRIPO_API_KEY is not set", result
        else:
            # Older Core exposes the exception repr instead of canonical error metadata.
            assert result["error"] == "RuntimeError('TRIPO_API_KEY is not set')", result
    finally:
        if old:
            os.environ["TRIPO_API_KEY"] = old


def live_balance_smoke() -> None:
    if os.environ.get("RUN_LIVE_API_SMOKE") != "true":
        print("skip live Tripo API smoke")
        return
    if not os.environ.get("TRIPO_API_KEY"):
        print("skip live Tripo API smoke: TRIPO_API_KEY is not set")
        return
    tripo = load("_tripo")
    response = tripo.request("GET", "/user/balance")
    assert "data" in response, response


def main() -> None:
    validate_skill()
    create_payload_contract()
    missing_key_contract()
    live_balance_smoke()


if __name__ == "__main__":
    main()

