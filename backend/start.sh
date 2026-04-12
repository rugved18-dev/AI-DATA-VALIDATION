#!/bin/bash
# Quick Start Script for AI Data Validation Backend
# This script sets up and runs the Flask backend

echo ""
echo "========================================"
echo "AI Data Validation - Backend Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python3_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $python3_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully!"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Dependencies installed successfully!"
else
    echo "Dependencies already installed."
fi

# Create uploads directory if it doesn't exist
if [ ! -d "uploads" ]; then
    echo "Creating uploads directory..."
    mkdir -p uploads
fi

# Run the Flask app
echo ""
echo "========================================"
echo "Starting Flask Backend..."
echo "========================================"
echo ""
echo "The server will run at: http://localhost:5000"
echo "Press CTRL+C to stop the server"
echo ""

python3 app.py
