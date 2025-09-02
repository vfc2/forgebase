"""Logging configuration for the application."""

import logging


def setup_logging(debug: bool = False) -> None:
    """
    Configure application-wide logging.

    Args:
        debug: If True, set log level to DEBUG, otherwise WARNING.
    """
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Never log secrets
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
        logging.WARNING
    )
