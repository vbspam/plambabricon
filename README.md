# Plambabricon 🌟
> **Pl**asma **Am**bient **Ba**sed **Bri**ghtness **Con**trol

`plambabricon` is a lightweight ambient light brightness controller designed for **KDE Plasma**. It automatically adjusts your laptop's display brightness based on your hardware ambient light sensor.

The project is split into three components: a background daemon, a lightweight system tray applet, and a configuration GUI.

---

## 🛠 Features
- **Daemon on Autopilot:** Runs asynchronously in the background, listening to the ambient light sensor.
- **Lightweight System Tray:** Sits quietly in your system tray, allowing you to temporarily inhibit automatic regulation or launch settings with a single click.
- **Logarithmic Scaling:** Matches how the human eye naturally perceives brightness changes.
- **Native Hardware Scaling:** Queries `brightnessMin` and `brightnessMax` from KDE D-Bus, seamlessly supporting devices with non-standard hardware ranges (e.g., 0-255 vs 0-10000).
- **Smooth Transitions (Hysteresis):** Prevents screen flickering due to tiny, rapid light fluctuations.
- **Modern Config GUI:** Native PyQt6 interface to adjust limits and sensitivity on the fly.
- **Proper XDG Standards:** Keeps your system clean by storing configuration in `~/.config/plambabricon/config.json`.

---

## 📂 Project Structure

```text
plambabricon/
├── pyproject.toml              # Python project metadata & editable install config
├── plambabricond.py            # Async background service (Daemon)
├── plambabricongui.py          # Native configuration utility (GUI)
├── plambabricontray.py         # System tray application & menu launcher
├── build-deb.sh                # Pure Debian package builder script
├── clean.sh                    # Workspace cleanup script
├── setup-env.sh                # Development venv bootstrapper
└── README.md                   # You are here!
```

---

## 📦 Packaging & Installation (.deb)

If you want a clean, system-wide installation that automatically runs the tray applet at startup, you can build and install a `.deb` package.

### 1. Build the package
From the root of the project directory, run the build script:
```bash
chmod +x build-deb.sh
./build-deb.sh
```

### 2. Install the package
Install the generated `.deb` file using `apt` (which will automatically resolve PyQt6 and D-Bus dependencies from system repositories):
```bash
sudo apt install ./plambabricon_1.0.0_all.deb
```

Once installed, the **Plambabricon Tray** applet will automatically start on your next login.

---

## 💻 Local Development

If you want to modify the code or run it locally without installing it system-wide, we provide automation scripts to set up a sandboxed environment.

### 1. Setup the virtual environment
The `setup-env.sh` script automatically creates a clean Python virtual environment, upgrades core packaging tools, and installs the project in editable mode:
```bash
chmod +x setup-env.sh clean.sh
./setup-env.sh
```

### 2. Run components
Activate the environment and run any of the components:
```bash
source venv/bin/activate

# Run the background daemon
plambabricond

# Run the system tray launcher
plambabricontray

# Run the settings GUI directly
plambabricongui
```

### 3. Clean the workspace
To remove all build caches, `__pycache__` directories, and build artifacts:
```bash
./clean.sh
```