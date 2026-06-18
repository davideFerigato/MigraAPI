"""
Progress notifications for MCP server (Advanced Topics).

Provides real-time progress updates during long-running operations
like scanning large directories.

Uses the FastMCP context for progress reporting.
"""

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP, Context


def register_progress_handlers(mcp: FastMCP) -> None:
    """
    Register progress-related handlers with the MCP server.

    This demonstrates the pattern for progress notifications using
    the FastMCP Context object.
    """

    @mcp.tool()
    async def scan_with_progress(
        directory_path: str,
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Scan a directory with real-time progress notifications.

        This demonstrates how to use progress notifications
        during a long-running operation.

        Args:
            directory_path: Path to the directory to scan.
            ctx: FastMCP context for progress reporting.

        Returns:
            JSON with scan results.
        """
        path = Path(directory_path)
        if not path.exists():
            return {"status": "error", "error": f"Directory not found: {directory_path}"}

        # Find all Python and JavaScript files
        files = []
        for ext in [".py", ".js", ".mjs", ".cjs"]:
            files.extend(list(path.rglob(f"*{ext}")))

        total = len(files)
        if total == 0:
            return {"status": "success", "files_scanned": 0, "message": "No files found"}

        # Report initial progress
        await ctx.report_progress(0, total, "Starting scan...")

        results = []
        from .scanner_adapter import scan_file

        for i, file in enumerate(files):
            # Report progress for each file
            await ctx.report_progress(
                i + 1,
                total,
                f"Scanning: {file.name} ({i+1}/{total})"
            )

            # Perform the scan
            try:
                result = scan_file(str(file))
                results.append(result)
            except Exception as e:
                results.append({
                    "status": "error",
                    "file": str(file),
                    "error": str(e)
                })

            # Small delay to make progress visible (for demonstration)
            await asyncio.sleep(0.01)

        # Report completion
        await ctx.report_progress(total, total, "Scan complete!")

        return {
            "status": "success",
            "directory": str(path),
            "files_scanned": total,
            "files": results
        }

    @mcp.tool()
    async def migrate_with_progress(
        source_directory: str,
        dry_run: bool = False,
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Run the full migration pipeline with progress notifications.

        Args:
            source_directory: Directory containing code to migrate.
            dry_run: If True, preview changes without writing.
            ctx: FastMCP context for progress reporting.

        Returns:
            Summary of migration operations.
        """
        path = Path(source_directory)
        if not path.exists():
            return {"status": "error", "error": f"Directory not found: {source_directory}"}

        # Step 1: Scan with progress
        await ctx.report_progress(0, 3, "Phase 1/3: Scanning files...")

        from .core import scan_directory
        scan_result = scan_directory(str(path))
        if scan_result.get("status") == "error":
            return scan_result

        files = scan_result.get("files", [])
        total_files = len(files)

        if total_files == 0:
            return {"status": "success", "message": "No deprecated API calls found"}

        # Step 2: Rewrite with progress
        await ctx.report_progress(1, 3, f"Phase 2/3: Rewriting {total_files} files...")

        from .core import rewrite_file
        rewrite_results = []
        for i, file_info in enumerate(files):
            file_path = file_info.get("path")
            if file_path:
                await ctx.report_progress(
                    i + 1,
                    total_files,
                    f"Rewriting: {Path(file_path).name} ({i+1}/{total_files})"
                )
                result = rewrite_file(file_path, dry_run=dry_run)
                rewrite_results.append(result)

        # Step 3: Validate with progress
        await ctx.report_progress(2, 3, "Phase 3/3: Validating modified files...")

        validation_results = []
        for i, result in enumerate(rewrite_results):
            if result.get("status") == "success" and result.get("changes_made", 0) > 0:
                file_path = result.get("file")
                if file_path:
                    await ctx.report_progress(
                        i + 1,
                        len(rewrite_results),
                        f"Validating: {Path(file_path).name}"
                    )
                    from .core import validate_file
                    validation_results.append(validate_file(file_path))

        # Report completion
        await ctx.report_progress(3, 3, "Migration complete!")

        total_changes = sum(r.get("changes_made", 0) for r in rewrite_results)
        files_modified = sum(1 for r in rewrite_results if r.get("changes_made", 0) > 0)
        errors = [r for r in validation_results if r.get("status") == "error"]

        return {
            "status": "success" if not errors else "partial",
            "directory": str(path),
            "dry_run": dry_run,
            "files_scanned": total_files,
            "files_modified": files_modified,
            "changes_made": total_changes,
            "errors": errors,
            "message": f"Migrated {files_modified} files with {total_changes} changes"
        }
