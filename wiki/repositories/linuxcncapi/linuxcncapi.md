# LinuxCNC API

**FastAPI REST + MQTT backend for remote monitoring and control of the Microb CNC machine.**

- **Repository:** `git@github.com:ymiroshnychenko668/linuxcncapi.git`
- **Role:** Non-real-time API layer — exposes machine state, handles tool change confirmation, publishes probe results via MQTT
- **Lifecycle:** Starts/stops automatically with LinuxCNC (loaded via `POSTGUI_HALCMD`)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| Framework | FastAPI + Uvicorn (ASGI) |
| Validation | Pydantic |
| Messaging | Paho-MQTT (broker on port 1883, WebSocket on 9001) |
| Database | SQLite |
| Testing | pytest, pytest-asyncio, pytest-cov |
| Linting | Ruff |

## How It Starts

1. LinuxCNC loads `corvuscnc.ini`
2. After GUI initializes, `POSTGUI_HALCMD` triggers `linuxcnc_api_launcher.sh`
3. Launcher starts FastAPI/Uvicorn as a background process on port 8080
4. API connects to MQTT broker and begins serving requests

**Do NOT start or stop this service manually** — it is a LinuxCNC module.

## API Endpoints

| Group | Endpoint | Purpose |
|-------|----------|---------|
| Health | `GET /health` | Server health status |
| Docs | `GET /docs` | Swagger UI |
| Status | `GET /api/machine/status` | Current machine state (position, mode) |
| Status | `GET /api/machine/position` | XYZ position |
| Status | `GET /api/machine/tool` | Current tool info |
| Status | `GET /api/machine/spindle` | Spindle speed and state |
| Control | `POST /api/machine/jog` | Jog command |
| Control | `POST /api/machine/home` | Home axis |
| Control | `POST /api/machine/spindle/speed` | Set spindle RPM |
| Probe | `GET /api/probe/results` | Probe measurements |
| Probe | `DELETE /api/probe/results` | Clear probe history |
| Tool Change | `POST /api/toolchange/confirm` | Confirm tool change via API |
| Tool Change | `POST /api/toolchange/abort` | Abort tool change via API |

## MQTT Topics

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `linuxcnc/status/messages/from_gui` | Publish | Forwarded UI messages (errors, warnings) |
| `linuxcnc/status/probing/result/#` | Publish | Probe measurement results |
| `linuxcnc/gui/heartbeat` | Publish | QtDragon online/offline status |
| `linuxcnc/toolchange/#` | Pub/Sub | Tool change events and control |
| `linuxcnc/machine/status` | Publish | Real-time machine state updates |

## Key Modules

### Manual Tool Change
- `api_toolchange_hal.py` — HAL component synchronizing tool change state between API and LinuxCNC
- Monitors HAL pins: `manual_toolchange.change`, `.changed`, `.number`, `.api_confirm`, `.api_abort`
- Allows remote operators to confirm/abort tool changes via REST or MQTT

### Probe Integration
- `probe_remap.py` — Python functions for M700/M701 G-code remap handlers
- `M700` → `clear_probe_results()` — clears retained MQTT probe data
- `M701` → `publish_probe_result()` — publishes measurement to MQTT
- Called from `python/remap.py` in corvuscnc

### INI Handler
- Parses LinuxCNC INI configuration for machine parameters
- Provides axis limits, speeds, and machine settings to API consumers

## Integration Points

| Component | Integration | Mechanism |
|-----------|-----------|-----------|
| corvuscnc.ini | `POSTGUI_HALCMD` | Launches API server after GUI load |
| python/remap.py | Python import | M700/M701 remap handlers call probe_remap |
| qtvcp/lib/mqtt_message_forwarder.py | MQTT | Forwards UI messages to API topics |
| manual_toolchange_dialog.py | HTTP/MQTT | Optional API-based tool change control |
| HAL pins | Poll-based | API reads machine state without blocking RT thread |

## Development

```bash
cd linuxcncapi
python run_tests.py                                    # All tests
python -m pytest tests/unit/services/test_ini_handler.py -v  # Single test
python -m pytest --cov=app --cov-report=html           # Coverage
python run_tests.py --quick                            # Smoke tests
curl http://localhost:8080/health                      # Health check
mosquitto_sub -t 'linuxcnc/#' -v                       # Monitor MQTT
```

## Architecture Note

The API operates in the **non-real-time domain**. It reads HAL pins for status but never blocks the servo thread (< 25 us latency requirement). All I/O, database, and MQTT operations are async.
