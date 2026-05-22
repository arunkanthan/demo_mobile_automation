#!/bin/bash
# setup.sh - Automated setup script for macOS

set -e

echo "=================================="
echo "Mobile Automation Framework Setup"
echo "=================================="

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python found: $(python3 --version)"

# Check Node.js (for Appium)
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "Node.js not found. Installing with Homebrew..."
    brew install node
fi
echo "✓ Node.js found: $(node --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Copy environment file
echo ""
echo "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file (please configure with your device settings)"
else
    echo "✓ .env file already exists"
fi

# Install Appium if not present
echo ""
echo "Checking Appium installation..."
if ! command -v appium &> /dev/null; then
    echo "Installing Appium..."
    npm install -g appium
    appium driver install uiautomator2
    appium driver install xcuitest
    echo "✓ Appium installed"
else
    echo "✓ Appium found: $(appium --version)"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p reports/allure-results
mkdir -p reports/screenshots
mkdir -p reports/logs
echo "✓ Directories created"

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your device configuration"
echo "2. Start Appium: appium"
echo "3. Run tests: pytest --platform=ios -v"
echo ""
echo "Need help? Check SETUP_GUIDE.md"
