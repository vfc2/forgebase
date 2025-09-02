---
applyTo: "src/**,tests/**"
---
# Project Overview

Forgebase is a minimal MVP for conversational product requirement document (PRD) generation. It provides a transport-agnostic chat interface over Semantic Kernel with streaming responses, supporting both CLI and web interfaces.

**Goal:** Enable conversational workflows that turn dialogue into structured PRDs and scoped work plans through a simple, extensible architecture.

## Folder Structure

```
/workspaces/forgebase/backend/
├── src/forgebase/         # Python backend (core + interfaces)
│   ├── core/              # Transport-agnostic business logic
│   ├── infrastructure/    # Agent implementations
│   └── interfaces/        # CLI + Web API
│       ├── cli.py         # CLI interface
│       └── web.py         # FastAPI web API
└── tests/                 # Python backend tests
```

## Architecture

### Core Components
* `core/`: Domain logic with no I/O dependencies
  - [`ChatService`](src/forgebase/core/chat_service.py): Main orchestration service
  - [`AgentPort`](src/forgebase/core/ports.py): Protocol defining agent interface (`send_message_stream`, `reset`)

### Infrastructure Layer  
* [`config.py`](src/forgebase/infrastructure/config.py): Environment-based agent selection (Azure OpenAI vs stub)
* [`sk_agent.py`](src/forgebase/infrastructure/sk_agent.py): Semantic Kernel implementation with `ChatCompletionAgent`
* [`stub_agent.py`](src/forgebase/infrastructure/stub_agent.py): Mock implementation for testing

### Interface Layer
* [`cli.py`](src/forgebase/interfaces/cli.py): Click-based CLI with streaming output
* [`web.py`](src/forgebase/interfaces/web.py): FastAPI app with `/api/chat/stream` endpoint
* `frontend/`: React SPA that consumes the web API

## Key Patterns

* **Async streaming**: All message flows use `AsyncIterator[str]` for real-time responses
* **Port/adapter**: Core logic isolated through `AgentPort` protocol
* **Configuration-driven**: Agent selection via environment variables (Azure OpenAI or stub)
* **Transport-agnostic**: Same `ChatService` powers CLI and web interfaces
* **Frontend separation**: React app is independent, calls FastAPI endpoints

## Development Setup

**Required tools:** Python 3.12, semantic-kernel, FastAPI for web interface

**Quality gates (must pass):**
```bash
python -m black src tests
python -m pylint src tests
python -m mypy src
python -m pytest tests
```

**Run interfaces:**
- Always use the virtual environment:
  ```bash
  source .venv/bin/activate
  ```
- CLI:
  ```bash
  python -m forgebase.interfaces.cli chat
  ```
- Web API (direct):
  ```bash
  PYTHONPATH=src python src/forgebase/interfaces/web.py
  ```
- Frontend:
  ```bash
  cd frontend && npm run dev
  ```
- Full stack (backend + frontend):
  ```bash
  ./start_dev.sh
  ```

## Coding Standards

* **Simplicity first**: Minimize side-effects and complexity
* **Full type hints**: Especially `AsyncIterator[str]` for streaming
* **Google docstrings**: Every module, class, function
* **No I/O in core/**: Keep domain logic pure
* **Never log secrets**: Especially API keys
* **Async-first design**: Use `asyncio` patterns throughout

## Strict Rules for Agents

- Do not add external dependencies without approval.
- Maintain the streaming contract (see below); do not buffer entire responses.
- Never log secrets; keep configuration via environment variables only.
- No I/O in `core/**`; keep domain logic pure.
- If you change public behavior, add/adjust tests in `tests/**` accordingly.

## Streaming Contract (SSE)

- Endpoint: `POST /api/chat/stream`
- Server emits UTF-8 encoded SSE lines:
  - Data chunks: `data: <payload>\n\n` where `<payload>` has newlines escaped as `\\n`
  - Completion: `data: [DONE]\n\n`
- Client unescapes `\\n` back to `\n` and concatenates chunks in order.