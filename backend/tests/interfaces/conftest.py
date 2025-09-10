"""Shared test fixtures for interface tests."""

import pytest
from forgebase.infrastructure import config


@pytest.fixture(autouse=True)
def reset_repository():
    """Reset the global repository before each test for isolation."""
    config.reset_project_repository()
    yield
    config.reset_project_repository()
