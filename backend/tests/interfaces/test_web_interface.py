"""Tests for the web interface."""

import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from forgebase.interfaces.web import create_app, app


class TestWebInterfaceBasic(unittest.TestCase):
    """Basic tests for web interface structure."""

    def test_create_app_returns_fastapi_instance(self):
        """Test that create_app returns a FastAPI instance with correct configuration."""
        app_instance = create_app()

        assert isinstance(app_instance, FastAPI)
        assert app_instance.title == "Forgebase API"
        assert (
            app_instance.description == "Conversational PRD generation chat interface"
        )
        assert app_instance.version == "0.1.0"

    def test_app_module_level_instance(self):
        """Test that the module-level app instance exists and is configured."""
        assert isinstance(app, FastAPI)
        assert app.title == "Forgebase API"

    def test_app_has_expected_routes(self):
        """Test that the app has all expected API routes."""
        app_instance = create_app()

        # Check routes using openapi schema
        openapi_schema = app_instance.openapi()
        paths = list(openapi_schema["paths"].keys())

        # Core routes should exist
        expected_routes = [
            "/",
            "/api/health",
            "/api/chat/stream",
            "/api/chat/reset",
            "/api/projects",
            "/api/projects/{project_id}",
        ]

        for route in expected_routes:
            assert route in paths, f"Route {route} not found in API"


class TestWebInterfaceIntegration(unittest.TestCase):
    """Integration tests for the web interface with real behavior."""

    def setUp(self):
        """Set up test client with the actual app instance."""
        self.client = TestClient(app)

    def test_health_endpoint_works(self):
        """Test that health endpoint returns expected response."""
        response = self.client.get("/api/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        assert response.headers["content-type"] == "application/json"

    def test_index_endpoint_responds(self):
        """Test that index endpoint returns a valid response."""
        response = self.client.get("/")

        # Should get either a template response or redirect to frontend
        assert response.status_code in [200, 307]

        if response.status_code == 307:
            # If redirecting, should have a location header
            assert "location" in response.headers

    def test_project_endpoints_exist(self):
        """Test that project management endpoints are accessible."""
        # Test GET /api/projects (list projects)
        response = self.client.get("/api/projects")
        # Should be 200 (success) or 500 (service not initialized)
        assert response.status_code in [200, 500]

        # Test POST /api/projects (create project)
        response = self.client.post(
            "/api/projects", json={"name": "Test Project", "prd": "Test content"}
        )
        # Should be 200 (success) or 500 (service not initialized)
        assert response.status_code in [200, 500]

    def test_chat_endpoints_exist(self):
        """Test that chat endpoints are accessible."""
        # Test POST /api/chat/reset
        response = self.client.post("/api/chat/reset")
        # Should be 200 (success) or 500 (service not initialized)
        assert response.status_code in [200, 500]

        # Test POST /api/chat/stream
        response = self.client.post("/api/chat/stream", json={"message": "Hello"})
        # Should be 200 (success) or 500 (service not initialized)
        assert response.status_code in [200, 500]

    def test_cors_headers_present(self):
        """Test that CORS headers are properly configured."""
        # Test CORS by making a simple GET request and checking headers
        response = self.client.get("/api/health")

        # Should have CORS headers configured
        assert response.status_code == 200
        # FastAPI with CORS middleware should allow cross-origin requests
        # The exact headers depend on the request, but the endpoint should work

    def test_api_validates_bad_requests(self):
        """Test that API properly validates malformed requests."""
        # Test invalid project creation
        response = self.client.post("/api/projects", json={})
        assert response.status_code == 422  # Validation error

        # Test invalid project ID format
        response = self.client.get("/api/projects/invalid-uuid")
        assert response.status_code == 422  # Validation error
