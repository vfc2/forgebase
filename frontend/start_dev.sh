#!/bin/bash

# Forgebase Frontend Development Server
echo "🚀 Starting Forgebase Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "🌐 Starting Vite dev server on http://localhost:5173..."
npm run dev