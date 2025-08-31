"""Web interface for the forgebase chat application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from forgebase.core import chat_service
from forgebase.infrastructure import config, logging_config


# Global service instance that will be shared across requests
_service: chat_service.ChatService | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Manage application lifespan - startup and shutdown logic."""
    # Startup: Initialize the chat service
    global _service  # pylint: disable=global-statement
    logging_config.setup_logging(debug=False)
    agent = config.get_agent()
    _service = chat_service.ChatService(agent)

    yield  # Application runs here

    # Shutdown: Clean up resources if needed
    _service = None


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    fastapi_app = FastAPI(
        title="Forgebase Chat",
        description="Ultra-minimal chat interface over Semantic Kernel",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Setup templates and static files
    templates = Jinja2Templates(directory="src/forgebase/web/templates")
    fastapi_app.mount(
        "/static", StaticFiles(directory="src/forgebase/web/static"), name="static"
    )

    @fastapi_app.get("/")
    async def index(request: Request):
        """Serve the chat interface."""
        return templates.TemplateResponse("chat.html", {"request": request})

    @fastapi_app.post("/api/chat/stream")
    async def chat_stream(request: dict):
        """Stream chat response."""
        user_message = request.get("message", "")

        async def generate():
            if _service:
                async for chunk in _service.send_message_stream(user_message):
                    yield chunk.encode("utf-8")
                # Add a newline at the end like CLI does
                yield "\n".encode("utf-8")

        return StreamingResponse(generate(), media_type="text/plain")

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

    return fastapi_app


# Create the app instance
app = create_app()
