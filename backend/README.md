# Forgebase Backend

Conversational PRD generation with tool-enabled AI agents. Provides transport-agnostic chat interface over Semantic Kernel with streaming responses and intelligent tool calling.

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```

3. **Configure environment:**
   Copy `.env.sample` to `.env` and fill in your Azure OpenAI details.
   ```bash
   cp .env.sample .env
   ```

## Development

### Running the Backend

```bash
# Quick start
./start_dev.sh

# Or manually
source .venv/bin/activate
PYTHONPATH=src python src/forgebase/interfaces/web.py
```

The backend will be available at http://localhost:8000

## API Endpoints

### Chat Interface

#### Stream Chat
- **POST** `/api/chat/stream`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "message": "string",
    "projectId": "uuid (optional)"
  }
  ```
- **Response:** Server-Sent Events (SSE)
  - Data chunks: `data: <content>\n\n`
  - Completion: `data: [DONE]\n\n`
- **Description:** Stream conversational responses with tool calling capability. When `projectId` is provided, agent can save PRD content to that project.

### Project Management

#### Create Project
- **POST** `/api/projects`
- **Request Body:**
  ```json
  {
    "name": "string",
    "prd": "string (optional)"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "id": "uuid",
    "name": "string",
    "prd": "string|null",
    "createdAt": "ISO datetime",
    "updatedAt": "ISO datetime|null"
  }
  ```

#### List Projects
- **GET** `/api/projects`
- **Response:** `200 OK`
  ```json
  [
    {
      "id": "uuid",
      "name": "string", 
      "prd": "string|null",
      "createdAt": "ISO datetime",
      "updatedAt": "ISO datetime|null"
    }
  ]
  ```
- **Description:** Returns projects sorted by creation date (newest first)

#### Get Project
- **GET** `/api/projects/{id}`
- **Response:** `200 OK` or `404 Not Found`
  ```json
  {
    "id": "uuid",
    "name": "string",
    "prd": "string|null", 
    "createdAt": "ISO datetime",
    "updatedAt": "ISO datetime|null"
  }
  ```

#### Update Project
- **PATCH** `/api/projects/{id}`
- **Request Body:**
  ```json
  {
    "name": "string (optional)",
    "prd": "string (optional)"
  }
  ```
- **Response:** `200 OK` or `404 Not Found`
- **Description:** Partially update project name and/or PRD content. Agent tools use this to save PRD content.

#### Delete Project
- **DELETE** `/api/projects/{id}`
- **Response:** `204 No Content` or `404 Not Found`

### System Endpoints

#### Health Check
- **GET** `/health`
- **Response:** `200 OK`
  ```json
  {
    "status": "healthy"
  }
  ```

#### Web Interface
- **GET** `/`
- **Response:** HTML page for basic web interface

## Architecture

### Tool-Enabled Agents
- Agents use Semantic Kernel plugins for tool calling
- Current tools:
  - `PRDTools.update_prd()`: Save PRD content to projects
- Project context flows from chat requests to agent tools
- Tools are automatically registered with agents via dependency injection

### Split Service Architecture
- **ChatService**: Handles conversations and streaming with project context
- **ProjectService**: Manages CRUD operations and validation
- **AgentPort**: Protocol for AI agents with tool support
- **ToolPort**: Protocol for agent tools/plugins

### CLI Interface

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run CLI
python -m forgebase.interfaces.cli chat
```

### Code Quality

```bash
# Format code
black src tests

# Lint code  
pylint src tests

# Type check
mypy src

# Run tests
pytest
```

### Project Structure

```
src/forgebase/
├── core/           # Domain logic (ChatService, ProjectService, ports)
├── infrastructure/ # Agent implementations and configuration
├── interfaces/     # CLI, web API
├── tools/          # Agent tools and plugins
└── prompts/        # AI prompts and templates
```

## Tool Calling Flow

1. Frontend sends chat message with optional `projectId`
2. ChatService initializes agent with project context
3. Agent processes message and may decide to call tools
4. Tools (e.g., `update_prd`) perform actions using project context
5. Agent streams response including tool execution results