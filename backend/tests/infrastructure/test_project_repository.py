"""Tests for the in-memory project repository."""

from uuid import uuid4

import pytest

from forgebase.core.entities import Project
from forgebase.core.exceptions import ProjectAlreadyExistsError, ProjectNotFoundError
from forgebase.infrastructure.project_repository import InMemoryProjectRepository


class TestInMemoryProjectRepository:
    """Test cases for the InMemoryProjectRepository."""

    @pytest.fixture
    def repository(self):
        """Provide a fresh repository for each test."""
        return InMemoryProjectRepository()

    @pytest.mark.asyncio
    async def test_create_project(self, repository):
        """Test creating a project."""
        user_id = "test-user"
        project = Project.create(user_id, "Test Project")

        result = await repository.create(project)

        assert result == project
        assert result is project

    @pytest.mark.asyncio
    async def test_create_project_already_exists(self, repository):
        """Test creating a project with an existing ID raises an exception."""
        user_id = "test-user"
        project = Project.create(user_id, "Test Project")

        await repository.create(project)

        with pytest.raises(ProjectAlreadyExistsError) as exc_info:
            await repository.create(project)

        assert str(project.id) in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_by_id(self, repository):
        """Test getting a project by ID."""
        user_id = "test-user"
        project = Project.create(user_id, "Test Project")
        await repository.create(project)

        result = await repository.get_by_id(project.id)

        assert result == project

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repository):
        """Test getting a non-existent project returns None."""
        non_existent_id = uuid4()
        result = await repository.get_by_id(non_existent_id)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_empty(self, repository):
        """Test getting all projects when none exist."""
        result = await repository.get_all()
        assert result == []

    @pytest.mark.asyncio
    async def test_get_all_multiple(self, repository):
        """Test getting all projects."""
        user_id = "test-user"
        project1 = Project.create(user_id, "Project 1")
        project2 = Project.create(user_id, "Project 2")
        project3 = Project.create(user_id, "Project 3")

        await repository.create(project1)
        await repository.create(project2)
        await repository.create(project3)

        result = await repository.get_all()

        assert len(result) == 3
        # Should be ordered by creation date (newest first)
        assert result[0] == project3
        assert result[1] == project2
        assert result[2] == project1

    @pytest.mark.asyncio
    async def test_update_project(self, repository):
        """Test updating a project."""
        user_id = "test-user"
        project = Project.create(user_id, "Original Name")
        await repository.create(project)

        project.update_name("Updated Name")
        result = await repository.update(project)

        assert result == project

        # Verify the update is persisted
        retrieved = await repository.get_by_id(project.id)
        assert retrieved.name == "Updated Name"
        assert retrieved.updated_at is not None

    @pytest.mark.asyncio
    async def test_update_project_prd(self, repository):
        """Test updating a project's PRD content."""
        user_id = "test-user"
        project = Project.create(user_id, "Test Project", "Original PRD")
        await repository.create(project)

        project.update_prd("Updated PRD content")
        result = await repository.update(project)

        assert result == project

        # Verify the update is persisted
        retrieved = await repository.get_by_id(project.id)
        assert retrieved.prd == "Updated PRD content"
        assert retrieved.updated_at is not None

    @pytest.mark.asyncio
    async def test_update_project_not_found(self, repository):
        """Test updating a non-existent project raises an exception."""
        user_id = "test-user"
        project = Project.create(user_id, "Test Project")

        with pytest.raises(ProjectNotFoundError) as exc_info:
            await repository.update(project)

        assert str(project.id) in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_delete_project(self, repository):
        """Test deleting a project."""
        user_id = "test-user"
        project = Project.create(user_id, "Test Project")
        await repository.create(project)

        result = await repository.delete(project.id)

        assert result is True

        # Verify it's gone
        retrieved = await repository.get_by_id(project.id)
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_delete_project_not_found(self, repository):
        """Test deleting a non-existent project returns False."""
        non_existent_id = uuid4()
        result = await repository.delete(non_existent_id)
        assert result is False
