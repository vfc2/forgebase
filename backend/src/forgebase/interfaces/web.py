"""Web interface for the forgebase chat application."""

import os
from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from forgebase.core import chat_service, project_service
from forgebase.core.exceptions import ProjectNotFoundError, ProjectAlreadyExistsError
from forgebase.infrastructure import config, logging_config, project_repository
from forgebase.interfaces import project_models


# Templates/static handling for both new and old directory structures
TEMPLATE_DIR = "frontend"
STATIC_DIR = "frontend/public"

# Check if we're in the new backend-only structure
if not os.path.exists("frontend") and os.path.exists("../frontend"):
    TEMPLATE_DIR = "../frontend"
    STATIC_DIR = "../frontend/public"

templates = Jinja2Templates(directory=TEMPLATE_DIR)
has_index = os.path.exists(os.path.join(TEMPLATE_DIR, "index.html"))

# Global service instance that will be shared across requests
_service: chat_service.ChatService | None = None
_project_service: project_service.ProjectService | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Manage application lifespan - startup and shutdown logic."""
    # Startup: Initialize the chat service and project service
    global _service, _project_service  # pylint: disable=global-statement
    logging_config.setup_logging(debug=False)
    agent = config.get_agent()
    _service = chat_service.ChatService(agent)

    # Initialize project service with in-memory repository
    project_repo = project_repository.InMemoryProjectRepository()
    _project_service = project_service.ProjectService(project_repo)

    yield  # Application runs here

    # Shutdown: Clean up resources if needed
    _service = None
    _project_service = None


def get_cors_origins() -> list[str]:
    """Get CORS origins from environment variable or use defaults."""
    cors_origins_env = os.getenv("CORS_ORIGINS")
    if cors_origins_env:
        return [origin.strip() for origin in cors_origins_env.split(",")]

    # If no environment variable is set, construct defaults from other env vars
    frontend_host = os.getenv("FRONTEND_HOST", "localhost")
    frontend_port = os.getenv("FRONTEND_PORT", "5173")
    frontend_fallback_port = os.getenv("FRONTEND_FALLBACK_PORT", "5174")

    # Build default origins dynamically
    origins = []
    localhost_aliases = [frontend_host]

    # Add 127.0.0.1 alias if frontend_host is localhost
    if frontend_host == "localhost":
        localhost_aliases.append("127.0.0.1")

    for hostname in localhost_aliases:
        for port_num in [frontend_port, frontend_fallback_port]:
            origins.append(f"http://{hostname}:{port_num}")

    return origins


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    fastapi_app = FastAPI(
        title="Forgebase Chat",
        description="Ultra-minimal chat interface over Semantic Kernel",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Add CORS middleware to allow frontend communication
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files (path mocked in tests)
    if os.path.exists(STATIC_DIR):
        fastapi_app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @fastapi_app.get("/")
    async def index(request: Request):
        """Basic index route (templates mocked in tests)."""
        if has_index:
            return templates.TemplateResponse("index.html", {"request": request})
        # Fallback to dev frontend if templates are not present
        frontend_host = os.getenv("FRONTEND_HOST", "localhost")
        frontend_port = os.getenv("FRONTEND_PORT", "5173")
        frontend_url = f"http://{frontend_host}:{frontend_port}"
        accepts_html = "text/html" in (request.headers.get("accept") or "")
        if accepts_html:
            return RedirectResponse(frontend_url, status_code=307)
        return JSONResponse(
            {
                "message": "Frontend assets not found. Use the React dev server.",
                "frontend": frontend_url,
            }
        )

    @fastapi_app.post("/api/chat/stream")
    async def chat_stream(request: dict):
        """Stream chat response."""
        user_message = request.get("message", "")

        async def generate():
            if _service:
                # Recommended SSE headers are set on response; here we just yield the body
                async for chunk in _service.send_message_stream(user_message):
                    # Escape newlines for SSE format
                    escaped_chunk = chunk.replace("\n", "\\n")
                    yield f"data: {escaped_chunk}\n\n".encode("utf-8")
                # Completion marker
                yield b"data: [DONE]\n\n"

        # Proper SSE media type and useful headers
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    @fastapi_app.post("/api/chat/reset")
    async def reset_chat():
        """Reset the chat conversation."""
        if _service:
            await _service.reset()
        return {"status": "reset"}

    @fastapi_app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "forgebase-web"}

    # Project API endpoints
    @fastapi_app.post("/api/projects", response_model=project_models.ProjectResponse)
    async def create_project(request: project_models.ProjectCreateRequest):
        """Create a new project."""
        if not _project_service:
            raise HTTPException(
                status_code=500, detail="Project service not initialized"
            )

        try:
            project = await _project_service.create_project(request.name, request.prd)
            response = project_models.ProjectResponse.model_validate(project)
            return JSONResponse(
                content=response.model_dump(by_alias=True, mode="json"),
                media_type="application/json",
            )
        except ProjectAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @fastapi_app.get(
        "/api/projects", response_model=list[project_models.ProjectResponse]
    )
    async def list_projects():
        """List all projects."""
        if not _project_service:
            raise HTTPException(
                status_code=500, detail="Project service not initialized"
            )

        projects = await _project_service.list_projects()
        responses = [
            project_models.ProjectResponse.model_validate(project)
            for project in projects
        ]
        return JSONResponse(
            content=[r.model_dump(by_alias=True, mode="json") for r in responses],
            media_type="application/json",
        )

    @fastapi_app.put(
        "/api/projects/{project_id}/name", response_model=project_models.ProjectResponse
    )
    async def update_project_name(
        project_id: UUID, request: project_models.ProjectUpdateNameRequest
    ):
        """Update only a project's name."""
        if not _project_service:
            raise HTTPException(
                status_code=500, detail="Project service not initialized"
            )

        try:
            project = await _project_service.update_project(project_id, request.name)
            response = project_models.ProjectResponse.model_validate(project)
            return JSONResponse(
                content=response.model_dump(by_alias=True, mode="json"),
                media_type="application/json",
            )
        except ProjectNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @fastapi_app.put(
        "/api/projects/{project_id}/prd", response_model=project_models.ProjectResponse
    )
    async def update_project_prd(
        project_id: UUID, request: project_models.ProjectUpdatePRDRequest
    ):
        """Update only a project's PRD content."""
        if not _project_service:
            raise HTTPException(
                status_code=500, detail="Project service not initialized"
            )

        try:
            project = await _project_service.update_project_prd(project_id, request.prd)
            response = project_models.ProjectResponse.model_validate(project)
            return JSONResponse(
                content=response.model_dump(by_alias=True, mode="json"),
                media_type="application/json",
            )
        except ProjectNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @fastapi_app.get(
        "/api/projects/{project_id}", response_model=project_models.ProjectResponse
    )
    async def get_project(project_id: UUID):
        """Get a project by ID."""
        if not _project_service:
            raise HTTPException(
                status_code=500, detail="Project service not initialized"
            )

        try:
            project = await _project_service.get_project(project_id)
            response = project_models.ProjectResponse.model_validate(project)
            return JSONResponse(
                content=response.model_dump(by_alias=True, mode="json"),
                media_type="application/json",
            )
        except ProjectNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @fastapi_app.put(
        "/api/projects/{project_id}", response_model=project_models.ProjectResponse
    )
    async def update_project(
        project_id: UUID, request: project_models.ProjectUpdateRequest
    ):
        """Update a project."""
        if not _project_service:
            raise HTTPException(
                status_code=500, detail="Project service not initialized"
            )

        try:
            project = await _project_service.update_project_full(
                project_id, request.name, request.prd
            )
            return project_models.ProjectResponse.model_validate(project)
        except ProjectNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @fastapi_app.delete("/api/projects/{project_id}")
    async def delete_project(project_id: UUID):
        """Delete a project."""
        if not _project_service:
            raise HTTPException(
                status_code=500, detail="Project service not initialized"
            )

        deleted = await _project_service.delete_project(project_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Project not found")

        return {"status": "deleted"}

    return fastapi_app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("FORGEBASE_HOST", "0.0.0.0")
    port = int(os.getenv("FORGEBASE_PORT", "8000"))
    uvicorn.run("forgebase.interfaces.web:app", host=host, port=port, reload=True)
