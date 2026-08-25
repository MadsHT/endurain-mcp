import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
import tools.activities as activities_tools
import tools.health as health_tools

# 1. Initialize FastMCP normally
mcp = FastMCP("endurain", host="0.0.0.0", port=8000)

activities_tools.register(mcp)
health_tools.register(mcp)

# 2. Force Uvicorn to run it strictly in stateless HTTP mode
# This bypasses the session-manager list leak completely!
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        stateless_http=True
    )
