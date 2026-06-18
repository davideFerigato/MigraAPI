#!/usr/bin/env python3
"""
Test suite for MigraAPI MCP Server.

Tests tools, resources, and prompts using the FastMCP test client.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from mcp_server.server import mcp


@pytest.fixture
async def client():
    """Create a test client for the MCP server."""
    async with mcp.run_test_client() as client:
        yield client


@pytest.mark.asyncio
async def test_tools_list(client):
    """Test that all tools are correctly registered."""
    response = await client.send_request("tools/list", {})
    tools = response.get("tools", [])
    tool_names = [t["name"] for t in tools]
    expected = [
        "scan_file_tool",
        "scan_directory_tool",
        "rewrite_file_tool",
        "validate_file_tool",
        "migrate_codebase_tool"
    ]
    for name in expected:
        assert name in tool_names, f"Tool {name} not found"


@pytest.mark.asyncio
async def test_resources_list(client):
    """Test that resources are correctly registered."""
    response = await client.send_request("resources/list", {})
    resources = response.get("resources", [])
    resource_uris = [r["uri"] for r in resources]
    assert "migration-rules://current" in resource_uris
    assert any("migration-rules://language/" in uri for uri in resource_uris)


@pytest.mark.asyncio
async def test_prompts_list(client):
    """Test that prompts are correctly registered."""
    response = await client.send_request("prompts/list", {})
    prompts = response.get("prompts", [])
    prompt_names = [p["name"] for p in prompts]
    assert "migrate_codebase_prompt" in prompt_names
    assert "resolve_ambiguity_prompt" in prompt_names


@pytest.mark.asyncio
async def test_scan_file_tool(client):
    """Test the scan_file_tool on a real file."""
    # Use an existing file from examples
    test_file = Path(__file__).parent.parent / "examples" / "before" / "sample.py"
    if not test_file.exists():
        pytest.skip(f"Test file not found: {test_file}")

    response = await client.send_request(
        "tools/call",
        {
            "name": "scan_file_tool",
            "arguments": {"file_path": str(test_file)}
        }
    )
    assert response["status"] == "success"
    assert "occurrences" in response


@pytest.mark.asyncio
async def test_scan_file_tool_not_found(client):
    """Test scan_file_tool with a non-existent file."""
    response = await client.send_request(
        "tools/call",
        {
            "name": "scan_file_tool",
            "arguments": {"file_path": "non_existent.py"}
        }
    )
    assert response["status"] == "error"
    assert "File not found" in response.get("error", "")


@pytest.mark.asyncio
async def test_validate_file_tool(client):
    """Test validate_file_tool on a valid file."""
    test_file = Path(__file__).parent.parent / "examples" / "before" / "sample.py"
    if not test_file.exists():
        pytest.skip(f"Test file not found: {test_file}")

    response = await client.send_request(
        "tools/call",
        {
            "name": "validate_file_tool",
            "arguments": {"file_path": str(test_file), "language": "python"}
        }
    )
    # Might fail if Python isn't available, but we check structure
    assert "status" in response
    assert "valid" in response or "error" in response


@pytest.mark.asyncio
async def test_resource_migration_rules(client):
    """Test reading the migration rules resource."""
    response = await client.send_request(
        "resources/read",
        {"uri": "migration-rules://current"}
    )
    assert "contents" in response
    content = response["contents"][0]["text"]
    data = json.loads(content)
    assert "rules" in data
    assert len(data["rules"]) > 0


@pytest.mark.asyncio
async def test_resource_migration_rules_language(client):
    """Test reading language-specific migration rules."""
    for lang in ["python", "javascript"]:
        response = await client.send_request(
            "resources/read",
            {"uri": f"migration-rules://language/{lang}"}
        )
        assert "contents" in response
        content = response["contents"][0]["text"]
        data = json.loads(content)
        assert data.get("language") == lang
        assert "rules" in data


@pytest.mark.asyncio
async def test_prompt_migrate_codebase(client):
    """Test the migrate_codebase_prompt."""
    response = await client.send_request(
        "prompts/get",
        {
            "name": "migrate_codebase_prompt",
            "arguments": {"source_directory": "examples/before"}
        }
    )
    assert "messages" in response
    messages = response["messages"]
    assert len(messages) > 0
    # Check that the prompt contains expected content
    content = messages[0]["content"]["text"]
    assert "Migrate Codebase" in content
    assert "examples/before" in content


@pytest.mark.asyncio
async def test_prompt_resolve_ambiguity(client):
    """Test the resolve_ambiguity_prompt."""
    response = await client.send_request(
        "prompts/get",
        {
            "name": "resolve_ambiguity_prompt",
            "arguments": {"old_pattern": "old_api.get_user", "context": "Python code"}
        }
    )
    assert "messages" in response
    messages = response["messages"]
    assert len(messages) > 0
    content = messages[0]["content"]["text"]
    assert "Resolve Migration Ambiguity" in content
    assert "old_api.get_user" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
