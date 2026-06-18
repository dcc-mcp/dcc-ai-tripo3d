from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_error, skill_exception, skill_success

from _tripo import request


def _image_file(url: str) -> dict[str, str]:
    return {"type": "jpg", "url": url}


@skill_entry
def main(
    task_type: str,
    prompt: str | None = None,
    image_url: str | None = None,
    image_urls: list[str] | None = None,
    model_version: str = "v2.5-20250123",
    texture: bool = True,
    pbr: bool = True,
    face_limit: int | None = None,
    texture_quality: str = "standard",
    geometry_quality: str = "standard",
    smart_low_poly: bool = False,
    quad: bool = False,
    **_: Any,
) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = {
            "type": task_type,
            "model_version": model_version,
            "texture": texture,
            "pbr": pbr,
            "texture_quality": texture_quality,
            "geometry_quality": geometry_quality,
            "smart_low_poly": smart_low_poly,
            "quad": quad,
        }
        if face_limit is not None:
            payload["face_limit"] = face_limit

        if task_type == "text_to_model":
            if not prompt:
                return skill_error("prompt is required", "text_to_model requires prompt")
            payload["prompt"] = prompt
        elif task_type == "image_to_model":
            if not image_url:
                return skill_error("image_url is required", "image_to_model requires a public image URL")
            payload["file"] = _image_file(image_url)
        elif task_type == "multiview_to_model":
            if not image_urls or len(image_urls) < 2:
                return skill_error("image_urls is required", "multiview_to_model requires at least two public image URLs")
            payload["files"] = [_image_file(url) for url in image_urls]
        else:
            return skill_error("Unsupported task_type", task_type)

        response = request("POST", "/task", payload)
        task_id = (response.get("data") or {}).get("task_id")
        return skill_success("Tripo task created", task_id=task_id, response=response)
    except Exception as exc:
        return skill_exception(exc, message="Failed to create Tripo task")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

