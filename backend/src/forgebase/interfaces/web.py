"""Web interface for the forgebase chat application."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from forgebase.core import chat_service
from forgebase.infrastructure import config, logging_config


# Templates/static handling for both new and old directory structures
template_dir = "frontend"
static_dir = "frontend/public"

# Check if we're in the new backend-only structure
if not os.path.exists("frontend") and os.path.exists("../frontend"):
    template_dir = "../frontend"
    static_dir = "../frontend/public"

templates = Jinja2Templates(directory=template_dir)

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
    if os.path.exists(static_dir):
        fastapi_app.mount(
            "/static", StaticFiles(directory=static_dir), name="static"
        )

    @fastapi_app.get("/")
    async def index(request: Request):
        """Basic index route (templates mocked in tests)."""
        return templates.TemplateResponse("index.html", {"request": request})

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

    return fastapi_app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("FORGEBASE_HOST", "0.0.0.0")
    port = int(os.getenv("FORGEBASE_PORT", "8000"))
    uvicorn.run("forgebase.interfaces.web:app",
                host=host, port=port, reload=True)
