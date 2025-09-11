"""Web interface for the forgebase chat application."""

import logging
import os
from contextlib import asynccontextmanager
from typing import Any, cast
from uuid import UUID

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from forgebase.core.chat_service import ChatService
from forgebase.core.project_service import ProjectService
from forgebase.core.exceptions import ProjectNotFoundError, ProjectAlreadyExistsError
from forgebase.infrastructure import config, logging_config
from forgebase.interfaces import project_models
from forgebase.interfaces.project_models import ChatStreamRequest

# Temporary test user ID - will be replaced with proper authentication later
TEST_USER_ID = "test-user-123"

# Set up a logger for our endpoint logging
logger = logging.getLogger("forgebase.api")
logger.setLevel(logging.INFO)

# Add a console handler if none exists
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:     %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False


TEMPLATE_DIR = "../frontend"
STATIC_DIR = "../frontend/public"

templates = Jinja2Templates(directory=TEMPLATE_DIR)
has_index = os.path.exists(os.path.join(TEMPLATE_DIR, "index.html"))


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Application lifespan context.

    Initializes the services and stores them on ``app.state``. This avoids hidden
    globals, improves test isolation, and allows multiple app instances.
    """
    logging_config.setup_logging(debug=False)
    fastapi_app.state.chat_service = config.get_chat_service()
    fastapi_app.state.project_service = config.get_project_service()
    try:
        yield
    finally:
        fastapi_app.state.chat_service = None
        fastapi_app.state.project_service = None


def get_chat_service(request: Request) -> ChatService:
    """Dependency to retrieve the chat service from application state."""
    service = getattr(request.app.state, "chat_service", None)
    if service is None:
        raise HTTPException(
            status_code=500, detail="Chat service not initialized")
    return service  # type: ignore[no-any-return]


def get_project_service(request: Request) -> ProjectService:
    """Dependency to retrieve the project service from application state."""
    service = getattr(request.app.state, "project_service", None)
    if service is None:
        raise HTTPException(
            status_code=500, detail="Project service not initialized")
    return service  # type: ignore[no-any-return]


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
        title="Forgebase API",
        description="Conversational PRD generation chat interface",
        version="0.1.0",
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
        fastapi_app.mount(
            "/static", StaticFiles(directory=STATIC_DIR), name="static")

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

    @fastapi_app.get("/api/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}

    @fastapi_app.post("/api/chat/stream")
    async def chat_stream(
        request: ChatStreamRequest,
        chat_service: ChatService = Depends(get_chat_service),
    ):
        """Stream chat response with optional project context."""
        # Debug logging
        print(
            f"DEBUG: Received project_id: {request.project_id} (type: {type(request.project_id)})")

        # Set project context if provided
        if request.project_id:
            project_id_str = str(request.project_id)
            print(f"DEBUG: Setting project context to: {project_id_str}")
            chat_service.set_project_context(project_id_str)

        async def generate():
            async for chunk in chat_service.send_message_stream(request.message):
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
    async def reset_chat(chat_service: ChatService = Depends(get_chat_service)):
        """Reset the chat conversation."""
        await chat_service.reset_chat()
        return {"status": "reset"}

    # Project management endpoints
    def _project_to_payload(project_models_module, project) -> dict[str, Any]:
        """Serialize project with camelCase field names."""
        resp = project_models_module.ProjectResponse.model_validate(project)
        return cast(
            dict[str, Any], resp.model_dump(mode="json", by_alias=True)
        )  # type: ignore[no-any-return]

    @fastapi_app.post("/api/projects", response_model=project_models.ProjectResponse)
    async def create_project(
        request: project_models.ProjectCreateRequest,
        project_service: ProjectService = Depends(get_project_service),
    ):
        """Create a new project."""
        logger.info(
            "CREATE_PROJECT: user_id=%s, project_name=%s", TEST_USER_ID, request.name)
        try:
            project = await project_service.create_project(TEST_USER_ID, request.name, request.prd)
            logger.info(
                "CREATE_PROJECT_SUCCESS: user_id=%s, project_id=%s", TEST_USER_ID, project.id)
            return JSONResponse(content=_project_to_payload(project_models, project))
        except ProjectAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @fastapi_app.get(
        "/api/projects", response_model=list[project_models.ProjectResponse]
    )
    async def list_projects(
        project_service: ProjectService = Depends(get_project_service),
    ):
        """List all projects."""
        logger.info("LIST_PROJECTS: user_id=%s", TEST_USER_ID)
        projects = await project_service.list_projects(TEST_USER_ID)
        logger.info(
            "LIST_PROJECTS_SUCCESS: user_id=%s, count=%s", TEST_USER_ID, len(projects))
        return JSONResponse(
            content=[_project_to_payload(project_models, p) for p in projects]
        )

    @fastapi_app.get(
        "/api/projects/{project_id}", response_model=project_models.ProjectResponse
    )
    async def get_project(
        project_id: UUID, project_service: ProjectService = Depends(get_project_service)
    ):
        """Get a project by ID."""
        logger.info(
            "GET_PROJECT: user_id=%s, project_id=%s", TEST_USER_ID, project_id)
        try:
            project = await project_service.get_project(str(project_id), TEST_USER_ID)
            logger.info(
                "GET_PROJECT_SUCCESS: user_id=%s, project_id=%s", TEST_USER_ID, project_id)
            return JSONResponse(content=_project_to_payload(project_models, project))
        except ProjectNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @fastapi_app.patch(
        "/api/projects/{project_id}", response_model=project_models.ProjectResponse
    )
    async def update_project_partial(
        project_id: UUID,
        request: project_models.ProjectUpdateRequest,
        project_service: ProjectService = Depends(get_project_service),
    ):
        """Partially update a project (name and/or PRD)."""
        logger.info(
            "UPDATE_PROJECT: user_id=%s, project_id=%s", TEST_USER_ID, project_id)
        try:
            project = await project_service.update_project(
                str(project_id), TEST_USER_ID, name=request.name, prd=request.prd
            )
            logger.info(
                "UPDATE_PROJECT_SUCCESS: user_id=%s, project_id=%s", TEST_USER_ID, project_id)
            return JSONResponse(content=_project_to_payload(project_models, project))
        except ProjectNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @fastapi_app.delete("/api/projects/{project_id}")
    async def delete_project(
        project_id: UUID, project_service: ProjectService = Depends(get_project_service)
    ):
        """Delete a project."""
        logger.info(
            "DELETE_PROJECT: user_id=%s, project_id=%s", TEST_USER_ID, project_id)
        deleted = await project_service.delete_project(str(project_id), TEST_USER_ID)
        if deleted:
            logger.info(
                "DELETE_PROJECT_SUCCESS: user_id=%s, project_id=%s", TEST_USER_ID, project_id)
            return {"status": "deleted"}
        logger.info(
            "DELETE_PROJECT_NOT_FOUND: user_id=%s, project_id=%s", TEST_USER_ID, project_id)
        raise HTTPException(status_code=404, detail="Project not found")

    return fastapi_app


# Create the global app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("forgebase.interfaces.web:app",
                host="0.0.0.0", port=8000, reload=True)
