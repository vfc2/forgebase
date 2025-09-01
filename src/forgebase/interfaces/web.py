"""Web interface for the forgebase chat application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

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

    # Add CORS middleware to allow frontend communication
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173",
                       "http://127.0.0.1:5173"],  # React dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @fastapi_app.post("/api/chat/stream")
    async def chat_stream(request: dict):
        """Stream chat response."""
        user_message = request.get("message", "")

        async def generate():
            if _service:
                async for chunk in _service.send_message_stream(user_message):
                    # Format as Server-Sent Events
                    yield f"data: {chunk}\n".encode("utf-8")
                # Send completion marker
                yield "data: [DONE]\n".encode("utf-8")

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("forgebase.interfaces.web:app",
                host="0.0.0.0", port=8000, reload=True)
