#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

PROJECT_DIR="$(pwd)"

echo "==========================================="
echo "🧹 Cleaning project directory..."
echo "==========================================="

# 1. Remove build directories and debian artifacts
echo "Removing build/ and debian artifacts..."
rm -rf "${PROJECT_DIR}/build"
rm -f "${PROJECT_DIR}"/*.deb
rm -rf "${PROJECT_DIR}/bin"
rm -rf "${PROJECT_DIR}/lib"
rm -rf "${PROJECT_DIR}/lib64"
rm -rf "${PROJECT_DIR}/include"
rm -rf "${PROJECT_DIR}/venv"

# 2. Remove Python compilation caches and metadata
echo "Removing Python compilation caches and egg-info..."
rm -rf "${PROJECT_DIR}/plambabricon.egg-info"
find "${PROJECT_DIR}" -type d -name "__pycache__" -exec rm -rf {} +
find "${PROJECT_DIR}" -type f -name "*.pyc" -delete
find "${PROJECT_DIR}" -type f -name "*.pyo" -delete

# 3. Remove temporary files used by AppImage builds (if any exist)
rm -rf "/tmp/plambabricon-appdir" "/tmp/plambabricon-tools"

echo "✨ Workspace is clean!"
echo "==========================================="