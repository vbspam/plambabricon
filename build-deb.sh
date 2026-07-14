#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# --- CONFIGURATION ---
PACKAGE_NAME="plambabricon"
VERSION="1.0.0"
ARCH="all"

MAINTAINER="vbspam <vbspam@centrum.cz>"

# Define local build directories
PROJECT_DIR="$(pwd)"
BUILD_ROOT="${PROJECT_DIR}/build"
BUILD_DIR="${BUILD_ROOT}/debian"
OUTPUT_DEB="${PROJECT_DIR}/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

echo "==========================================="
echo "🛠️  Building Pure Debian Package: ${PACKAGE_NAME} (${VERSION})"
echo "==========================================="

# 1. CLEAN STEP 
echo "🧹 Cleaning up old build directories and previous .deb..."
rm -rf "${BUILD_ROOT}"
rm -f "${OUTPUT_DEB}"

# 2. Create layout inside build/debian/
echo "📂 Creating package layout in build/debian/..."
mkdir -p "${BUILD_DIR}/DEBIAN"
mkdir -p "${BUILD_DIR}/usr/share/${PACKAGE_NAME}"
mkdir -p "${BUILD_DIR}/usr/bin"
mkdir -p "${BUILD_DIR}/etc/xdg/autostart"

# 3. Generate control file with SYSTEM dependencies
echo "📝 Generating DEBIAN/control..."
cat <<EOF > "${BUILD_DIR}/DEBIAN/control"
Package: ${PACKAGE_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: ${MAINTAINER}
Depends: python3, python3-pyqt6, python3-dbus-next, iio-sensor-proxy
Description: Plasma Ambient Based Brightness Control
 Automatically adjusts KDE Plasma screen brightness using the ambient light sensor.
 Uses system-provided PyQt6 and dbus-next libraries.
EOF

# 4. Copy all python source files directly to build/debian/usr/share/plambabricon
echo "📦 Copying Python source files..."
cp "${PROJECT_DIR}/plambabricond.py" "${BUILD_DIR}/usr/share/${PACKAGE_NAME}/"
cp "${PROJECT_DIR}/plambabricongui.py" "${BUILD_DIR}/usr/share/${PACKAGE_NAME}/"
cp "${PROJECT_DIR}/plambabricontray.py" "${BUILD_DIR}/usr/share/${PACKAGE_NAME}/"

# 5. Generate system-wide wrappers in /usr/bin using SYSTEM python
echo "🔗 Generating launcher wrappers..."

# Wrapper for daemon
cat <<EOF > "${BUILD_DIR}/usr/bin/plambabricond"
#!/bin/sh
export PYTHONPATH="/usr/share/${PACKAGE_NAME}:\$PYTHONPATH"
exec python3 /usr/share/${PACKAGE_NAME}/plambabricond.py "\$@"
EOF

# Wrapper for GUI
cat <<EOF > "${BUILD_DIR}/usr/bin/plambabricongui"
#!/bin/sh
export PYTHONPATH="/usr/share/${PACKAGE_NAME}:\$PYTHONPATH"
exec python3 /usr/share/${PACKAGE_NAME}/plambabricongui.py "\$@"
EOF

# Wrapper for Tray
cat <<EOF > "${BUILD_DIR}/usr/bin/plambabricontray"
#!/bin/sh
export PYTHONPATH="/usr/share/${PACKAGE_NAME}:\$PYTHONPATH"
exec python3 /usr/share/${PACKAGE_NAME}/plambabricontray.py "\$@"
EOF

chmod +x "${BUILD_DIR}/usr/bin/plambabricond"
chmod +x "${BUILD_DIR}/usr/bin/plambabricongui"
chmod +x "${BUILD_DIR}/usr/bin/plambabricontray"

# 6. Generate KDE Autostart for Tray App (launches the tray icon on startup)
echo "⚙️  Generating KDE Autostart..."
cat <<EOF > "${BUILD_DIR}/etc/xdg/autostart/plambabricontray.desktop"
[Desktop Entry]
Type=Application
Name=Plambabricon Tray
Comment=Plasma Ambient Based Brightness Control Tray Icon
Exec=plambabricontray
StartupNotify=false
Terminal=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
X-KDE-autostart-after=panel
EOF

# 7. Build package using the local directory
echo "📦 Packaging from build/debian/..."
dpkg-deb --build "${BUILD_DIR}" "${OUTPUT_DEB}"

# 8. Post-build CLEAN step
echo "✨ Build directory preserved at: build/debian/"

echo "==========================================="
echo "🎉 Pure Debian package created successfully!"
echo "➡️  File: ${OUTPUT_DEB}"
echo "==========================================="