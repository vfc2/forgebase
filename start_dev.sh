#!/bin/bash

# Forgebase Development Startup Script
# This script starts both the backend (FastAPI) and frontend (Vite) servers

set -e

echo "🚀 Starting Forgebase Development Environment..."

# Kill any existing dev servers
echo "🔍 Checking for existing dev servers..."

# Check if lsof is available
if ! command -v lsof &> /dev/null; then
    echo "⚠️  lsof not found. Skipping port cleanup."
else
    # Kill processes running on port 8000 (FastAPI backend)
    BACKEND_PIDS=$(lsof -ti:8000 2>/dev/null || true)
    if [ ! -z "$BACKEND_PIDS" ]; then
        echo "🔪 Killing existing backend server(s) on port 8000..."
        echo "$BACKEND_PIDS" | xargs kill -9 2>/dev/null || true
        sleep 1
    fi

    # Kill processes running on port 5173 (Vite frontend)
    FRONTEND_PIDS=$(lsof -ti:5173 2>/dev/null || true)
    if [ ! -z "$FRONTEND_PIDS" ]; then
        echo "🔪 Killing existing frontend server(s) on port 5173..."
        echo "$FRONTEND_PIDS" | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
fi

# Also kill any Python processes that might be running the web interface
PYTHON_WEB_PIDS=$(pgrep -f "python.*web.py" 2>/dev/null || true)
if [ ! -z "$PYTHON_WEB_PIDS" ]; then
    echo "🔪 Killing existing Python web processes..."
    echo "$PYTHON_WEB_PIDS" | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Kill any npm/node processes that might be running Vite
NPM_VITE_PIDS=$(pgrep -f "vite" 2>/dev/null || true)
if [ ! -z "$NPM_VITE_PIDS" ]; then
    echo "🔪 Killing existing Vite processes..."
    echo "$NPM_VITE_PIDS" | xargs kill -9 2>/dev/null || true
    sleep 1
fi

echo "✅ Cleanup complete!"

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "🧹 Cleaning up development servers..."
    
    # Kill the specific PIDs we started
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        echo "🔪 Stopped backend server (PID: $BACKEND_PID)"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        echo "🔪 Stopped frontend server (PID: $FRONTEND_PID)"
    fi
    
    # Double-check and kill any remaining processes on our ports
    if command -v lsof &> /dev/null; then
        REMAINING_8000=$(lsof -ti:8000 2>/dev/null || true)
        if [ ! -z "$REMAINING_8000" ]; then
            echo "$REMAINING_8000" | xargs kill -9 2>/dev/null || true
        fi
        
        REMAINING_5173=$(lsof -ti:5173 2>/dev/null || true)
        if [ ! -z "$REMAINING_5173" ]; then
            echo "$REMAINING_5173" | xargs kill -9 2>/dev/null || true
        fi
    fi
    
    echo "✅ Cleanup complete!"
    exit 0
}

# Set up cleanup on script exit
trap cleanup EXIT INT TERM

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating Python virtual environment..."
source .venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please copy .env.sample to .env and configure your API keys."
    exit 1
fi

# Start backend server
echo "🐍 Starting FastAPI backend server on http://localhost:8000..."
cd /workspaces/forgebase
PYTHONPATH=src python src/forgebase/interfaces/web.py &
BACKEND_PID=$!

# Wait for backend to start with better retry logic
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend started successfully!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start after 30 seconds. Check the logs above."
        echo "📋 Backend logs:"
        # Show last few lines of backend process if still running
        if kill -0 $BACKEND_PID 2>/dev/null; then
            echo "Backend process is still running (PID: $BACKEND_PID)"
        else
            echo "Backend process has exited"
        fi
        exit 1
    fi
    echo "   Attempt $i/30: Backend not ready yet, waiting 1 second..."
    sleep 1
done

# Start frontend server
echo "⚛️  Starting React frontend server on http://localhost:5173..."
cd /workspaces/forgebase/frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

echo ""
echo "🎉 Forgebase is ready!"
echo ""
echo "📝 Backend API: http://localhost:8000"
echo "🌐 Frontend App: http://localhost:5173"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for processes to complete
wait $BACKEND_PID $FRONTEND_PID
