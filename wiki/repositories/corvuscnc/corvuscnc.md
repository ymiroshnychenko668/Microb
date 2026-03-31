# CorvusCNC

**LinuxCNC configuration and software stack for the Microb CNC milling machine.**

- **Repository:** `https://github.com/ymiroshnychenko668/corvuscnc.git`
- **Role:** Top-level CNC control system — machine configs, operator UI, hardware integration, and four nested service submodules

## Tech Stack

| Layer | Technology |
|-------|-----------|
| CNC Platform | LinuxCNC 2.9 (PREEMPT-RT kernel, servo latency < 25 us) |
| Motion Controller | Mesa 7i76e Ethernet (192.168.1.121) — 5 stepgens, 1 encoder |
| Spindle | Delta VFD-E, 4500 W, 12k–20k RPM via Modbus RS-485 |
| Operator UI | QtDragon HD (Qt5 / qtvcp) — custom `crow_cnc_hd` screen |
| Scripting | Python 3.11+, G-code (NGC), HAL scripting |
| Probe System | 95+ probe routines in 9 categories |
| Backend Services | FastAPI (linuxcncapi), MQTT, SQLite |
| PLM Integration | CorvusAgent (Git REST + Claude SDK) |
| File Management | Filebrowser (Go binary, port 80) |

## Machine Specifications

| Axis | Range | Max Velocity | Notes |
|------|-------|-------------|-------|
| X | 0–1200 mm | 40 mm/s | |
| Y | 0–2500 mm | 28.125 mm/s | Dual-motor XYYZ gantry |
| Z | -420–0 mm | 25 mm/s | |
| A *(optional)* | 360 deg | 360 deg/s | 5:1 gear reduction |

**Tool change position:** X=28 mm, Y=48 mm, Z=0 mm

## Configuration Variants

| INI File | Description |
|----------|-------------|
| `corvuscnc.ini` | Primary 3-axis production config |
| `corvuscnc_4axis.ini` | 4-axis with rotational A-axis |
| `corvus_cnc_sim.ini` | Simulator (no hardware required) |
| `g540.ini` | Parallel port G540 alternative |

## Directory Structure

```
corvuscnc/
├── *.ini / *.hal              Machine & HAL configurations
├── hal/
│   ├── 7i76eu/                Mesa 7i76e HAL (probe, coolant, endstops, spindle)
│   ├── deltavfde/             Delta VFD-E Modbus spindle control
│   ├── mtc/                   Manual tool change HAL wiring
│   ├── 7i92th/                7i92TH variant
│   └── sim/                   Simulator HAL
├── qtvcp/
│   ├── screens/crow_cnc_hd/   Operator interface (handler + 14 mixins, 3 themes)
│   ├── widgets/               47 local widgets + probe_routines_lib (95+ routines)
│   └── lib/                   11 local libs + MQTT message forwarder
├── python/                    G-code remap handlers (M6 tool change, M700/M701 probe)
├── remap-subroutines/         NGC subroutines (tool change, probing, abort)
├── docs/                      Operator documentation (en/ + uk/)
├── linuxcncapi/               [submodule] REST + MQTT backend
├── corvusagent/               [submodule] Git REST & AI agent service
├── filebrowser/               [submodule] Web file manager
└── linuxcncsetup/             [submodule] Provisioning scripts
```

## HAL Architecture

HAL files are loaded in cascading order:

1. **Main HAL** (`corvuscnc.hal`) — loads Mesa card, PIDs, stepgens, core wiring
2. **Hardware HAL** (`hal/7i76eu/*.hal`) — probe pins, coolant, endstops, spindle
3. **Spindle HAL** (`hal/deltavfde/delta_vfde_modbus.hal`) — Modbus RS-485 VFD control
4. **Custom HAL** (`custom.hal`) — user customizations (tool change, joystick)
5. **Post-GUI HAL** (`custom_postgui.hal`) — services started after Qt UI loads

### Key HAL Pins

| Pin | Purpose |
|-----|---------|
| `manual_toolchange.change` | Triggers tool change (from motion controller) |
| `manual_toolchange.changed` | Confirms completion (read by motion controller) |
| `manual_toolchange.number` | Requested tool number |
| `manual_toolchange.api_confirm` | API signal to confirm tool change |
| `manual_toolchange.api_abort` | API signal to abort tool change |
| `motion.probe-input` | Filtered probe signal (dual input, debounced 15 ms) |

## Operator Interface (crow_cnc_hd)

The custom Qt5 screen is built with a **mixin architecture** — 14 feature-specific Python modules mixed into the main handler:

- Responsive layout adaptation
- Runtime machine state management
- Keybinding support
- Dashboard panel (consolidated status)
- 3 color themes (blueprint, amber, default)
- Ukrainian language support (`corvus_i18n.py`)

### Probe System

95+ probe routines organized into 9 categories:

| Category | Examples |
|----------|---------|
| calibration | Probe offset calibration |
| features | Feature detection |
| tool | Tool measurement |
| surface | Surface measurement |
| outside | Outer edge detection |
| inside | Hole detection |
| length | Tool length measurement |
| skew | Angle/skew detection |
| material | Material detection |

## Widget Dependencies

Per `dependency.md` audit (2026-03-23):
- 47 local widget files: 34 system copies + 6 custom overrides + 7 original
- 11 local library files: 9 system copies + 2 custom (MQTT forwarder)
- 154 widget instances across 25 widget classes — all resolved locally
- Zero external dependency except `qtvcp.core` framework and `qt5_graphics`

## Nested Submodules

| Submodule | Purpose | Port |
|-----------|---------|------|
| [linuxcncapi](../linuxcncapi/linuxcncapi.md) | REST + MQTT machine API | 8080 |
| [corvusagent](../corvusagent/corvusagent.md) | Git REST & AI agents for PLM | 8765 |
| [filebrowser](../filebrowser/filebrowser.md) | Web G-code file manager | 80 |
| [linuxcncsetup](../linuxcncsetup/linuxcncsetup.md) | Controller provisioning | — |

## Quick Start

```bash
git submodule update --init --recursive
linuxcnc corvuscnc.ini          # 3-axis production
linuxcnc corvuscnc_4axis.ini    # 4-axis
linuxcnc corvus_cnc_sim.ini     # Simulator
curl http://localhost:8080/health  # Check API
```
