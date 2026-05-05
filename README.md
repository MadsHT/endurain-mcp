# endurain-mcp

A Model Context Protocol (MCP) server that exposes [Endurain](https://codeberg.org/endurain-project/endurain) fitness data as tools for AI assistants such as OpenCode.

Runs as a Docker container, communicates with your Endurain instance over HTTP, and exposes an SSE endpoint that MCP clients can connect to remotely.

## Architecture

```
AI Assistant (e.g. OpenCode)
    |
    | HTTPS (mcp-remote)
    v
https://your-mcp-domain.example.com  (reverse proxy)
    |
    | HTTP (internal network)
    v
endurain-mcp container (port 8000)
    |
    | HTTPS
    v
https://your-endurain-domain.example.com
```

## Available tools

| Tool | Description |
|---|---|
| `get_recent_activities(limit)` | Last N activities (default 10) |
| `get_activity_detail(activity_id)` | Full detail for a single activity |
| `get_activities_this_week()` | All activities in the current week |
| `get_weekly_summary()` | Distance totals by sport type this week |
| `get_monthly_summary()` | Distance totals by sport type this month |
| `get_sleep(days)` | Sleep records for the last N days (default 7) |
| `get_steps(days)` | Daily step counts for the last N days (default 7) |
| `get_weight(days)` | Weight entries for the last N days (default 30) |

## Deployment

### 1. Pull the image

```bash
docker pull ghcr.io/madsht/endurain-mcp:latest
```

### 2. Deploy with Docker Compose

Copy the `docker-compose.yml` and fill in your credentials:

```yaml
services:
  endurain-mcp:
    image: ghcr.io/madsht/endurain-mcp:latest
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      ENDURAIN_URL: https://your-endurain-domain.example.com
      ENDURAIN_USERNAME: your_username
      ENDURAIN_PASSWORD: your_password
```

```bash
docker compose up -d
```

### 3. Expose via reverse proxy

Point a subdomain (e.g. `https://your-mcp-domain.example.com`) at port `8000` on the Docker host.

### 4. Configure your MCP client

For OpenCode, add the following to `~/.config/opencode/opencode.json`:

```json
"endurain": {
  "type": "local",
  "command": [
    "npx", "-y", "mcp-remote",
    "https://your-mcp-domain.example.com/sse"
  ],
  "enabled": true
}
```

## Environment variables

| Variable | Description |
|---|---|
| `ENDURAIN_URL` | Base URL of your Endurain instance |
| `ENDURAIN_USERNAME` | Endurain login username |
| `ENDURAIN_PASSWORD` | Endurain login password |

## Development

```bash
git clone https://github.com/madsht/endurain-mcp
cd endurain-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ENDURAIN_URL=https://your-endurain-domain.example.com \
ENDURAIN_USERNAME=your_username \
ENDURAIN_PASSWORD=your_password \
python app/server.py
```

## License

MIT
