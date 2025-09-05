"""Core service for project management."""

from typing import List, Optional
from uuid import UUID

from forgebase.core import ports
from forgebase.core.entities import Project
from forgebase.core.exceptions import ProjectNotFoundError


class ProjectService:
    """
    Orchestrates project management operations.

    This service handles the business logic for project CRUD operations,
    delegating persistence to a configured repository.
    """

    def __init__(self, repository: ports.ProjectRepositoryPort):
        """
        Initialize the ProjectService.

        Args:
            repository: The repository that will handle persistence.
        """
        self._repository = repository

    async def create_project(self, name: str) -> Project:
        """
        Create a new project.

        Args:
            name: The name of the project.

        Returns:
            The created project.
        """
        project = Project.create(name)
        return await self._repository.create(project)

    async def get_project(self, project_id: UUID) -> Project:
        """
        Get a project by ID.

        Args:
            project_id: The project ID to retrieve.

        Returns:
            The project.

        Raises:
            ProjectNotFoundError: If the project doesn't exist.
        """
        project = await self._repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(str(project_id))
        return project

    async def get_project_optional(self, project_id: UUID) -> Optional[Project]:
        """
        Get a project by ID, returning None if not found.

        Args:
            project_id: The project ID to retrieve.

        Returns:
            The project if found, None otherwise.
        """
        return await self._repository.get_by_id(project_id)

    async def list_projects(self) -> List[Project]:
        """
        List all projects.

        Returns:
            List of all projects, ordered by creation date (newest first).
        """
        return await self._repository.get_all()

    async def update_project(self, project_id: UUID, name: str) -> Project:
        """
        Update a project's name.

        Args:
            project_id: The project ID to update.
            name: The new name for the project.

        Returns:
            The updated project.

        Raises:
            ProjectNotFoundError: If the project doesn't exist.
        """
        project = await self.get_project(project_id)
        project.update_name(name)
        return await self._repository.update(project)

    async def delete_project(self, project_id: UUID) -> bool:
        """
        Delete a project.

        Args:
            project_id: The project ID to delete.

        Returns:
            True if the project was deleted, False if it didn't exist.
        """
        return await self._repository.delete(project_id)
