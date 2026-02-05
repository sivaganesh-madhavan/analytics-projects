@echo off
REM Quick Start - Informatica Launcher
REM This script installs dependencies and launches the app

echo ========================================
echo Informatica Quick Launcher - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

REM Install dependencies
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies may have failed to install
    echo The launcher may still work, but some features might not be available
    echo.
)

echo.
echo ========================================
echo Setup complete! Launching application...
echo ========================================
echo.

REM Launch the application
python launcher.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start launcher
    echo Please check the error messages above
    echo.
    pause
)
