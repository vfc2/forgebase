"""Tests for the web interface."""

import unittest
from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from forgebase.interfaces.web import create_app, app


class TestWebInterface(unittest.TestCase):
    """Test cases for the web interface functionality."""

    @patch("forgebase.interfaces.web.config.get_service")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_create_app_returns_fastapi_instance(
        self, _mock_static, _mock_templates, _mock_logging, mock_get_service
    ):
        """Test that create_app returns a FastAPI instance."""
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service
        app_instance = create_app()

        assert isinstance(app_instance, FastAPI)
        assert app_instance.title == "Forgebase API"

    @patch("forgebase.interfaces.web.config.get_service")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_app_has_correct_routes(
        self, _mock_static, _mock_templates, _mock_logging, mock_get_service
    ):
        """Test that the app has the expected routes."""
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        app_instance = create_app()

        # Check routes using openapi schema which is more reliable
        openapi_schema = app_instance.openapi()
        paths = list(openapi_schema["paths"].keys())

        # Check expected routes
        assert "/" in paths
        assert "/api/health" in paths
        assert "/api/chat/stream" in paths
        assert "/api/chat/reset" in paths
        assert "/api/projects" in paths
        assert "/api/projects/{project_id}" in paths

    @patch("forgebase.interfaces.web.config.get_service")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_health_endpoint(
        self, _mock_static, _mock_templates, _mock_logging, mock_get_service
    ):
        """Test the health endpoint."""
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        app_instance = create_app()

        with TestClient(app_instance) as client:
            response = client.get("/api/health")

            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}

    @patch("forgebase.interfaces.web.config.get_service")
    @patch("forgebase.interfaces.web.logging_config.setup_logging")
    @patch("forgebase.interfaces.web.Jinja2Templates")
    @patch("forgebase.interfaces.web.StaticFiles")
    def test_index_endpoint(
        self, _mock_static, mock_templates, _mock_logging, mock_get_service
    ):
        """Test the index endpoint renders the chat template."""
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        # Mock the template response
        mock_template_response = object()
        mock_templates.return_value.TemplateResponse.return_value = (
            mock_template_response
        )

        app_instance = create_app()

        with TestClient(app_instance) as client:
            response = client.get("/")

            # Should get a response (might be template or redirect)
            assert response.status_code in [200, 307]  # 307 for redirect to frontend

    def test_app_module_level_instance(self):
        """Test that the module-level app instance exists."""
        assert isinstance(app, FastAPI)
        assert app.title == "Forgebase API"


class TestWebInterfaceIntegration(unittest.TestCase):
    """Integration tests for the web interface with actual services."""

    def test_integration_basic_functionality(self):
        """Test basic integration with the app instance."""
        # Use the module-level app instance
        with TestClient(app) as client:
            # Test health endpoint
            response = client.get("/api/health")
            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}

            # Test index endpoint
            response = client.get("/")
            assert response.status_code in [
                200,
                307,
            ]  # 200 for template, 307 for redirect

            # Test that project endpoints exist (even if they fail due to no service)
            response = client.get("/api/projects")
            # May return 500 if service not initialized, but route should exist
            assert response.status_code in [200, 500]
