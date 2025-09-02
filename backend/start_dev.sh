#!/bin/bash

# Forgebase Backend Development Server
echo "🚀 Starting Forgebase Backend..."

# Activate virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/installed" ]; then
    echo "📦 Installing dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt -r requirements-dev.txt
    touch .venv/installed
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copy .env.sample to .env and configure your settings."
    if [ -f ".env.sample" ]; then
        echo "💡 You can run: cp .env.sample .env"
    fi
    exit 1
fi

echo "🌐 Starting FastAPI server on http://localhost:8000..."
PYTHONPATH=src python src/forgebase/interfaces/web.py