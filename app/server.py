import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.mcpserver import MCPServer
import tools.activities as activities_tools
import tools.health as health_tools

mcp = MCPServer("endurain")

activities_tools.register(mcp)
health_tools.register(mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
