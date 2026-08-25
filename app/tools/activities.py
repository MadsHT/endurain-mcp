from mcp.server.mcpserver import MCPServer
from client import client


def register(mcp: MCPServer):

    @mcp.tool()
    def get_recent_activities(limit: int = 10) -> list[dict]:
        """Get the most recent activities for the authenticated user.

        Args:
            limit: Number of activities to return (default 10, max 100).
        """
        limit = max(1, min(limit, 100))
        result = client.request(
            "GET",
            f"/activities/user/{client.user_id}/page_number/1/num_records/{limit}",
        )
        return result or []

    @mcp.tool()
    def get_activity_detail(activity_id: int) -> dict:
        """Get full detail for a single activity by its ID.

        Args:
            activity_id: The numeric ID of the activity.
        """
        return client.request("GET", f"/activities/{activity_id}") or {}

    @mcp.tool()
    def get_activities_this_week() -> list[dict]:
        """Get all activities recorded in the current week."""
        result = client.request(
            "GET",
            f"/activities/user/{client.user_id}/week/0",
        )
        return result or []

    @mcp.tool()
    def get_weekly_summary() -> dict:
        """Get distance totals broken down by sport type for the current week."""
        result = client.request(
            "GET",
            f"/activities/user/{client.user_id}/thisweek/distances",
        )
        return result or {}

    @mcp.tool()
    def get_monthly_summary() -> dict:
        """Get distance totals broken down by sport type for the current month."""
        result = client.request(
            "GET",
            f"/activities/user/{client.user_id}/thismonth/distances",
        )
        return result or {}

    @mcp.tool()
    def get_activity_streams(activity_id: int) -> list[dict]:
        """Get all time-series streams for an activity (heart rate, elevation, GPS, pace, cadence, etc.).

        Args:
            activity_id: The numeric ID of the activity.
        """
        result = client.request(
            "GET",
            f"/activities_streams/activity_id/{activity_id}/all",
        )
        return result or []
