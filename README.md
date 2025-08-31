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

## Development

This project uses `black`, `pylint`, and `mypy` for code quality.

*   **Format code:** `black .`
*   **Lint code:** `pylint src tests`
*   **Type-check:** `mypy src`
*   **Run tests:** `pytest`

```bash
python -m black src tests && python -m pylint src tests && python -m mypy src && python -m pytest tests
```

## Future Web Integration

The core `ChatService` is designed to be transport-agnostic. It can be used in any async web framework (e.g., FastAPI, Starlette) to stream responses via Server-Sent Events (SSE) or WebSockets. See `forgebase/interfaces/hooks.py` for placeholders.
