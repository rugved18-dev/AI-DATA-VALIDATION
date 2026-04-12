@echo off
REM Quick Start Script for AI Data Validation Backend
REM This script sets up and runs the Flask backend

echo.
echo ========================================
echo AI Data Validation - Backend Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created successfully!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
pip show Flask >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed successfully!
) else (
    echo Dependencies already installed.
)

REM Create uploads directory if it doesn't exist
if not exist "uploads\" (
    echo Creating uploads directory...
    mkdir uploads
)

REM Run the Flask app
echo.
echo ========================================
echo Starting Flask Backend...
echo ========================================
echo.
echo The server will run at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.

python app.py

pause
