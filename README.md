<div align="center">
  <img src="docs/images/logo.png" alt="MigraAPI Logo" width="120" />
  <h1>MigraAPI</h1>
  <p><em>“Claude Agent for Automated API Migration”</em></p>
</div>

<p align="center">
  <!-- Badge principali -->
  <a href="https://github.com/davideFerigato/MigraAPI"><img src="https://img.shields.io/badge/Claude_Skills-5A3E2B?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Skills"/></a>
  <a href="https://github.com/davideFerigato/MigraAPI"><img src="https://img.shields.io/badge/Subagents-7B2D8E?style=flat-square&logo=anthropic" alt="Subagents"/></a>
  <a href="https://github.com/davideFerigato/MigraAPI"><img src="https://img.shields.io/badge/Anthropic-Claude-5A3E2B?logo=anthropic" alt="Anthropic"/></a>
  <a href="https://github.com/davideFerigato/MigraAPI"><img src="https://img.shields.io/badge/Agent_Skills-v1.0-5A3E2B" alt="Agent Skills"/></a>
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/>
  <a href="https://github.com/davideFerigato/MigraAPI/actions/workflows/ci.yml"><img src="https://github.com/davideFerigato/MigraAPI/actions/workflows/ci.yml/badge.svg" alt="CI"/></a>
  <img src="https://img.shields.io/badge/code%20style-ruff-000000.svg" alt="Code style"/>
  <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="Pre-commit"/>
  <img src="https://img.shields.io/badge/Maintenance-yes-green" alt="Maintenance"/>
  <img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196" alt="Conventional Commits"/>
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform"/>
  <img src="https://img.shields.io/badge/GitHub-Pages-blue?logo=githubpages" alt="GitHub Pages"/>
  <a href="https://davideferigato.github.io/MigraAPI"><img src="https://img.shields.io/badge/docs-mcp.md-blue?logo=markdown" alt="MCP Docs"/></a>
  <!-- MCP Advanced Badges -->
  <img src="https://img.shields.io/badge/MCP_Server-v1.0-6C47FF" alt="MCP Server"/>
  <img src="https://img.shields.io/badge/Sampling-Advanced-purple" alt="Sampling"/>
  <img src="https://img.shields.io/badge/Progress_Notifications-Advanced-orange" alt="Progress Notifications"/>
  <img src="https://img.shields.io/badge/Roots-Permission_Model-2ea44f" alt="Roots"/>
  <!-- DOI (sostituisci con il tuo DOI reale) -->
  <a href="https://doi.org/10.5281/zenodo.XXXXXXX"><img src="https://zenodo.org/badge/1269595514.svg" alt="DOI"/></a>
</p>

> **AI agent based on Claude Skills, Subagents, and MCP Server (Anthropic) that automatically migrates code from a deprecated API to a new API.**

---

## Table of Contents

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Progressive Disclosure](#progressive-disclosure)
- [Skills vs CLAUDE.md vs Hooks vs Subagents](#skills-vs-claudemd-vs-hooks-vs-subagents)
- [MCP Server (Model Context Protocol)](#mcp-server-model-context-protocol)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Plugin Distribution](#plugin-distribution)
- [Enterprise Managed Settings](#enterprise-managed-settings)
- [Security Best Practices](#security-best-practices)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)

---

## Introduction

**MigraAPI** is a comprehensive demonstration project that implements **all four Anthropic courses**:

1. ✅ **Introduction to Agent Skills** – SKILL.md, progressive disclosure, hooks, plugin.json
2. ✅ **Introduction to Subagents** – scanner, rewriter, validator with structured JSON & obstacle reporting
3. ✅ **Introduction to MCP** – MCP Server with tools, resources, prompts, STDIO transport
4. ✅ **MCP Advanced Topics** – Sampling, progress notifications, roots, Streamable HTTP transport

It automates the migration of deprecated API calls in Python and JavaScript codebases using an orchestrator agent that delegates tasks to isolated subagents, and exposes all capabilities via the **Model Context Protocol (MCP)**.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Client (any)                            │
│       Claude Desktop / Claude Code / Cursor / VS Code          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ MCP Protocol (STDIO / HTTP)
┌─────────────────────────────────────────────────────────────────┐
│                   MigraAPI MCP Server                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Tools: scan_file, scan_directory, rewrite_file,        │   │
│  │        validate_file, migrate_codebase                  │   │
│  │ Resources: migration-rules://current,                   │   │
│  │           migration-rules://language/{language}         │   │
│  │ Prompts: migrate-codebase, resolve-ambiguity            │   │
│  │ Advanced: Sampling, Progress, Roots                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator (Claude Code)                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │   Scanner    │ │   Rewriter   │ │  Validator   │           │
│  │   Subagent   │ │   Subagent   │ │   Subagent   │           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
│        ↑                  ↑                  ↑                │
│   (parallel on files)   (parallel)        (parallel)           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    File System (read/write)
```

### Components

| Component | Description | Tools |
|-----------|-------------|-------|
| **`api-migration` Skill** | Migration rules, regex patterns, scanner script | Read, Grep, Glob, Bash |
| **`scanner` Subagent** | Scans a file and returns structured JSON with occurrences | Read, Grep, Glob |
| **`rewriter` Subagent** | Applies transformations using mapping rules | Read, Write, Edit |
| **`validator` Subagent** | Verifies syntactic correctness with obstacle reporting | Read, Bash, Grep |
| **MCP Server** | Exposes tools, resources, prompts via MCP protocol | (server-side) |
| **Orchestrator** | Main agent that loads the skill and coordinates subagents | Task tool |

---

## Progressive Disclosure

The skill uses a **3-level progressive disclosure** mechanism to minimize context consumption:

| Level | Description |
|-------|-------------|
| **1. Discovery** | Claude preloads only `name` and `description` in the system prompt |
| **2. Activation** | When the task matches the description, Claude reads the full `SKILL.md` |
| **3. Execution** | If needed, Claude loads additional files (`migration-rules.json`, `regex-patterns.md`) and runs external scripts (`scanner.py`) that do not consume context |

---

## Skills vs CLAUDE.md vs Hooks vs Subagents

| Feature | Purpose | When to use | Example |
|---------|---------|-------------|---------|
| **Skills** | Dynamic, reusable instructions for specialized tasks | Repeated workflows needing specific knowledge | `api-migration` skill with migration rules |
| **CLAUDE.md** | Project-wide always-active configuration | Project settings, style preferences | Ignoring files, env vars |
| **Hooks** | Event-based automations (pre/post) | Triggers like “before every edit, backup” | `pre-edit` hook that backs up files |
| **Subagents** | Task delegation to isolated context windows | Tasks that would blow the main context, parallel execution | Scanner, rewriter, validator |

---

## MCP Server (Model Context Protocol)

MigraAPI includes a complete **MCP Server** that exposes all migration capabilities to any MCP-compatible client.

### Tools

| Tool | Description |
|------|-------------|
| `scan_file_tool` | Scan a single file for deprecated API calls |
| `scan_directory_tool` | Recursively scan a directory |
| `rewrite_file_tool` | Apply migration changes to a file (with dry-run) |
| `validate_file_tool` | Validate a migrated file for syntax correctness |
| `migrate_codebase_tool` | Full pipeline: scan → rewrite → validate |

### Resources

| Resource | Description |
|----------|-------------|
| `migration-rules://current` | Complete migration rules as JSON |
| `migration-rules://language/{language}` | Rules filtered by language |

### Prompts

| Prompt | Description |
|--------|-------------|
| `migrate_codebase_prompt` | Template for migrating an entire codebase |
| `resolve_ambiguity_prompt` | Ask Claude to resolve ambiguous migration patterns |

### Advanced Features (MCP Advanced Topics)

| Feature | Description | File |
|---------|-------------|------|
| **Sampling** | Server asks client (Claude) for completions to resolve ambiguities | `mcp_server/sampling.py` |
| **Progress Notifications** | Real-time progress updates during long operations | `mcp_server/progress.py` |
| **Roots** | Permission model for filesystem access | `mcp_server/roots.py` |

### Running the MCP Server

**Locally (STDIO):**
```bash
python -m mcp_server.server --transport stdio
```

**Remotely (Streamable HTTP):**
```bash
python -m mcp_server.server --transport streamable-http --port 8000
```

### Claude Desktop Integration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "migrapi": {
      "command": "python3",
      "args": ["-m", "mcp_server.server", "--transport", "stdio"],
      "cwd": "/path/to/MigraAPI"
    }
  }
}
```

For detailed MCP documentation, see [`docs/mcp.md`](docs/mcp.md).

---

## Prerequisites

- **Claude Code** (agentic mode enabled) – [installation guide](https://docs.anthropic.com/claude-code)
- **Python 3.9+** (for scanner script and MCP server)
- **Node.js** (for JavaScript examples, optional)
- Unix terminal (macOS/Linux)

---

## Installation

```bash
git clone https://github.com/davideFerigato/MigraAPI
cd MigraAPI
# No external dependencies – all standard
```

### MCP Server Dependencies (optional)

```bash
pip install -r requirements-mcp.txt
```

---

## Usage

### Automated demo script

```bash
./demo-script.sh
```

Runs simulated scanning and produces `migration_report.json`.

### Real usage with Claude Code

```bash
claude
```

Then ask:
```
Migrate the code in examples/before from the old API to the new API using the api-migration skill.
```

Claude will activate the skill, invoke subagents in parallel, and return the result.

### Via MCP Server (Claude Desktop / any MCP client)

1. Start the MCP server:
```bash
python -m mcp_server.server --transport stdio
```

2. Connect from Claude Desktop (configured as above)
3. Use the tools directly:
   - `scan_file_tool("examples/before/sample.py")`
   - `rewrite_file_tool("examples/before/sample.py")`
   - `validate_file_tool("examples/before/sample.py")`

---

## Plugin Distribution

To package MigraAPI as a Claude Code plugin:

1. Structure is already ready:
   ```
   .claude/skills/api-migration/
   .claude/agents/
   ```
2. Add to a marketplace:
   ```bash
   /plugin marketplace add anthropics/skills
   ```
3. Install the plugin:
   ```bash
   /plugin install migrapi@your-org/skills
   ```

See [`plugin.json`](plugin.json) for metadata.

---

## Enterprise Managed Settings

In enterprise environments, skills can be centrally deployed:

- **Managed settings** preinstall skills on all team workstations.
- An admin can enforce the `api-migration` skill on specific repositories.
- Skills auto-update when the central repository changes.

---

## Security Best Practices

- **Always verify skills from external sources** – inspect content, especially scripts.
- **Use `allowed-tools`** – restrict sensitive tools (e.g., `Write`, `Bash`). In this skill, the scanner only has read tools.
- **Never include secrets or API keys** in skill files.
- **Run scripts in sandboxes** (containers or isolated environments) when possible.
- **Audit changes** – use the `validator` subagent to check every modification.

For detailed security policy, see [`SECURITY.md`](SECURITY.md).

---

## Examples

**Before migration** (`examples/before/sample.py`):
```python
from old_api import Client
client = Client(api_key="test")
user = client.get_user(user_id=123)
```

**After migration** (`examples/after/sample.py`):
```python
from new_api import Client
client = Client(api_key="test")
user = client.fetch_user_by_id(user_id=123)
```

Run the test suite:
```bash
python tests/test_migration.py
```

---

## Troubleshooting

### Skill does not activate
- Check `name` and `description` in `SKILL.md` frontmatter.
- Verify the skill is in `.claude/skills/api-migration/`.
- Explicitly ask: “Use the api-migration skill to...”

### Scanner finds no occurrences
- Update patterns in `regex-patterns.md` and the `PATTERNS` dict in `scanner.py`.
- Ensure file extensions are `.py`, `.js`, `.mjs`, `.cjs`.
- Test manually: `python .claude/skills/api-migration/scripts/scanner.py <file>`

### Rewriter errors
- Check file write permissions.
- Ensure `allowed-tools` includes `Write` and `Edit`.
- Refine mappings in `migration-rules.json` (use more specific strings).

### Validation fails
- Inspect the JSON error output for line numbers.
- Manually correct the file or adjust migration rules.
- Add an intermediate validation step in the orchestration.

### MCP Server not starting
- Check Python version: `python --version` (requires 3.9+)
- Install dependencies: `pip install -r requirements-mcp.txt`
- Verify port is available: `netstat -an | grep 8000`

---

## Roadmap

- [x] Claude Skills implementation (progressive disclosure, hooks, plugin.json)
- [x] Subagents with structured JSON and obstacle reporting
- [x] MCP Server with tools, resources, prompts
- [x] MCP Advanced Topics (Sampling, Progress, Roots)
- [x] Streamable HTTP transport for remote deployment
- [x] Full documentation and CI/CD
- [ ] Support more languages (Java, Go, TypeScript)
- [ ] Publish as a plugin on Anthropic marketplace

---

## Acknowledgements

- [Anthropic Claude](https://www.anthropic.com)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [FastMCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Code](https://docs.anthropic.com/claude-code)

---

<div align="center">
  <sub>MigraAPI</sub><br>
</div>
