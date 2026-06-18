from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _tripo import request


@skill_entry
def main(task_id: str, **_: Any) -> dict[str, Any]:
    try:
        response = request("GET", f"/task/{task_id}")
        status = ((response.get("data") or {}).get("status") if isinstance(response, dict) else None)
        return skill_success("Tripo task fetched", status=status, response=response)
    except Exception as exc:
        return skill_exception(exc, message="Failed to get Tripo task")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

