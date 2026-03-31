# CorvusAgent

**Git REST API, AI agent orchestration, and developer tool management for Crow PLM integration.**

- **Repository:** `git@github.com:ymiroshnychenko668/corvusagent.git`
- **Role:** Bridge between the Crow PLM/MES platform (Java/Spring Boot) and remote environments — provides Git ops, network config, AI agents, and tool lifecycle management
- **Default port:** 8765 (configurable)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Framework | FastAPI + Uvicorn |
| AI/Agent | Claude Code SDK, MCP (Model Context Protocol), SSE Starlette |
| HTTP Client | httpx (async, for Crow API calls) |
| Git | GitPython |
| Cache | Hazelcast Python Client 5.4+ |
| Database | SQLite3 (config, tool state, port overrides) |
| Testing | pytest, mypy, ruff |
| Deployment | systemd (Linux), launchd (macOS), Windows Service |

## API Surface

### Git Operations
| Endpoint | Purpose |
|----------|---------|
| `/git/status`, `/git/log`, `/git/branch/*` | Read operations |
| `/git/fetch`, `/git/pull`, `/git/push`, `/git/merge` | Sync operations |
| `/git/worktree/add`, `/git/worktree/remove` | Worktree management |
| `/repositories`, `/repositories/search` | Repo discovery |

### Network Configuration
| Endpoint | Purpose |
|----------|---------|
| `/network/interfaces` | List network interfaces |
| `/network/interfaces/{iface}/configure-*` | Ethernet/WiFi setup (DHCP/static) |

### Tool Lifecycle
| Endpoint | Purpose |
|----------|---------|
| `/tools`, `/tools/{name}/*` | Install/start/stop/status/delete tools |

Available tools:
- **Code Server** (port 3100) — VS Code in browser
- **ttyd** (port 7681) — web terminal (tmux-backed)
- **Hazelcast** (port 5701) — in-memory data grid

### AI Agents
| Endpoint | Purpose |
|----------|---------|
| `/agents` | List pre-registered agents |
| `/agent/stream` | SSE streaming agent interaction |
| `/agent/self/update`, `/agent/self/restart` | Self-management |

Pre-registered agents:
- **PLM Engineering Assistant** — searches components, BOMs, products via `crow-plm` MCP server
- **Wiki Assistant** — searches & reads documentation via `crow-wiki` MCP server

### Claude Code Proxy
| Endpoint | Purpose |
|----------|---------|
| `/api/claude/projects` | List Claude Code projects |
| `/api/claude/histories` | List session histories |
| `/api/claude/conversations/{id}` | Load conversation |
| `/api/claude/chat` | Streaming chat (NDJSON) |

## Security Model

- **Localhost-only binding** (127.0.0.1 / ::1) with Host header validation
- **Path sandboxing** — all Git operations restricted to `BASE_ROOT`
- **Command whitelisting** — subprocess with argument validation, no shell
- **Audit logging** — every Git command logged to `logs/audit.log`
- **Optional token auth** — `ENABLE_TOKEN_AUTH=true` + `API_TOKEN`
- **Rate limiting** — per-client IP (configurable RPM)

## Integration with Crow PLM

1. **Java orchestrator** spawns CorvusAgent: `python3 crow_agent.py --port 9800 --base-dir ~/.corvusagent`
2. Communicates via REST at `http://127.0.0.1:9800`
3. MCP servers call Crow REST API (`http://localhost:8080/api/plm/*`, `api/wiki/*`)
4. Handles Git operations for DSL sync (per `FileReplicatedEntity` pattern)
5. Connects to Crow's Hazelcast cluster for distributed caching

## Directory Structure

```
corvusagent/
├── app/
│   ├── main.py              FastAPI app, middleware, lifespan
│   ├── config.py            Pydantic settings
│   ├── routers/             8 API router modules
│   ├── services/            Business logic (git, network, tools, agents)
│   ├── tooldefs/            Auto-discovered tool definitions
│   ├── agents/              Pre-registered AI agents (plm, wiki)
│   ├── claude_proxy/        Claude Code IDE integration
│   └── mcp_servers/         MCP stdio server implementations
├── tests/                   pytest suite
├── scripts/                 install/format/test scripts
├── crow_agent.py            CLI entry point
├── Makefile                 Build targets
└── requirements.txt         Dependencies
```

## Development

```bash
make start-dev          # Auto-reload dev server
make test               # Run tests
make test-cov           # Tests + coverage
make lint               # Ruff linting
make type-check         # mypy static analysis
make format             # Code formatting
```

## Deployment

```bash
sudo make install-systemd BASE_ROOT=/path/to/repos    # Linux
make install-launchd BASE_ROOT=/path/to/repos          # macOS
make docker-build && make docker-run                   # Docker
```
