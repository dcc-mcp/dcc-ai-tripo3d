from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


BASE_URL = os.environ.get("TRIPO_BASE_URL", "https://api.tripo3d.ai/v2/openapi")


def request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    api_key = os.environ.get("TRIPO_API_KEY")
    if not api_key:
        raise RuntimeError("TRIPO_API_KEY is not set")
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        urllib.parse.urljoin(BASE_URL.rstrip("/") + "/", path.lstrip("/")),
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "dcc-mcp-tripo3d/0.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Tripo API error {exc.code}: {detail}") from exc


def download(url: str, output_dir: str, name_hint: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    clean = urllib.parse.urlparse(url).path.rsplit("/", 1)[-1] or name_hint
    target = Path(output_dir) / clean
    urllib.request.urlretrieve(url, target)
    return str(target)

