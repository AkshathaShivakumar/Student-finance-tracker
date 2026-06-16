@echo off
REM Windows setup script for Student Finance Tracker
REM Run this script to set up the development environment

echo.
echo ========================================
echo Student Finance Tracker Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Copying environment template...
if not exist .env (
    copy .env.example .env
    echo Created .env file - please edit with your credentials
) else (
    echo .env already exists - skipping
)

echo [5/5] Database initialization...
echo.
echo To initialize the database, run:
echo   python init_db.py
echo.
echo After that, start the application with:
echo   python run.py
echo.
echo The app will be available at: http://localhost:5000
echo.
pause
