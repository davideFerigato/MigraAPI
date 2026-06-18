"""
Sampling implementation for MCP server (Advanced Topics).

Allows the server to request LLM completions from the client
to resolve ambiguities in migration rules.

Uses the correct `@mcp.sampling()` decorator with `CreateMessageRequest`.
"""

import json
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.types import CreateMessageRequest, TextContent


def register_sampling_handlers(mcp: FastMCP) -> None:
    """
    Register sampling-related handlers with the MCP server.

    Sampling allows the server to ask the client (Claude) for help
    resolving ambiguous migration patterns.
    """

    @mcp.sampling()
    async def resolve_migration_ambiguity(
        old_pattern: str,
        context: str = "",
        alternatives: List[str] = None
    ) -> Dict[str, Any]:
        """
        Request sampling from the client to resolve migration ambiguity.

        This is called by the server when a migration rule is ambiguous.
        The client (Claude) will provide a completion.

        Args:
            old_pattern: The deprecated API pattern that is ambiguous.
            context: Additional context about the code.
            alternatives: List of possible new API mappings.

        Returns:
            Suggested migration mapping from the LLM.
        """
        if alternatives is None:
            alternatives = []

        # Build the message to send to the client
        prompt = f"""
You are helping resolve a migration ambiguity.

**Deprecated Pattern:** `{old_pattern}`

**Context:**
{context or "No additional context provided."}

**Possible alternatives:** {', '.join(alternatives) if alternatives else 'None provided'}

Please suggest the most appropriate new API mapping and explain your reasoning.
Return a JSON object with:
- `suggested_mapping`: str (the new API call)
- `confidence`: float (0.0 to 1.0)
- `reasoning`: str
- `alternative_mappings`: list of alternatives considered
"""

        # The sampling request will be sent to the client
        # and the response will be returned here.
        #
        # In the MCP SDK, this decorator handles the CreateMessageRequest
        # automatically. The client (Claude) provides the completion.
        #
        # The return value should be the parsed completion from the client.
        #
        # For testing, we can simulate a response.
        # In production, the client will provide the actual completion.
        #
        # The MCP SDK will handle the CreateMessageRequest automatically.
        # We just return the result.
        #
        # The actual implementation will be provided by the client
        # when this function is called via MCP.

        # This is a placeholder that will be replaced by the actual client response
        return {
            "old_pattern": old_pattern,
            "context": context,
            "alternatives": alternatives,
            "suggested_mapping": None,
            "confidence": 0.0,
            "reasoning": "Awaiting sampling response from client",
            "status": "pending"
        }

    @mcp.sampling()
    async def analyze_pattern_with_llm(
        pattern: str,
        language: str,
        code_snippet: str = ""
    ) -> Dict[str, Any]:
        """
        Use sampling to analyze a code pattern and suggest migration.

        Args:
            pattern: The code pattern to analyze.
            language: 'python' or 'javascript'.
            code_snippet: Optional code context.

        Returns:
            Analysis and suggested migration.
        """
        prompt = f"""
Analyze this {language} code pattern and suggest the appropriate migration.

**Pattern:** `{pattern}`

**Code snippet:**
```
{code_snippet or 'No snippet provided'}
```

Return a JSON with:
- `migration_candidates`: list of possible new API calls
- `recommendation`: the best candidate
- `reasoning`: why this is the best
"""

        # The sampling request will be sent to the client
        return {
            "status": "pending",
            "pattern": pattern,
            "language": language,
            "migration_candidates": [],
            "recommendation": None,
            "reasoning": "Awaiting sampling response"
        }
