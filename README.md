# forgebase

Ultra-minimal, async, transport-agnostic chat boundary over Semantic Kernel that streams replies.

## Quickstart

Backend and frontend now live in separate folders.

1) Backend (FastAPI)
```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
# Optional Azure config
cp .env.sample .env  # then edit values

# Run the web API
PYTHONPATH=src python src/forgebase/interfaces/web.py
```

2) Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```

3) Run both from repo root
```bash
./start_dev.sh
# Backend:  http://localhost:8000
# Frontend: http://localhost:5173
```

## Development

This project uses `black`, `pylint`, and `mypy` for code quality.

*   **Format code:** `black .`
*   **Lint code:** `pylint src tests`
*   **Type-check:** `mypy src`
*   **Run tests:** `pytest`

```bash
python -m black src tests && python -m pylint src tests && python -m mypy src && python -m pytest tests
```

## Web Interface

Forgebase includes a clean, minimal web interface built with FastAPI:

- **Real-time streaming** responses via HTTP streaming
- **Professional separation** of HTML, CSS, and JavaScript
- **Zero architecture changes** - reuses the same `ChatService`
- **Docker-friendly** development with auto-reload
- **VS Code debugging** support

### Development

- Auto-reload enabled for development
- Available at http://localhost:8000

## Future Web Integration

The core `ChatService` is designed to be transport-agnostic. The web interface demonstrates how it can be used in any async web framework to stream responses in real-time.
