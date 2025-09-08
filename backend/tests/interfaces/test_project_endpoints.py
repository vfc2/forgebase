"""Tests for project API endpoints."""

from uuid import uuid4, UUID
import pytest

from fastapi.testclient import TestClient

from forgebase.interfaces.web import create_app


class TestProjectAPI:
    """Test cases for the project API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        import sys

        sys.path.insert(0, "/workspaces/forgebase/backend/src")

        app = create_app()
        with TestClient(app) as client:
            yield client

    def test_create_project(self, client):
        """Test creating a project via API."""
        response = client.post("/api/projects", json={"name": "Test Project"})

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == "Test Project"
        assert data["prd"] == ""  # Default empty PRD
        assert "id" in data
        assert "created_at" in data
        assert data["updated_at"] is None

        # Validate UUID format
        UUID(data["id"])  # Should not raise an exception

    def test_create_project_with_prd(self, client):
        """Test creating a project with PRD content via API."""
        response = client.post(
            "/api/projects", json={"name": "Test Project", "prd": "Test PRD content"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == "Test Project"
        assert data["prd"] == "Test PRD content"
        assert "id" in data
        assert "created_at" in data
        assert data["updated_at"] is None

    def test_create_project_invalid_name(self, client):
        """Test creating a project with invalid name."""
        # Empty name
        response = client.post("/api/projects", json={"name": ""})
        assert response.status_code == 422

        # Missing name
        response = client.post("/api/projects", json={})
        assert response.status_code == 422

    def test_list_projects_empty(self, client):
        """Test listing projects when none exist."""
        response = client.get("/api/projects")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_projects_with_data(self, client):
        """Test listing projects after creating some."""
        # Create projects
        project1 = client.post("/api/projects", json={"name": "Project 1"}).json()
        project2 = client.post("/api/projects", json={"name": "Project 2"}).json()

        # List projects
        response = client.get("/api/projects")

        assert response.status_code == 200
        projects = response.json()

        assert len(projects) == 2
        # Should be ordered by creation date (newest first)
        assert projects[0]["id"] == project2["id"]
        assert projects[1]["id"] == project1["id"]

    def test_get_project(self, client):
        """Test getting a specific project."""
        # Create a project
        created = client.post("/api/projects", json={"name": "Test Project"}).json()
        project_id = created["id"]

        # Get the project
        response = client.get(f"/api/projects/{project_id}")

        assert response.status_code == 200
        data = response.json()
        assert data == created

    def test_get_project_not_found(self, client):
        """Test getting a non-existent project."""
        non_existent_id = str(uuid4())
        response = client.get(f"/api/projects/{non_existent_id}")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_project_invalid_uuid(self, client):
        """Test getting a project with invalid UUID."""
        response = client.get("/api/projects/invalid-uuid")

        assert response.status_code == 422

    def test_update_project(self, client):
        """Test updating a project with both name and PRD."""
        # Create a project
        created = client.post(
            "/api/projects", json={"name": "Original Name", "prd": "Original PRD"}
        ).json()
        project_id = created["id"]

        # Update the project
        response = client.put(
            f"/api/projects/{project_id}",
            json={"name": "Updated Name", "prd": "Updated PRD"},
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == project_id
        assert data["name"] == "Updated Name"
        assert data["prd"] == "Updated PRD"
        assert data["created_at"] == created["created_at"]
        assert data["updated_at"] is not None

    def test_update_project_not_found(self, client):
        """Test updating a non-existent project."""
        non_existent_id = str(uuid4())
        response = client.put(
            f"/api/projects/{non_existent_id}",
            json={"name": "New Name", "prd": "New PRD"},
        )

        assert response.status_code == 404

    def test_update_project_invalid_name(self, client):
        """Test updating a project with invalid name."""
        # Create a project
        created = client.post("/api/projects", json={"name": "Test Project"}).json()
        project_id = created["id"]

        # Try to update with empty name
        response = client.put(
            f"/api/projects/{project_id}", json={"name": "", "prd": "Some PRD"}
        )

        assert response.status_code == 422

    def test_delete_project(self, client):
        """Test deleting a project."""
        # Create a project
        created = client.post("/api/projects", json={"name": "Test Project"}).json()
        project_id = created["id"]

        # Delete the project
        response = client.delete(f"/api/projects/{project_id}")

        assert response.status_code == 200
        assert response.json()["status"] == "deleted"

        # Verify it's gone
        get_response = client.get(f"/api/projects/{project_id}")
        assert get_response.status_code == 404

    def test_delete_project_not_found(self, client):
        """Test deleting a non-existent project."""
        non_existent_id = str(uuid4())
        response = client.delete(f"/api/projects/{non_existent_id}")

        assert response.status_code == 404

    def test_project_crud_workflow(self, client):
        """Test a complete CRUD workflow."""
        # Create
        created = client.post(
            "/api/projects", json={"name": "Workflow Test", "prd": "Test PRD"}
        ).json()
        project_id = created["id"]

        # Read
        get_response = client.get(f"/api/projects/{project_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["name"] == "Workflow Test"
        assert data["prd"] == "Test PRD"

        # Update
        update_response = client.put(
            f"/api/projects/{project_id}",
            json={"name": "Updated Workflow Test", "prd": "Updated PRD"},
        )
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["name"] == "Updated Workflow Test"
        assert updated_data["prd"] == "Updated PRD"

        # List (should show updated name and PRD)
        list_response = client.get("/api/projects")
        assert list_response.status_code == 200
        projects = list_response.json()
        assert len(projects) == 1
        assert projects[0]["name"] == "Updated Workflow Test"
        assert projects[0]["prd"] == "Updated PRD"

        # Delete
        delete_response = client.delete(f"/api/projects/{project_id}")
        assert delete_response.status_code == 200

        # List (should be empty)
        list_response = client.get("/api/projects")
        assert list_response.status_code == 200
        assert list_response.json() == []
