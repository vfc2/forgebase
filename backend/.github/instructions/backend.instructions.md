---
applyTo: "src/**,tests/**"
---
# Project Overview

Forgebase is a minimal MVP for conversational product requirement document (PRD) generation. It provides a transport-agnostic chat interface over Semantic Kernel with streaming responses, supporting both CLI and web interfaces. Agents can use tools to save and manage PRDs through conversational workflows.

**Goal:** Enable conversational workflows that turn dialogue into structured PRDs and scoped work plans through a simple, extensible architecture with intelligent tool calling.

## Folder Structure

```
/workspaces/forgebase/backend/
├── src/forgebase/         # Python backend (core + interfaces)
│   ├── core/              # Transport-agnostic business logic
│   ├── infrastructure/    # Agent implementations
│   ├── interfaces/        # CLI + Web API
│   ├── tools/             # Agent tools and plugins
│   └── prompts/           # AI prompts and templates
└── tests/                 # Python backend tests
```

## Architecture

### Core Components
* `core/`: Domain logic with no I/O dependencies
  - [`ChatService`](src/forgebase/core/chat_service.py): Chat orchestration with project context
  - [`ProjectService`](src/forgebase/core/project_service.py): Project CRUD operations and validation
  - [`AgentPort`](src/forgebase/core/ports.py): Protocol defining agent interface with tool support
  - [`ToolPort`](src/forgebase/core/tool_port.py): Protocol for agent tools/plugins
  - [`ProjectRepositoryPort`](src/forgebase/core/ports.py): Protocol defining project persistence interface
  - [`Project`](src/forgebase/core/entities.py): Project entity (ID, name, timestamps, PRD content)

### Infrastructure Layer  
* [`config.py`](src/forgebase/infrastructure/config.py): Environment-based agent selection with tool wiring
* [`agent.py`](src/forgebase/infrastructure/agent.py): Semantic Kernel implementation with tool registration
* [`stub_agent.py`](src/forgebase/infrastructure/stub_agent.py): Mock implementation for testing
* [`project_repository.py`](src/forgebase/infrastructure/project_repository.py): In-memory project storage

### Tools Layer
* [`prd_tools.py`](src/forgebase/tools/prd_tools.py): PRD management tools for agents (save/update PRD content)

### Interface Layer
* [`cli.py`](src/forgebase/interfaces/cli.py): Click-based CLI with streaming output
* [`web.py`](src/forgebase/interfaces/web.py): FastAPI app with chat streaming + project CRUD endpoints
* [`project_models.py`](src/forgebase/interfaces/project_models.py): Pydantic models for project API

## Key Patterns

* **Async streaming**: All message flows use `AsyncIterator[str]` for real-time responses
* **Split services**: ChatService (conversations) and ProjectService (CRUD) follow SRP
* **Tool calling**: Agents use Semantic Kernel plugins to perform actions (save PRDs, etc.)
* **Project context**: ChatService manages current project context for tools
* **Port/adapter**: Core logic isolated through protocols (`AgentPort`, `ToolPort`, `ProjectRepositoryPort`)
* **Repository pattern**: Project persistence abstracted for easy database integration
* **Configuration-driven**: Agent selection and tool wiring via environment variables
* **Transport-agnostic**: Same services power CLI and web interfaces
* **Dependency injection**: FastAPI uses DI for service management
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
* **Tool protocols**: Tools implement `ToolPort` and register with Semantic Kernel
* **Project context**: Tools receive project context through `set_project_context()`
* **RESTful HTTP verbs**: Use PATCH for partial updates, POST for creation, GET for retrieval

## Strict Rules for Agents

- Do not add external dependencies without approval.
- Maintain the streaming contract (see below); do not buffer entire responses.
- Never log secrets; keep configuration via environment variables only.
- No I/O in `core/**`; keep domain logic pure.
- Tools must implement `ToolPort` protocol and be stateless except for project context.
- If you change public behavior, add/adjust tests in `tests/**` accordingly.

## Tool Calling Architecture

- Agents receive tools via constructor and register them with Semantic Kernel
- Tools implement `ToolPort`: `plugin_name`, `register_with_kernel()`, `set_project_context()`
- Project context flows: ChatService → Agent → Tools
- Tools use `@kernel_function` decorator for Semantic Kernel integration
- Current tools: `PRDTools.update_prd()` for saving PRD content to projects

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
- `PATCH /api/projects/{id}` - Partially update project name and/or PRD
- `DELETE /api/projects/{id}` - Delete project
- Uses Pydantic models for validation, repository pattern for persistence
- Project entity includes: `id`, `name`, `prd` (content), `created_at`, `updated_at`
- PATCH semantics: Only provided fields are updated, others remain unchanged