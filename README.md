# DCC-MCP Tripo3D

<p align="center">
  <img src="docs/assets/dcc-ai-tripo3d.svg" alt="DCC-MCP · TRIPO3D" width="600">
</p>

## Agent workflow

AI agents should use installed package skills through the shared gateway. IDE
users may continue to use the MCP endpoint.

```bash
dcc-mcp-cli dcc-types
dcc-mcp-cli list
dcc-mcp-cli search --query "<task>" --dcc-type <host>
dcc-mcp-cli describe <tool-slug>
dcc-mcp-cli call <tool-slug> --json '{"key":"value"}'
```

If the package skill is not active, call
`dcc-mcp-cli load-skill <skill-name> --dcc-type <host>`. After the task,
query `dcc-mcp-cli stats --range 24h --session-id <task-id>` and pass only
bounded evidence to the `review_skill_improvement` prompt from
`dcc-mcp-skills-creator`.


![Workflow showcase](docs/images/dcc-ai-tripo3d-showcase.webp)

Tripo 3D generation tools for DCC-MCP.

The scripts call the Tripo OpenAPI directly with Python stdlib. Set
`TRIPO_API_KEY` in the runtime environment before submitting jobs.

## Install

```bash
dcc-mcp-cli marketplace add dcc-mcp/dcc-ai-tripo3d
dcc-mcp-cli marketplace install dcc-ai-tripo3d
```

## Tools

- `create_tripo3d_task`
- `get_tripo3d_task`
- `download_tripo3d_task`
