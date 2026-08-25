import os
import sys
from pathlib import Path
from unittest.mock import patch

# Ensure 'app' directory is in sys.path so tests run cleanly from repo root without external PYTHONPATH
app_dir = str(Path(__file__).resolve().parent.parent / "app")
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Set required environment variables before importing server components
os.environ.setdefault("ENDURAIN_URL", "http://localhost:8080")
os.environ.setdefault("ENDURAIN_USERNAME", "test_user")
os.environ.setdefault("ENDURAIN_PASSWORD", "test_password")

from mcp.server.mcpserver import MCPServer
import server
from client import client


def _get_registered_tools(mcp_instance: MCPServer):
    """Helper to access registered tools across MCP server internal representations."""
    if hasattr(mcp_instance, "_tool_manager") and hasattr(mcp_instance._tool_manager, "list_tools"):
        return mcp_instance._tool_manager.list_tools()
    raise AttributeError("Unable to retrieve registered tools from MCPServer instance")


def test_server_initialization():
    """Verify MCPServer instance initializes with correct name."""
    assert isinstance(server.mcp, MCPServer)
    assert server.mcp.name == "endurain"


def test_tool_registration():
    """Verify all expected Endurain tools are registered on the MCPServer."""
    expected_tools = {
        "get_recent_activities",
        "get_activity_detail",
        "get_activities_this_week",
        "get_weekly_summary",
        "get_monthly_summary",
        "get_activity_streams",
        "get_sleep",
        "get_steps",
        "get_weight",
    }
    
    tools = _get_registered_tools(server.mcp)
    registered_tools = {tool.name for tool in tools}
    assert expected_tools.issubset(registered_tools), f"Missing tools: {expected_tools - registered_tools}"


@patch("client.client.request")
def test_get_recent_activities_tool_capping(mock_request):
    """Test get_recent_activities tool execution and parameter capping (max 100)."""
    mock_request.return_value = [{"activity_id": 123, "name": "Run"}]
    
    # Mock user_id property to prevent network call to _login()
    with patch.object(type(client), "user_id", 42):
        tool_func = None
        for tool in _get_registered_tools(server.mcp):
            if tool.name == "get_recent_activities":
                tool_func = tool.fn
                break
                
        assert tool_func is not None
        # Passing 500 should be capped to 100
        result = tool_func(limit=500)
        assert len(result) == 1
        assert result[0]["activity_id"] == 123
        mock_request.assert_called_once_with(
            "GET",
            "/activities/user/42/page_number/1/num_records/100",
        )
