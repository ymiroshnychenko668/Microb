# Filebrowser

**Web-based G-code file manager for the Microb CNC machine.**

- **Repository:** `https://github.com/ymiroshnychenko668/filebrowser` (custom fork)
- **Role:** Provides browser-accessible file management for G-code (NC) files without requiring direct filesystem access
- **Port:** 80 (HTTP)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Application | Filebrowser (open-source, Go binary) |
| Database | SQLite (`filebrowser.db`) |
| Integration | Shell scripts + LinuxCNC HAL commands |
| OS | PREEMPT-RT Linux (same host as LinuxCNC) |

## How It Works

Filebrowser is **lifecycle-bound to LinuxCNC** — it starts when the CNC starts and stops when it shuts down.

### Startup
1. LinuxCNC loads and GUI (QtDragon) initializes
2. `custom_postgui.hal` triggers: `loadusr filebrowser_launcher.sh`
3. Launcher checks for stale PID, starts binary in background
4. Filebrowser serves files at `http://<machine-ip>/`

### Shutdown
1. LinuxCNC triggers `shutdown.hal`
2. `filebrowser_shutdown.sh` reads PID file, sends SIGTERM
3. Process exits cleanly, PID file removed

## Configuration

| Setting | Value |
|---------|-------|
| Binary | `filebrowser/filebrowser` |
| Root directory | `/home/user/linuxcnc/nc_files` |
| Address | `0.0.0.0` (all interfaces) |
| Port | 80 |
| Authentication | Disabled (`--noauth`) |
| Database | `filebrowser.db` (SQLite, 65 KB) |
| PID file | `filebrowser/filebrowser.pid` |

## Key Files

| File | Purpose |
|------|---------|
| `filebrowser_launcher.sh` | Starts filebrowser with config, PID tracking, stale PID cleanup |
| `filebrowser_shutdown.sh` | Graceful stop via SIGTERM + PID file cleanup |
| `install_filebrowser.sh` | One-time setup: init submodule, set `cap_net_bind_service`, create dirs |
| `filebrowser.db` | SQLite persistent config (users, permissions, settings) |

## Installation

```bash
cd corvuscnc
./install_filebrowser.sh
# Steps: git submodule init, setcap for port 80, create nc_files dir
```

The `setcap 'cap_net_bind_service=+ep'` capability allows the non-root binary to bind to port 80.

## Access

- **Local:** `http://localhost/`
- **Network:** `http://<machine-ip>/`
- **No authentication** — suitable for closed workshop networks only
- Files are sandboxed to `/home/user/linuxcnc/nc_files` (no parent directory access)
