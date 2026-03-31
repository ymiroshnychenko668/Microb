# Repository Map — Microb CNC Project

This product repository (`microb`) contains metainformation and submodules for the Microb CNC milling machine.

## Repository Tree

```
microb/                             (this repo — product metainformation)
├── corvuscnc/                      LinuxCNC machine configuration & software stack
│   ├── linuxcncapi/                FastAPI REST + MQTT backend for machine control
│   ├── corvusagent/                Git REST API & AI agent orchestration for PLM
│   ├── filebrowser/                Web-based G-code file manager
│   └── linuxcncsetup/              Controller provisioning & setup scripts
├── fusion/                         Fusion 360 CAD data (DSL schema + models)
├── specification/                  Product specifications (placeholder)
├── software/                       Related software repos (placeholder)
└── wiki/                           Product documentation
```

## Submodule Index

| Repository | Tech Stack | Role | Details |
|------------|-----------|------|---------|
| [corvuscnc](corvuscnc/) | LinuxCNC, Python, Qt5, HAL | CNC machine control system | [Details](corvuscnc/corvuscnc.md) |
| [linuxcncapi](linuxcncapi/) | Python, FastAPI, MQTT, SQLite | Machine REST API & messaging | [Details](linuxcncapi/linuxcncapi.md) |
| [corvusagent](corvusagent/) | Python, FastAPI, Claude SDK, MCP | PLM agent & Git REST service | [Details](corvusagent/corvusagent.md) |
| [filebrowser](filebrowser/) | Go, SQLite | Web file manager | [Details](filebrowser/filebrowser.md) |
| [linuxcncsetup](linuxcncsetup/) | Shell scripts | Controller provisioning | [Details](linuxcncsetup/linuxcncsetup.md) |

## System Integration Diagram

```
                    ┌──────────────────────────────────┐
                    │  Crow PLM/MES (Java/Spring Boot)  │
                    └──────────┬───────────────────────┘
                               │ REST / SSE
                    ┌──────────▼───────────────────────┐
                    │  corvusagent (Python FastAPI)      │
                    │  Git ops, AI agents, tool mgmt    │
                    └──────────┬───────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                     │
 ┌────────▼────────┐  ┌───────▼────────┐  ┌────────▼────────┐
 │   linuxcncapi    │  │  filebrowser   │  │  linuxcncsetup  │
 │  REST + MQTT     │  │  Web files     │  │  Provisioning   │
 │  port 8080       │  │  port 80       │  │  (one-time)     │
 └────────┬─────────┘  └───────┬────────┘  └─────────────────┘
          │                     │
 ┌────────▼─────────────────────▼─────────────────────────────┐
 │  LinuxCNC (PREEMPT-RT kernel)                               │
 │  ┌─────────────────────────────────────────────────────┐   │
 │  │  corvuscnc (HAL + INI + Qt UI + Python remaps)      │   │
 │  │  Mesa 7i76e → steppers, encoders, probes, spindle   │   │
 │  └─────────────────────────────────────────────────────┘   │
 └─────────────────────────────────────────────────────────────┘
```
