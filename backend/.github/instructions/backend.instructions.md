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
  - [`ProjectService`](src/forgebase/core/project_service.py): Project management service
  - [`AgentPort`](src/forgebase/core/ports.py): Protocol defining agent interface (`send_message_stream`, `reset`)
  - [`ProjectRepositoryPort`](src/forgebase/core/ports.py): Protocol defining project persistence interface
  - [`Project`](src/forgebase/core/entities.py): Project entity (ID, name, timestamps)

### Infrastructure Layer  
* [`config.py`](src/forgebase/infrastructure/config.py): Environment-based agent selection (Azure OpenAI vs stub)
* [`sk_agent.py`](src/forgebase/infrastructure/sk_agent.py): Semantic Kernel implementation with `ChatCompletionAgent`
* [`stub_agent.py`](src/forgebase/infrastructure/stub_agent.py): Mock implementation for testing
* [`project_repository.py`](src/forgebase/infrastructure/project_repository.py): In-memory project storage (extensible to database)

### Interface Layer
* [`cli.py`](src/forgebase/interfaces/cli.py): Click-based CLI with streaming output
* [`web.py`](src/forgebase/interfaces/web.py): FastAPI app with chat streaming + project CRUD endpoints
* [`project_models.py`](src/forgebase/interfaces/project_models.py): Pydantic models for project API
* `frontend/`: React SPA that consumes the web API

## Key Patterns

* **Async streaming**: All message flows use `AsyncIterator[str]` for real-time responses
* **Port/adapter**: Core logic isolated through `AgentPort` and `ProjectRepositoryPort` protocols
* **Repository pattern**: Project persistence abstracted for easy database integration later
* **Configuration-driven**: Agent selection via environment variables (Azure OpenAI or stub)
* **Transport-agnostic**: Same services power CLI and web interfaces
* **Frontend separation**: React app is independent, calls FastAPI endpoints

## Development Setup

**Required tools:** Python 3.12, semantic-kernel, FastAPI for web interface, pydantic for validation

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

## Project Management API

- `POST /api/projects` - Create project
- `GET /api/projects` - List projects (newest first)  
- `GET /api/projects/{id}` - Get project by ID
- `PUT /api/projects/{id}` - Update project name
- `DELETE /api/projects/{id}` - Delete project
- Uses Pydantic models for validation, repository pattern for persistence