"""Tests for the project service."""

from uuid import uuid4

import pytest

from forgebase.core.exceptions import ProjectNotFoundError
from forgebase.core.project_service import ProjectService
from forgebase.infrastructure.project_repository import InMemoryProjectRepository


class TestProjectService:
    """Test cases for the ProjectService."""

    @pytest.fixture
    def repository(self):
        """Provide a fresh repository for each test."""
        return InMemoryProjectRepository()

    @pytest.fixture
    def service(self, repository):
        """Provide a project service with the repository."""
        return ProjectService(repository)

    @pytest.mark.asyncio
    async def test_create_project(self, service):
        """Test creating a project."""
        name = "Test Project"
        project = await service.create_project(name)

        assert project.name == name
        assert project.id is not None
        assert project.created_at is not None
        assert project.updated_at is None

    @pytest.mark.asyncio
    async def test_get_project(self, service):
        """Test getting a project by ID."""
        # Create a project
        created_project = await service.create_project("Test Project")

        # Retrieve it
        retrieved_project = await service.get_project(created_project.id)

        assert retrieved_project == created_project

    @pytest.mark.asyncio
    async def test_get_project_not_found(self, service):
        """Test getting a non-existent project raises an exception."""
        non_existent_id = uuid4()

        with pytest.raises(ProjectNotFoundError) as exc_info:
            await service.get_project(non_existent_id)

        assert str(non_existent_id) in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_project_optional(self, service):
        """Test getting a project optionally returns None for non-existent projects."""
        non_existent_id = uuid4()
        result = await service.get_project_optional(non_existent_id)
        assert result is None

        # But returns the project if it exists
        created_project = await service.create_project("Test Project")
        result = await service.get_project_optional(created_project.id)
        assert result == created_project

    @pytest.mark.asyncio
    async def test_list_projects_empty(self, service):
        """Test listing projects when none exist."""
        projects = await service.list_projects()
        assert projects == []

    @pytest.mark.asyncio
    async def test_list_projects_multiple(self, service):
        """Test listing multiple projects."""
        project1 = await service.create_project("Project 1")
        project2 = await service.create_project("Project 2")
        project3 = await service.create_project("Project 3")

        projects = await service.list_projects()

        assert len(projects) == 3
        # Should be ordered by creation date (newest first)
        assert projects[0] == project3
        assert projects[1] == project2
        assert projects[2] == project1

    @pytest.mark.asyncio
    async def test_update_project(self, service):
        """Test updating a project's name."""
        # Create a project
        project = await service.create_project("Original Name")
        original_created_at = project.created_at

        # Update it
        new_name = "Updated Name"
        updated_project = await service.update_project(project.id, new_name)

        assert updated_project.id == project.id
        assert updated_project.name == new_name
        assert updated_project.created_at == original_created_at
        assert updated_project.updated_at is not None
        assert updated_project.updated_at >= original_created_at

    @pytest.mark.asyncio
    async def test_update_project_not_found(self, service):
        """Test updating a non-existent project raises an exception."""
        non_existent_id = uuid4()

        with pytest.raises(ProjectNotFoundError):
            await service.update_project(non_existent_id, "New Name")

    @pytest.mark.asyncio
    async def test_delete_project(self, service):
        """Test deleting a project."""
        # Create a project
        project = await service.create_project("Test Project")

        # Verify it exists
        assert await service.get_project_optional(project.id) is not None

        # Delete it
        deleted = await service.delete_project(project.id)
        assert deleted is True

        # Verify it's gone
        assert await service.get_project_optional(project.id) is None

    @pytest.mark.asyncio
    async def test_delete_project_not_found(self, service):
        """Test deleting a non-existent project returns False."""
        non_existent_id = uuid4()
        deleted = await service.delete_project(non_existent_id)
        assert deleted is False
