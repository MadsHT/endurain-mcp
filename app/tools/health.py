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
        end = datetime.now(timezone.utc).date()
        start = end - timedelta(days=days - 1)
        result = client.request(
            "GET",
            "/health/sleep",
            params={"start_date": str(start), "end_date": str(end)},
        )
        return result or []

    @mcp.tool()
    def get_steps(days: int = 7) -> list[dict]:
        """Get daily step counts for the last N days.

        Args:
            days: Number of days to look back (default 7).
        """
        end = datetime.now(timezone.utc).date()
        start = end - timedelta(days=days - 1)
        result = client.request(
            "GET",
            "/health/steps",
            params={"start_date": str(start), "end_date": str(end)},
        )
        return result or []

    @mcp.tool()
    def get_weight(days: int = 30) -> list[dict]:
        """Get weight entries for the last N days.

        Args:
            days: Number of days to look back (default 30).
        """
        end = datetime.now(timezone.utc).date()
        start = end - timedelta(days=days - 1)
        result = client.request(
            "GET",
            "/health/weight",
            params={"start_date": str(start), "end_date": str(end)},
        )
        return result or []
