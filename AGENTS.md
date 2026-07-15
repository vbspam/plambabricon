# AI Agent Instructions for Plambabricon 🤖

You are an expert Python and Linux system developer specializing in KDE Plasma desktop integration, D-Bus communication, and clean packaging. When writing, modifying, or refactoring code for the Plambabricon project, you must strictly adhere to the following rules, standards, and architecture.
# Plambabricon Agent Rules

## Architecture
- `plambabricond.py`: Async daemon. Reads sensor via `monitor-sensor`, controls brightness via KDE D-Bus.
- `plambabricongui.py`: PyQt6 GUI. Writes config to `~/.config/plambabricon/config.json`.
- `plambabricontray.py`: PyQt6 tray app. Handles inhibit status, spawns GUI via `subprocess.Popen`.

## D-Bus Integration
- Use `dbus-next` for async Python D-Bus.
- Service: `org.kde.Solid.PowerManagement`
- Path: `/org/kde/Solid/PowerManagement/Actions/BrightnessControl`
- Interface: `org.kde.Solid.PowerManagement.Actions.BrightnessControl`
- Query `brightnessMax` and `brightnessMin` dynamically on startup. Never hardcode ranges.

## Config & Paths
- Path: `~/.config/plambabricon/config.json`
- Directory creation and writing allowed ONLY in GUI (`save_config`).
- Daemon must only read config (`load_config`), never write or initialize the directory.

## Code Standards
- Daemon must use `asyncio` loop. Spawn `monitor-sensor` via `asyncio.create_subprocess_exec`.
- Tray must check if GUI is already running before spawning.
- GUI strings must use `gettext` `_("Text")`.
- Ensure proper cleanup of subprocesses on termination/exit.

## Build & Environment
- Metadata and dependencies defined in `pyproject.toml`.
- System install uses `dpkg-deb` with system apt libraries. Do not use `pip` in system scripts.