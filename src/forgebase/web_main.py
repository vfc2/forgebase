"""Standalone web application entry point."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "forgebase.interfaces.web:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload for development
        log_level="info",
    )
