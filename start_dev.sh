#!/bin/bash
set -e

echo "Starting Forgebase dev (backend + frontend)..."

# Kill existing ports if lsof exists (optional)
if command -v lsof &>/dev/null; then
  for p in 8000 5173; do
    PIDS=$(lsof -ti:$p 2>/dev/null || true)
    if [ -n "$PIDS" ]; then echo "Killing PIDs on :$p"; echo "$PIDS" | xargs kill -9 || true; fi
  done
fi

# Start backend
pushd backend >/dev/null
./start_dev.sh &
BACKEND_PID=$!
popd >/dev/null

# Start frontend
pushd frontend >/dev/null
./start_dev.sh &
FRONTEND_PID=$!
popd >/dev/null

trap 'echo; echo "Shutting down..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; wait' INT TERM
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
wait $BACKEND_PID $FRONTEND_PID