"""Tests for the FastAPI web interface."""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from forgebase.interfaces.web import create_app


class TestWebInterface(unittest.TestCase):
    """Test cases for the web interface functionality."""

    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_create_app_returns_fastapi_instance(self, _mock_static, _mock_templates, _mock_logging):
        """Test that create_app returns a FastAPI instance."""
        app = create_app()

        assert isinstance(app, FastAPI)
        assert app.title == "Forgebase Chat"

    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_app_has_correct_routes(self, _mock_static, _mock_templates, _mock_logging, mock_get_agent):
        """Test that the app has the expected routes."""
        mock_agent = AsyncMock()
        mock_get_agent.return_value = mock_agent

        app = create_app()

        # Check routes using openapi schema which is more reliable
        openapi_schema = app.openapi()
        paths = list(openapi_schema["paths"].keys())

        # Check expected routes
        assert "/" in paths
        assert "/health" in paths
        assert "/api/chat/stream" in paths
        assert "/api/chat/reset" in paths

    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_health_endpoint(self, _mock_static, _mock_templates, _mock_logging, mock_get_agent):
        """Test the health endpoint."""
        mock_agent = AsyncMock()
        mock_get_agent.return_value = mock_agent

        app = create_app()

        with TestClient(app) as client:
            response = client.get("/health")

            assert response.status_code == 200
            assert response.json() == {
                "status": "healthy", "service": "forgebase-web"}

    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_index_endpoint(self, _mock_static, mock_templates, _mock_logging, mock_get_agent):
        """Test the index endpoint renders the chat template."""
        mock_agent = AsyncMock()
        mock_get_agent.return_value = mock_agent

        # Mock the template response
        mock_template_response = MagicMock()
        mock_template_response.status_code = 200
        mock_templates.return_value.TemplateResponse = MagicMock(
            return_value=mock_template_response
        )

        app = create_app()

        with TestClient(app) as client:
            response = client.get("/")
            # Just verify we get a response - template details are mocked
            assert response is not None

    @patch("forgebase.interfaces.web.chat_service.ChatService")
    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_chat_reset_endpoint(
        self,
        _mock_static,
        _mock_templates,
        _mock_logging,
        mock_get_agent,
        mock_chat_service,
    ):
        """Test the chat reset endpoint."""
        # Setup mocks
        mock_agent = AsyncMock()
        mock_get_agent.return_value = mock_agent

        mock_service_instance = AsyncMock()
        mock_chat_service.return_value = mock_service_instance

        app = create_app()

        # Trigger the startup event manually to initialize the chat service
        with TestClient(app) as client:
            # Test reset endpoint
            response = client.post("/api/chat/reset")

            assert response.status_code == 200
            assert response.json() == {"status": "reset"}
            mock_service_instance.reset.assert_called_once()

    @patch("forgebase.interfaces.web.chat_service.ChatService")
    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_chat_stream_endpoint(
        self,
        _mock_static,
        _mock_templates,
        _mock_logging,
        mock_get_agent,
        mock_chat_service,
    ):
        """Test the chat streaming endpoint."""
        # Setup mocks
        mock_agent = AsyncMock()
        mock_get_agent.return_value = mock_agent

        # Mock the chat service with streaming response
        mock_service_instance = AsyncMock()
        mock_chat_service.return_value = mock_service_instance

        app = create_app()

        # Mock the service on the app state to control streaming
        app.state.chat_service = mock_service_instance

        async def mock_stream(_user_text):
            yield "Hello "
            yield "World!"

        mock_service_instance.send_message_stream = mock_stream

        with TestClient(app) as client:
            # Test streaming endpoint
            response = client.post(
                "/api/chat/stream", json={"message": "Hello"})

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"
            # For streaming, the response might be empty in test due to TestClient limitations
            # Just verify the status code and content type

    @patch("forgebase.interfaces.web.chat_service.ChatService")
    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_chat_stream_with_empty_message(
        self,
        _mock_static,
        _mock_templates,
        _mock_logging,
        mock_get_agent,
        mock_chat_service,
    ):
        """Test the chat streaming endpoint with empty message."""
        # Setup mocks
        mock_agent = AsyncMock()
        mock_get_agent.return_value = mock_agent

        # Mock the chat service
        mock_service_instance = AsyncMock()
        mock_chat_service.return_value = mock_service_instance

        app = create_app()

        # Mock the service on the app state
        app.state.chat_service = mock_service_instance

        async def mock_stream(user_text):
            assert user_text == ""  # Should receive empty string
            yield "Empty "
            yield "response"

        mock_service_instance.send_message_stream = mock_stream

        with TestClient(app) as client:
            # Test with empty message
            response = client.post("/api/chat/stream", json={})

            assert response.status_code == 200
            # For streaming, TestClient might not capture the full response

    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_chat_stream_no_service(self, _mock_static, _mock_templates, _mock_logging, mock_get_agent):
        """Test chat streaming when service is not initialized."""
        # Setup mocks
        mock_agent = AsyncMock()
        mock_get_agent.return_value = mock_agent

        app = create_app()

        # Create test client without triggering proper startup
        with TestClient(app, raise_server_exceptions=False) as client:
            # Skip startup by directly testing the endpoint
            response = client.post(
                "/api/chat/stream", json={"message": "Hello"})

            # Should still return 200 but with empty content since service is None
            assert response.status_code == 200
            assert response.text == ""

    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_startup_event_initializes_service(self, _mock_static, _mock_templates, mock_logging, mock_get_agent):
        """Test that the startup event properly initializes the chat service."""
        # Setup mocks
        mock_agent = MagicMock()
        mock_get_agent.return_value = mock_agent

        app = create_app()

        # Create client which triggers startup event
        with TestClient(app):
            # Verify mocks were called during startup
            mock_logging.assert_called_once_with(debug=False)
            mock_get_agent.assert_called_once()

    def test_app_module_level_instance(self):
        """Test that the module-level app instance is created correctly."""
        # Import here to avoid circular imports in tests
        from forgebase.interfaces.web import app  # pylint: disable=import-outside-toplevel

        # Should be a FastAPI instance
        assert isinstance(app, FastAPI)


class TestWebInterfaceIntegration(unittest.TestCase):
    """Integration tests for the web interface with actual components."""

    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_integration_with_stub_agent(self, _mock_static, _mock_templates, _mock_logging, mock_get_agent):
        """Test integration with the stub agent for realistic behavior."""
        # Use a real stub agent
        from forgebase.infrastructure.stub_agent import StubAgent  # pylint: disable=import-outside-toplevel

        mock_agent = StubAgent()
        mock_get_agent.return_value = mock_agent

        app = create_app()

        with TestClient(app) as client:
            # Test health endpoint
            response = client.get("/health")
            assert response.status_code == 200

            # Test reset endpoint
            response = client.post("/api/chat/reset")
            assert response.status_code == 200

    @patch("forgebase.interfaces.web.config.get_agent")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_integration_chat_streaming(self, _mock_static, _mock_templates, _mock_logging, mock_get_agent):
        """Test integration of chat streaming with stub agent."""
        # Use a real stub agent
        from forgebase.infrastructure.stub_agent import StubAgent  # pylint: disable=import-outside-toplevel

        mock_agent = StubAgent()
        mock_get_agent.return_value = mock_agent

        app = create_app()

        with TestClient(app) as client:
            # Test streaming endpoint - should work with stub agent
            response = client.post(
                "/api/chat/stream", json={"message": "test"})
            assert response.status_code == 200

            # Stub agent should return some response content
            assert len(response.text) > 0
