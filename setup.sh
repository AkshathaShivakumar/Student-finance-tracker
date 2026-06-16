#!/bin/bash
# macOS/Linux setup script for Student Finance Tracker
# Run this script to set up the development environment

echo ""
echo "========================================"
echo "Student Finance Tracker Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Copying environment template..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - please edit with your credentials"
else
    echo ".env already exists - skipping"
fi

echo "[5/5] Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your MySQL and OpenAI credentials"
echo "2. Run: python init_db.py"
echo "3. Run: python run.py"
echo ""
echo "The app will be available at: http://localhost:5000"
echo ""
