"""Shared test fixtures for web interface tests."""

from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_templates():
    """Mock Jinja2Templates for testing."""
    mock = MagicMock()
    mock.TemplateResponse.return_value = MagicMock()
    return mock


@pytest.fixture
def mock_static_files():
    """Mock StaticFiles for testing."""
    return MagicMock()


@pytest.fixture
def mock_agent():
    """Mock agent for testing."""
    mock = MagicMock()

    # Mock the async streaming method
    async def mock_stream(user_text):
        yield "Mock "
        yield "response"

    mock.send_message_stream = mock_stream
    mock.reset.return_value = None
    return mock
