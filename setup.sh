#!/bin/bash

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    pip install uv
fi

# Create virtual environment
echo "Creating virtual environment with uv..."
uv venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies with uv..."
uv pip install -r pyproject.toml

echo "Setup complete! You can now run the application with:"
echo "uvicorn main:app --reload" 