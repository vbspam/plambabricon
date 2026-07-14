#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

PROJECT_DIR="$(pwd)"
VENV_DIR="${PROJECT_DIR}/venv"

echo "==========================================="
echo "🐍 Setting up development virtual environment..."
echo "==========================================="

# 1. Remove the old environment for a clean start
if [ -d "${VENV_DIR}" ]; then
    echo "🧹 Removing existing virtual environment..."
    rm -rf "${VENV_DIR}"
fi

# 2. Create a fresh virtual environment
echo "📦 Creating new virtual environment in ./venv..."
python3 -m venv "${VENV_DIR}"

# 3. Upgrade core packaging tools
echo "📥 Upgrading pip and installing dependencies..."
"${VENV_DIR}/bin/pip" install --upgrade pip setuptools wheel

# 4. Install the project in editable mode via pyproject.toml
echo "🛠️  Installing plambabricon in editable mode..."
"${VENV_DIR}/bin/pip" install -e .

echo "==========================================="
echo "🎉 Development environment is ready!"
echo ""
echo "To start developing, activate the environment:"
echo "👉 source venv/bin/activate"
echo ""
echo "After activation, you can run:"
echo "🚀 plambabricontray  (Launch tray app)"
echo "🚀 plambabricongui   (Launch configuration GUI)"
echo "🚀 plambabricond     (Launch background daemon)"
echo "==========================================="