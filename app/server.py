import sys
from pathlib import Path

# Ensure app/ is on the path so client.py and tools/ are importable
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
import tools.activities as activities_tools
import tools.health as health_tools

mcp = FastMCP("endurain", host="0.0.0.0", port=8000)

activities_tools.register(mcp)
health_tools.register(mcp)

# Expose the ASGI app for uvicorn so session crashes don't kill the process
sse_app = mcp.sse_app()

if __name__ == "__main__":
    mcp.run(transport="sse")
