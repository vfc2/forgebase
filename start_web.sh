#!/bin/bash
# Quick script to start the Forgebase web interface

cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)/src"

echo "🚀 Starting Forgebase Web Interface..."
echo "Open your browser to: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

.venv/bin/python src/forgebase/web_main.py
