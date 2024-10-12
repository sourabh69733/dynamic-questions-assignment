#!/bin/bash

# Exit script on error
set -e

# Function to install dependencies and set up the environment
setup_environment() {
    echo "Setting up the environment..."

    # Create a Python virtual environment
    if command -v python3 &>/dev/null; then
        python3 -m venv venv
    elif command -v python &>/dev/null; then
        python -m venv venv
    else
        echo "Python is not installed. Please install Python and try again."
        exit 1
    fi

    # Activate the virtual environment
    source venv/bin/activate

    # Upgrade pip
    pip install --upgrade pip

    # Install dependencies
    pip install -r requirements.txt


    echo "Dependencies installed."

    # Run FastAPI server for production
    echo "Starting FastAPI server..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

    echo "FastAPI server is running at http://0.0.0.0:8000"
}

# Check operating system and execute setup
case "$(uname -s)" in
    Darwin)
        echo "Detected macOS"
        setup_environment
        ;;
    Linux)
        echo "Detected Linux"
        setup_environment
        ;;
    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        echo "Detected Windows"
        # Use PowerShell commands for Windows
        powershell -Command "python -m venv venv; .\venv\Scripts\Activate.ps1; pip install --upgrade pip; pip install fastapi uvicorn[standard] requests beautifulsoup4 pytest; uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
        ;;
    *)
        echo "Unsupported OS"
        exit 1
        ;;
esac
