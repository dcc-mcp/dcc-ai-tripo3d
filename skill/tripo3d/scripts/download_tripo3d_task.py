from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_error, skill_exception, skill_success

from _tripo import download, request


@skill_entry
def main(
    task_id: str,
    output_dir: str,
    fields: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        response = request("GET", f"/task/{task_id}")
        data = response.get("data") or {}
        if data.get("status") != "success":
            return skill_error("Tripo task is not complete", str(data.get("status")), response=response)

        output = data.get("output") or {}
        wanted = set(fields or [])
        urls = [
            (name, value)
            for name, value in output.items()
            if isinstance(value, str)
            and value.startswith(("http://", "https://"))
            and (not wanted or name in wanted)
        ]
        if not urls:
            return skill_error("No downloadable output URLs found", "empty output", response=response)

        files = [download(url, output_dir, f"{task_id}_{name}") for name, url in urls]
        return skill_success("Tripo outputs downloaded", files=files, response=response)
    except Exception as exc:
        return skill_exception(exc, message="Failed to download Tripo task outputs")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

