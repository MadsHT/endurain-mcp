import os
import pytest
from unittest.mock import patch, MagicMock

# Set required environment variables before importing server components
os.environ.setdefault("ENDURAIN_URL", "http://localhost:8080")
os.environ.setdefault("ENDURAIN_USERNAME", "test_user")
os.environ.setdefault("ENDURAIN_PASSWORD", "test_password")

from mcp.server.mcpserver import MCPServer
import server
from client import client


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
    
    registered_tools = {tool.name for tool in server.mcp._tool_manager.list_tools()}
    assert expected_tools.issubset(registered_tools), f"Missing tools: {expected_tools - registered_tools}"


@patch("client.client.request")
def test_get_recent_activities_tool(mock_request):
    """Test get_recent_activities tool execution and parameter capping."""
    mock_request.return_value = [{"activity_id": 123, "name": "Run"}]
    
    # Mock user_id property to prevent network call to _login()
    with patch.object(type(client), "user_id", 42):
        tool_func = None
        for tool in server.mcp._tool_manager.list_tools():
            if tool.name == "get_recent_activities":
                tool_func = tool.fn
                break
                
        assert tool_func is not None
        result = tool_func(limit=5)
        assert len(result) == 1
        assert result[0]["activity_id"] == 123
        mock_request.assert_called_once_with(
            "GET",
            "/activities/user/42/page_number/1/num_records/5",
        )
