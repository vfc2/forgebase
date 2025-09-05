# Forgebase Backend

Ultra-minimal, async, transport-agnostic chat boundary over Semantic Kernel that streams replies.

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

### API Endpoints

#### Chat
- `GET /` - Web interface
- `POST /api/chat/stream` - Chat endpoint with streaming responses
- `GET /health` - Health check

#### Project Management
- `POST /api/projects` - Create new project
- `GET /api/projects` - List all projects (newest first)
- `GET /api/projects/{id}` - Get project by ID
- `PUT /api/projects/{id}` - Update project name
- `DELETE /api/projects/{id}` - Delete project

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
├── core/           # Core business logic
├── infrastructure/ # External integrations
├── interfaces/     # CLI, web, and other interfaces
└── prompts/        # AI prompts and templates
```