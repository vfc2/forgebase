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
    echo "⚠️  No .env file found. Continuing without Azure config (StubAgent)."
    if [ -f ".env.sample" ]; then
        echo "💡 Tip: cp .env.sample .env to configure Azure OpenAI."
    fi
else
    # shellcheck disable=SC2046
    export $(grep -v '^#' .env | xargs) 2>/dev/null || true
fi

echo "🌐 Starting FastAPI server on http://localhost:8000..."
PYTHONPATH=src python src/forgebase/interfaces/web.py