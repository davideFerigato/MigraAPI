# MCP Server Documentation

MigraAPI includes a complete **Model Context Protocol (MCP)** server that exposes its migration capabilities to any MCP-compatible client (Claude Desktop, Claude Code, Cursor, VS Code, etc.).

## Overview

The MCP server transforms MigraAPI from a Claude Code-only tool into a **standalone service** that can be consumed by any MCP client. This enables:

- **Claude Desktop** integration – use the migration tools directly from Claude Desktop
- **Remote deployment** – deploy the server as a microservice accessible to a team
- **Tool interoperability** – use the same migration capabilities across different IDEs

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  MCP Client (any)                          │
│         Claude Desktop / Claude Code / Cursor              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼ MCP Protocol
┌─────────────────────────────────────────────────────────────┐
│                 MigraAPI MCP Server                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Tools (5)                                          │   │
│  │  - scan_file_tool                                  │   │
│  │  - scan_directory_tool                             │   │
│  │  - rewrite_file_tool                               │   │
│  │  - validate_file_tool                              │   │
│  │  - migrate_codebase_tool                           │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Resources (2)                                      │   │
│  │  - migration-rules://current                       │   │
│  │  - migration-rules://language/{language}           │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Prompts (2)                                        │   │
│  │  - migrate_codebase_prompt                         │   │
│  │  - resolve_ambiguity_prompt                        │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Advanced Features (Corso 2)                        │   │
│  │  - Sampling (server asks client for completions)   │   │
│  │  - Progress notifications (real-time UX)           │   │
│  │  - Roots (permission model for filesystem)         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    File System (read/write)
```

## Tools

### 1. `scan_file_tool`

Scan a single file for deprecated API calls.

**Input**:
```json
{
  "file_path": "examples/before/sample.py"
}
```

**Output**:
```json
{
  "status": "success",
  "file": "examples/before/sample.py",
  "occurrences": [
    {"line": 2, "code": "from old_api import Client", "pattern": "import old_api"}
  ]
}
```

### 2. `scan_directory_tool`

Recursively scan a directory for deprecated API calls.

**Input**:
```json
{
  "directory_path": "examples/before"
}
```

**Output**:
```json
{
  "status": "success",
  "directory": "examples/before",
  "files": [{"path": "...", "occurrences": [...]}]
}
```

### 3. `rewrite_file_tool`

Apply migration changes to a file.

**Input**:
```json
{
  "file_path": "examples/before/sample.py",
  "dry_run": false
}
```

**Output**:
```json
{
  "status": "success",
  "file": "examples/before/sample.py",
  "changes_made": 2,
  "changes": [{"old": "old_api.get_user", "new": "new_api.fetch_user_by_id", "replaced": 1}]
}
```

### 4. `validate_file_tool`

Validate a migrated file for syntax correctness.

**Input**:
```json
{
  "file_path": "examples/before/sample.py",
  "language": "python"
}
```

**Output**:
```json
{
  "status": "success",
  "file": "examples/before/sample.py",
  "valid": true,
  "checks_passed": ["syntax"]
}
```

### 5. `migrate_codebase_tool`

Full migration pipeline: scan → rewrite → validate.

**Input**:
```json
{
  "source_directory": "examples/before",
  "dry_run": false
}
```

**Output**:
```json
{
  "status": "success",
  "directory": "examples/before",
  "files_scanned": 5,
  "files_modified": 4,
  "changes_made": 12,
  "errors": []
}
```

## Resources

### `migration-rules://current`
Returns the complete migration rules as JSON.

### `migration-rules://language/{language}`
Returns rules filtered by language (`python` or `javascript`).

## Prompts

### `migrate_codebase_prompt`
A template for asking Claude to migrate an entire codebase. Includes all instructions, rules summary, and output format.

### `resolve_ambiguity_prompt`
Used by sampling to resolve ambiguous migration patterns.

## Advanced Features (Corso 2)

### Sampling
The server can ask the client (Claude) for completions to resolve ambiguities. See `mcp_server/sampling.py`.

### Progress Notifications
Long operations report progress in real-time. See `mcp_server/progress.py`.

### Roots
Permission model for filesystem access. The server can only access directories the client authorizes. See `mcp_server/roots.py`.

## Running the Server

### Locally (STDIO)
```bash
python -m mcp_server.server --transport stdio
```

### Remotely (Streamable HTTP)
```bash
python -m mcp_server.server --transport streamable-http --port 8000
```

## Claude Desktop Integration

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

## Debugging with MCP Inspector

1. Start the server:
```bash
python -m mcp_server.server --transport streamable-http --port 8000
```

2. Open the Inspector:
```bash
npx -y @modelcontextprotocol/inspector
```

3. Connect to `http://localhost:8000/mcp`

## Testing

Run the MCP server tests:
```bash
python tests/test_mcp_server.py
```

## References

- [MCP Documentation](https://modelcontextprotocol.io)
- [FastMCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop MCP Integration](https://docs.anthropic.com/claude-desktop/mcp)
