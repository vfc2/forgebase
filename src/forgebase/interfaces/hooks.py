"""Placeholders for future web/ASGI integration hooks."""


async def on_startup() -> None:
    """
    Placeholder for logic to run on web server startup.
    """
    # E.g., initialize database connections, load models, etc.
    print("Web server starting up...")


async def on_shutdown() -> None:
    """
    Placeholder for logic to run on web server shutdown.
    """
    # E.g., close database connections, clean up resources.
    print("Web server shutting down...")
