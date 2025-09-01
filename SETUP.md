# Forgebase Application Setup Guide

This guide explains how to run the complete Forgebase application with both backend and frontend.

## Quick Start

### Option 1: Using the Development Script (Recommended)

```bash
# From the project root
./start_dev.sh
```

This script will:
- Start the FastAPI backend on `http://localhost:8000`
- Start the React frontend on `http://localhost:5173`
- Handle cleanup when you press Ctrl+C

### Option 2: Manual Setup

#### 1. Start the Backend (FastAPI + Uvicorn)

```bash
# From project root
cd /workspaces/forgebase
source .venv/bin/activate
PYTHONPATH=src python src/forgebase/interfaces/web.py
```

The backend will be available at:
- API: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`

#### 2. Start the Frontend (React + Vite)

In a new terminal:

```bash
# From project root
cd /workspaces/forgebase/frontend
npm run dev
```

The frontend will be available at:
- Application: `http://localhost:5173`

## Architecture

```
┌─────────────────┐    HTTP/CORS     ┌──────────────────┐
│   React App     │◄────────────────►│   FastAPI API    │
│   (Port 5173)   │                  │   (Port 8000)    │
│                 │                  │                  │
│ • Chat UI       │                  │ • /api/chat/*    │
│ • Markdown      │                  │ • /health        │
│ • Streaming     │                  │ • CORS enabled   │
└─────────────────┘                  └──────────────────┘
                                               │
                                               ▼
                                    ┌──────────────────┐
                                    │   ChatService    │
                                    │                  │
                                    │ • Semantic Kernel│
                                    │ • Azure OpenAI   │
                                    │ • Async Streaming│
                                    └──────────────────┘
```

## API Endpoints

The backend provides these endpoints for the frontend:

- `GET /health` - Health check
- `POST /api/chat/stream` - Streaming chat responses (SSE format)
- `POST /api/chat/reset` - Reset conversation

## Environment Configuration

### Backend (.env)

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_VERSION=2025-04-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
AZURE_OPENAI_API_KEY=your-key
```

### Frontend (frontend/.env)

```bash
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend Issues

1. **Port 8000 already in use:**
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

2. **Virtual environment not activated:**
   ```bash
   source .venv/bin/activate
   ```

3. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Issues

1. **Port 5173 already in use:**
   ```bash
   lsof -ti:5173 | xargs kill -9
   ```

2. **Missing node_modules:**
   ```bash
   cd frontend && npm install
   ```

3. **CORS errors:** The backend includes CORS middleware for localhost:5173

### Communication Issues

1. **Check backend health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check frontend can reach backend:**
   Open browser dev tools and check network requests

3. **Verify CORS configuration:**
   The backend allows requests from localhost:5173

## Development Workflow

1. **Backend changes:** The server will auto-reload (uvicorn --reload)
2. **Frontend changes:** Vite will hot-reload automatically
3. **API changes:** Update both backend endpoints and frontend types
4. **Testing:** Run `npm test` in frontend directory

## Production Deployment

For production:

1. **Backend:** Use proper ASGI server (uvicorn/gunicorn)
2. **Frontend:** Build with `npm run build` and serve static files
3. **Environment:** Set appropriate CORS origins and API URLs
4. **Security:** Enable HTTPS, secure API keys, rate limiting

## Next Steps

- Test the chat functionality end-to-end
- Add authentication if needed
- Implement file uploads
- Add chat history persistence
- Deploy to production environment
