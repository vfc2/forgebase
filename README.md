# forgebase

Ultra-minimal, async, transport-agnostic chat boundary over Semantic Kernel that streams replies.

## Quickstart

1.  **Install Python 3.12** and create a virtual environment:
    ```bash
    python3.12 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt -r requirements-dev.txt
    ```

3.  **Configure environment:**
    Copy `.env.sample` to `.env` and fill in your Azure OpenAI details.
    ```bash
    cp .env.sample .env
    ```

4.  **Run the CLI:**
    ```bash
    python -m forgebase.interfaces.cli chat
    ```

5.  **Or run the Web Interface:**
    ```bash
    # Quick start
    ./start_web.sh
    
    # Or manually
    PYTHONPATH=src python src/forgebase/web_main.py
    
    # Then open http://localhost:8000
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

- Use VS Code: Run "Debug Web Interface" configuration (F5)
- Or command line: `./start_web.sh`
- Auto-reload enabled for development
- Available at http://localhost:8000

## Future Web Integration

The core `ChatService` is designed to be transport-agnostic. The web interface demonstrates how it can be used in any async web framework to stream responses in real-time.
