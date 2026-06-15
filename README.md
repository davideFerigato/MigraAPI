# 🐝 MigraAPI – Claude Agent for Automated API Migration

![Claude Skills](https://img.shields.io/badge/Claude_Skills-5A3E2B?style=flat-square&logo=anthropic&logoColor=white)
![Subagents](https://img.shields.io/badge/Subagents-7B2D8E?style=flat-square&logo=anthropic)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintenance](https://img.shields.io/badge/Maintenance-yes-green)
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196)
![Code style](https://img.shields.io/badge/code%20style-ruff-000000.svg)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-5A3E2B?logo=anthropic)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-v1.0-5A3E2B)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)

> AI agent based on **Claude Skills** and **Subagents** (Anthropic) that automatically migrates code from a deprecated API to a new API.

## Table of Contents
- [Introduction](#introduction)
- [Architecture](#architecture)
- [Progressive Disclosure](#progressive-disclosure)
- [Skills vs CLAUDE.md vs Hooks vs Subagents](#skills-vs-claudemd-vs-hooks-vs-subagents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Plugin Distribution](#plugin-distribution)
- [Enterprise Managed Settings](#enterprise-managed-settings)
- [Security Best Practices](#security-best-practices)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)

## Introduction

MigraAPI is a demonstrative project implementing advanced **Agent Skills** and **Subagents** concepts from Anthropic's official courses. It automates the migration of deprecated API calls in Python and JavaScript codebases using an orchestrator agent that delegates tasks to isolated subagents.

## Architecture

The system follows the **orchestrator pattern**:

```
User → Orchestrator (Claude Code) → Subagent scanner → Subagent rewriter → Subagent validator
                                        ↑                    ↑                    ↑
                                   (parallel files)     (parallel)           (parallel)
```

### Components

1. **`api-migration` Skill**  
   - Contains migration rules (old→new mapping), regex patterns, and a scanner script.  
   - Follows **progressive disclosure** (see below).

2. **`scanner` Subagent**  
   - Isolated, scans a file and returns structured JSON with occurrences.  
   - Allowed tools: `Read`, `Grep`, `Glob`.

3. **`rewriter` Subagent**  
   - Applies transformations using mapping rules.  
   - Allowed tools: `Read`, `Write`, `Edit`.

4. **`validator` Subagent**  
   - Verifies syntactic correctness (and optionally runs tests).  
   - Returns JSON with results and obstacle reporting.

5. **Orchestrator**  
   - Main agent (Claude Code) loads the skill and coordinates subagents.  
   - Can run subagents **in parallel** on multiple files.

## Progressive Disclosure

| Level | Description |
|-------|-------------|
| **1. Discovery** | Claude preloads only `name` and `description` in the system prompt – minimal context. |
| **2. Activation** | When the task matches the description, Claude reads the full `SKILL.md`. |
| **3. Execution** | If needed, Claude loads additional files (`migration-rules.json`, `regex-patterns.md`) and runs external scripts (`scanner.py`) that do not consume context. |

## Skills vs CLAUDE.md vs Hooks vs Subagents

| Feature | Purpose | When to use | Example |
|---------|---------|-------------|---------|
| **Skills** | Dynamic, reusable instructions for specialized tasks | Repeated workflows needing specific knowledge | `api-migration` skill |
| **CLAUDE.md** | Project-wide always-active configuration | Project settings, style preferences | Ignoring files, env vars |
| **Hooks** | Event-based automations (pre/post) | Triggers like “before every edit, backup” | `pre-edit` hook |
| **Subagents** | Task delegation to isolated context windows | Tasks that would blow the main context, parallel execution | Scanner, rewriter, validator |

## Prerequisites

- **Claude Code** (agentic mode enabled) – [installation guide](https://docs.anthropic.com/claude-code)
- **Python 3.9+** (for scanner script, optional)
- **Node.js** (for JavaScript examples, optional)
- Unix terminal (macOS/Linux)

## Installation

```bash
git clone https://github.com/davideFerigato/MigraAPI
cd MigraAPI
# No external dependencies – all standard
```

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

## Enterprise Managed Settings

In enterprise environments, skills can be centrally deployed:

- **Managed settings** preinstall skills on all team workstations.
- An admin can enforce the `api-migration` skill on specific repositories.
- Skills auto-update when the central repository changes.

## Security Best Practices

- **Always verify skills from external sources** – inspect content, especially scripts.
- **Use `allowed-tools`** – restrict sensitive tools (e.g., `Write`, `Bash`). In this skill, the scanner only has read tools.
- **Never include secrets or API keys** in skill files.
- **Run scripts in sandboxes** (containers or isolated environments) when possible.
- **Audit changes** – use the `validator` subagent to check every modification.

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

## Roadmap

- [ ] Full integration with Claude Code (not just simulation).
- [ ] Support more languages (Java, Go, TypeScript).
- [ ] Publish as a plugin on Anthropic marketplace.

