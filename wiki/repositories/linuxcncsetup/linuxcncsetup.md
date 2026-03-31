# LinuxCNC Setup

**Controller provisioning and setup scripts for the Microb CNC machine.**

- **Repository:** `git@github.com:ymiroshnychenko668/linuxcncsetup.git`
- **Role:** One-time provisioning tooling — installs dependencies, configures the PREEMPT-RT kernel, sets up the LinuxCNC environment on a new controller machine
- **Status:** Submodule not initialized locally (content not available for detailed analysis)

## Tech Stack (Inferred)

| Component | Technology |
|-----------|-----------|
| Scripts | Shell (Bash) |
| Target OS | PREEMPT-RT Linux |
| Package management | apt (Debian/Ubuntu-based) |

## Expected Capabilities

Based on the corvuscnc ecosystem requirements, this submodule likely handles:

- PREEMPT-RT kernel installation and configuration
- LinuxCNC 2.9 installation from source or packages
- Mesa 7i76e Ethernet card driver setup
- Python 3.11+ environment setup
- Qt5 / qtvcp dependencies
- MQTT broker (Mosquitto) installation
- Network configuration for Mesa card (192.168.1.121)
- Modbus/RS-485 setup for Delta VFD-E spindle
- User permissions (real-time scheduling, serial port access)
- Filebrowser installation (`install_filebrowser.sh` in corvuscnc handles the file manager portion)

## Initialization

```bash
cd corvuscnc
git submodule update --init linuxcncsetup
```

## Related

The filebrowser and linuxcncapi submodules have their own install scripts within corvuscnc, but linuxcncsetup handles the base system provisioning that everything else depends on.
