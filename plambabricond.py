#!/usr/bin/env python3
import asyncio
import subprocess
import re
import math
import sys
import json
from pathlib import Path
from dbus_next.aio import MessageBus

CONFIG_DIR = Path.home() / ".config" / "plambabricon"
CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "min_brightness": 10,   # In percent (0-100)
    "max_brightness": 100,  # In percent (0-100)
    "max_lux": 1000,
    "hysteresis": 3
}

current_brightness_pct = -1

# These values will be dynamically loaded from KDE D-Bus
hw_min_brightness = 0
hw_max_brightness = 100  # Fallback default

def load_config():
    """Loads the configuration file on the fly."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            pass
    return DEFAULT_CONFIG

def calculate_brightness_pct(lux, config):
    """Calculates target brightness percentage using a logarithmic scale."""
    min_b = config["min_brightness"]
    max_b = config["max_brightness"]
    max_l = config["max_lux"]
    
    if lux <= 3:
        return min_b
    scale = (math.log10(min(lux, max_l)) / math.log10(max_l))
    brightness_pct = min_b + (max_b - min_b) * scale
    return int(max(min_b, min(max_b, brightness_pct)))

def pct_to_hw(pct):
    """Maps percentage (0-100) to the hardware brightness range."""
    global hw_min_brightness, hw_max_brightness
    hw_val = hw_min_brightness + (pct / 100.0) * (hw_max_brightness - hw_min_brightness)
    return int(hw_val)

async def main():
    global current_brightness_pct, hw_min_brightness, hw_max_brightness
    
    try:
        bus = await MessageBus().connect()
        introspection = await bus.introspect(
            "org.kde.Solid.PowerManagement",
            "/org/kde/Solid/PowerManagement/Actions/BrightnessControl"
        )
        proxy_object = bus.get_proxy_object(
            "org.kde.Solid.PowerManagement",
            "/org/kde/Solid/PowerManagement/Actions/BrightnessControl",
            introspection
        )
        brightness_control = proxy_object.get_interface(
            "org.kde.Solid.PowerManagement.Actions.BrightnessControl"
        )
        
        # Query hardware limits from KDE
        hw_max_brightness = await brightness_control.call_brightness_max()
        hw_min_brightness = await brightness_control.call_brightness_min()
        print(f"Detected hardware brightness limits: Min={hw_min_brightness}, Max={hw_max_brightness}")
        
    except Exception as e:
        print(f"Error: Failed to connect to KDE D-Bus or fetch limits ({e}).", file=sys.stderr)
        sys.exit(1)

    print("Starting automatic ambient brightness control...")

    # Start monitor-sensor as an async subprocess
    process = await asyncio.create_subprocess_exec(
        "monitor-sensor",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    lux_regex = re.compile(r"Light changed:\s+([0-9.]+)\s+\(lux\)")

    try:
        while True:
            line = await process.stdout.readline()
            if not line:
                break
                
            decoded_line = line.decode('utf-8', errors='ignore')
            match = lux_regex.search(decoded_line)
            
            if match:
                config = load_config()
                lux_val = float(match.group(1))
                
                # Calculate target brightness percentage
                target_pct = calculate_brightness_pct(lux_val, config)
                
                # Check hysteresis before applying changes
                if current_brightness_pct == -1 or abs(target_pct - current_brightness_pct) >= config["hysteresis"]:
                    target_hw = pct_to_hw(target_pct)
                    try:
                        await brightness_control.call_set_brightness(target_hw)
                        current_brightness_pct = target_pct
                        print(f"Brightness: {target_pct}% (HW: {target_hw}) [Lux: {lux_val:.1f}]")
                    except Exception as e:
                        print(f"D-Bus error while setting brightness: {e}", file=sys.stderr)
                        
    except asyncio.CancelledError:
        pass
    finally:
        try:
            process.terminate()
            await process.wait()
        except ProcessLookupError:
            pass

def main_entry():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[plambabricon] Daemon shutting down...")

if __name__ == "__main__":
    main_entry()