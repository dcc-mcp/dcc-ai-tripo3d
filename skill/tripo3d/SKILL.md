---
name: tripo3d
description: Create, inspect, and download Tripo text/image/multiview 3D generation tasks.
license: MIT
compatibility: "dcc-mcp-core 0.18+"
metadata:
  dcc-mcp:
    version: v0.1.0
    dcc: python
    layer: domain
    tags:
      - ai
      - tripo
      - tripo3d
      - 3d-generation
      - text-to-3d
      - image-to-3d
    search-hint: "tripo, tripo3d, text to model, image to model, multiview to model, 3d generation, download generated model"
    tools: tools.yaml
---

# Tripo3D

Use this skill for Tripo 3D generation jobs. It submits tasks, reads task
status, and downloads completed model outputs. Local image upload is deliberately
not bundled; pass public image URLs or tokens until upload flows are needed.
