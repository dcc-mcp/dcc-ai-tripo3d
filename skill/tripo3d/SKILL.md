---
name: tripo3d
description: Create, inspect, and download Tripo text/image/multiview 3D generation tasks.
metadata:
  dcc-mcp:
    version: v0.1.0
    dcc: python
    display_name: Tripo3D
    group: asset.ai.generation
    default_icon: cube
    affinity: any
    marketplace: dcc-ai-tripo3d
    tools: tools.yaml
    execution: sync
    permissions:
      - network
    examples:
      - "Create a Tripo text-to-model task"
      - "Create a Tripo image-to-model task from a public image URL"
      - "Download outputs from a finished Tripo task"
    contact:
      name: dcc-mcp team
      url: https://github.com/dcc-mcp/dcc-ai-tripo3d
    install:
      add_source: "dcc-mcp-cli marketplace add dcc-mcp/dcc-ai-tripo3d"
      then_install: "dcc-mcp-cli marketplace install dcc-ai-tripo3d"
---

# Tripo3D

Use this skill for Tripo 3D generation jobs. It submits tasks, reads task
status, and downloads completed model outputs. Local image upload is deliberately
not bundled; pass public image URLs or tokens until upload flows are needed.
