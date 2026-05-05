from datetime import datetime, timedelta, timezone

from mcp.server.fastmcp import FastMCP
from client import client


def register(mcp: FastMCP):

    @mcp.tool()
    def get_sleep(days: int = 7) -> list[dict]:
        """Get sleep records for the last N days.

        Args:
            days: Number of days to look back (default 7).
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days - 1)).date()
        result = client.request("GET", "/health/sleep")
        records = result.get("records", []) if isinstance(result, dict) else []
        return [r for r in records if r.get("date", "") >= str(cutoff)]

    @mcp.tool()
    def get_steps(days: int = 7) -> list[dict]:
        """Get daily step counts for the last N days.

        Args:
            days: Number of days to look back (default 7).
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days - 1)).date()
        result = client.request("GET", "/health/steps")
        records = result.get("records", []) if isinstance(result, dict) else []
        return [r for r in records if r.get("date", "") >= str(cutoff)]

    @mcp.tool()
    def get_weight(days: int = 30) -> list[dict]:
        """Get weight entries for the last N days.

        Args:
            days: Number of days to look back (default 30).
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days - 1)).date()
        result = client.request("GET", "/health/weight")
        records = result.get("records", []) if isinstance(result, dict) else []
        return [r for r in records if r.get("date", "") >= str(cutoff)]
