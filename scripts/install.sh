#!/bin/bash
# scripts/install.sh - Installation script for MJAS v3.0

set -e

echo "================================"
echo "MJAS v3.0 Installation"
echo "================================"
echo

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "ERROR: pyproject.toml not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -e ".[dev]"

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Create directory structure
echo "Setting up directories..."
mkdir -p logs data config screenshots

# Check for resume
echo
echo "================================"
echo "Next Steps:"
echo "================================"
echo

if [ ! -f "config/musharraf_kazi_resume.pdf" ]; then
    echo "1. Copy your resume to: config/musharraf_kazi_resume.pdf"
    echo
fi

echo "2. Set up credentials using the wizard:"
echo "   python scripts/setup_credentials.py"
echo

echo "3. Or manually copy the template:"
echo "   cp config/credentials.env.example config/credentials.env"
echo "   # Edit with your credentials"
echo

echo "4. Encrypt credentials:"
echo "   python -m mjas setup"
echo

echo "5. List available portals:"
echo "   python -m mjas list-portals"
echo

echo "6. Run a test cycle:"
echo "   python -m mjas run --visible --tier 1"
echo

echo "Installation complete!"
echo
echo "Activate the virtual environment with:"
echo "   source .venv/bin/activate"
