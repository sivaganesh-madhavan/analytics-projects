@echo off
REM Informatica Launcher - Quick Start Script
REM Double-click this file to launch the application

echo Starting Informatica Launcher...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Launch the application
cd /d "%~dp0"
python launcher.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start launcher
    echo.
    pause
)
