"""Tests for project web API endpoints."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from forgebase.interfaces.web import create_app


class TestProjectAPI:
    """Test cases for the project REST API."""

    @pytest.fixture
    def client(self):
        """Provide a test client for the FastAPI app."""
        app = create_app()
        with TestClient(app) as client:
            yield client

    def test_create_project(self, client):
        """Test creating a project via API."""
        response = client.post("/api/projects", json={"name": "Test Project"})

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Project"
        assert "id" in data
        assert "createdAt" in data
        assert data["updatedAt"] is None

    def test_create_project_invalid_name(self, client):
        """Test creating a project with invalid name."""
        response = client.post("/api/projects", json={"name": ""})

        assert response.status_code == 422

    def test_list_projects_empty(self, client):
        """Test listing projects when none exist."""
        response = client.get("/api/projects")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_projects_multiple(self, client):
        """Test listing multiple projects."""
        # Create projects
        project1_response = client.post("/api/projects", json={"name": "Project 1"})
        project2_response = client.post("/api/projects", json={"name": "Project 2"})

        assert project1_response.status_code == 200
        assert project2_response.status_code == 200

        # List projects
        response = client.get("/api/projects")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Should be ordered by creation date (newest first)
        assert data[0]["name"] == "Project 2"
        assert data[1]["name"] == "Project 1"

    def test_get_project(self, client):
        """Test getting a project by ID."""
        # Create a project
        create_response = client.post("/api/projects", json={"name": "Test Project"})
        created_project = create_response.json()

        # Get the project
        response = client.get(f"/api/projects/{created_project['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data == created_project

    def test_get_project_not_found(self, client):
        """Test getting a non-existent project."""
        non_existent_id = str(uuid4())
        response = client.get(f"/api/projects/{non_existent_id}")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_get_project_invalid_uuid(self, client):
        """Test getting a project with invalid UUID."""
        response = client.get("/api/projects/invalid-uuid")

        assert response.status_code == 422

    def test_update_project(self, client):
        """Test updating a project."""
        # Create a project
        create_response = client.post("/api/projects", json={"name": "Original Name"})
        created_project = create_response.json()

        # Update the project
        response = client.put(
            f"/api/projects/{created_project['id']}", json={"name": "Updated Name"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_project["id"]
        assert data["name"] == "Updated Name"
        assert data["createdAt"] == created_project["createdAt"]
        assert data["updatedAt"] is not None

    def test_update_project_not_found(self, client):
        """Test updating a non-existent project."""
        non_existent_id = str(uuid4())
        response = client.put(
            f"/api/projects/{non_existent_id}", json={"name": "New Name"}
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_project_invalid_name(self, client):
        """Test updating a project with invalid name."""
        # Create a project
        create_response = client.post("/api/projects", json={"name": "Test Project"})
        created_project = create_response.json()

        # Try to update with empty name
        response = client.put(
            f"/api/projects/{created_project['id']}", json={"name": ""}
        )

        assert response.status_code == 422

    def test_delete_project(self, client):
        """Test deleting a project."""
        # Create a project
        create_response = client.post("/api/projects", json={"name": "Test Project"})
        created_project = create_response.json()

        # Delete the project
        response = client.delete(f"/api/projects/{created_project['id']}")

        assert response.status_code == 200
        assert response.json() == {"status": "deleted"}

        # Verify it's gone
        get_response = client.get(f"/api/projects/{created_project['id']}")
        assert get_response.status_code == 404

    def test_delete_project_not_found(self, client):
        """Test deleting a non-existent project."""
        non_existent_id = str(uuid4())
        response = client.delete(f"/api/projects/{non_existent_id}")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_full_crud_workflow(self, client):
        """Test the complete CRUD workflow."""
        # Create
        create_response = client.post("/api/projects", json={"name": "CRUD Test"})
        assert create_response.status_code == 200
        project = create_response.json()

        # Read
        get_response = client.get(f"/api/projects/{project['id']}")
        assert get_response.status_code == 200
        assert get_response.json() == project

        # Update
        update_response = client.put(
            f"/api/projects/{project['id']}", json={"name": "CRUD Test Updated"}
        )
        assert update_response.status_code == 200
        updated_project = update_response.json()
        assert updated_project["name"] == "CRUD Test Updated"
        assert updated_project["updatedAt"] is not None

        # Delete
        delete_response = client.delete(f"/api/projects/{project['id']}")
        assert delete_response.status_code == 200

        # Verify deletion
        final_get_response = client.get(f"/api/projects/{project['id']}")
        assert final_get_response.status_code == 404
