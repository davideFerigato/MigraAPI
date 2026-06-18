"""
Roots implementation for MCP server (Advanced Topics).

Roots define the permission model for filesystem access.
Clients can list which directories the server is allowed to access.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.types import Root, Roots


def register_roots_handlers(mcp: FastMCP) -> None:
    """
    Register roots-related handlers with the MCP server.

    Roots are the recommended way for MCP clients to authorize
    filesystem access. The server can only access directories
    that the client has explicitly listed as roots.
    """

    @mcp.roots()
    async def get_allowed_roots() -> List[Root]:
        """
        Return the allowed roots for this server.

        This is the list of directories the client authorizes the server to access.
        """
        # In a real implementation, these would come from the client
        # via the roots/list request. For demonstration, we return
        # a default set of allowed directories.
        return [
            Root(
                name="project-root",
                uri="file:///Users/davideferigato/Documents/GitHub/MigraAPI",
                description="The MigraAPI project root directory"
            ),
            Root(
                name="examples",
                uri="file:///Users/davideferigato/Documents/GitHub/MigraAPI/examples",
                description="Example code directories (before/after)"
            ),
            Root(
                name="migration-scripts",
                uri="file:///Users/davideferigato/Documents/GitHub/MigraAPI/.claude/skills/api-migration/scripts",
                description="Scanner and migration scripts"
            )
        ]

    @mcp.roots()
    async def check_access(path: str) -> Dict[str, bool]:
        """
        Check if a given path is allowed by the roots.

        Args:
            path: The file path to check.

        Returns:
            Dict with 'allowed' boolean and 'reason' if not allowed.
        """
        from pathlib import Path
        from urllib.parse import urlparse

        # Parse the path
        target = Path(path).resolve()

        # Get allowed roots
        roots = await get_allowed_roots()

        for root in roots:
            # Extract the filesystem path from the URI
            uri = root.uri
            if uri.startswith("file://"):
                root_path = Path(urlparse(uri).path)
                try:
                    # Check if target is within root_path
                    target.relative_to(root_path)
                    return {"allowed": True, "reason": f"Path is within root: {root.name}"}
                except ValueError:
                    continue

        return {
            "allowed": False,
            "reason": f"Path {path} is not within any allowed root. Please add a root for this directory."
        }

    @mcp.roots()
    async def list_allowed_files(directory: str) -> Dict[str, Any]:
        """
        List files in a directory that are allowed by roots.

        Args:
            directory: The directory to list.

        Returns:
            List of allowed files with their metadata.
        """
        from pathlib import Path

        path = Path(directory)
        if not path.exists():
            return {"error": f"Directory not found: {directory}", "files": []}

        # Check access
        access = await check_access(str(path))
        if not access.get("allowed", False):
            return {
                "error": f"Access denied: {access.get('reason')}",
                "files": []
            }

        # List files
        files = []
        for ext in [".py", ".js", ".mjs", ".cjs"]:
            for f in path.rglob(f"*{ext}"):
                files.append({
                    "path": str(f),
                    "name": f.name,
                    "extension": f.suffix,
                    "size": f.stat().st_size
                })

        return {
            "directory": str(path),
            "files": files,
            "count": len(files)
        }
