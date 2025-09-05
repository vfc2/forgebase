"""In-memory implementation of project repository."""

from typing import Optional
from uuid import UUID

from forgebase.core.entities import Project
from forgebase.core.exceptions import ProjectAlreadyExistsError, ProjectNotFoundError


class InMemoryProjectRepository:
    """
    In-memory implementation of ProjectRepositoryPort.

    This implementation stores projects in memory using a dictionary.
    It's suitable for development and testing, but data will be lost
    when the application restarts.
    """

    def __init__(self):
        """Initialize the repository with an empty storage."""
        self._projects: dict[UUID, Project] = {}

    async def create(self, project: Project) -> Project:
        """
        Store a new project.

        Args:
            project: The project to store.

        Returns:
            The stored project.

        Raises:
            ProjectAlreadyExistsError: If a project with the same ID exists.
        """
        if project.id in self._projects:
            raise ProjectAlreadyExistsError(str(project.id))

        self._projects[project.id] = project
        return project

    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        """
        Retrieve a project by its ID.

        Args:
            project_id: The project ID to look up.

        Returns:
            The project if found, None otherwise.
        """
        return self._projects.get(project_id)

    async def get_all(self) -> list[Project]:
        """
        Retrieve all projects.

        Returns:
            List of all projects, ordered by creation date (newest first).
        """
        projects = list(self._projects.values())
        return sorted(projects, key=lambda p: p.created_at, reverse=True)

    async def update(self, project: Project) -> Project:
        """
        Update an existing project.

        Args:
            project: The project with updated data.

        Returns:
            The updated project.

        Raises:
            ProjectNotFoundError: If the project doesn't exist.
        """
        if project.id not in self._projects:
            raise ProjectNotFoundError(str(project.id))

        self._projects[project.id] = project
        return project

    async def delete(self, project_id: UUID) -> bool:
        """
        Delete a project by its ID.

        Args:
            project_id: The project ID to delete.

        Returns:
            True if the project was deleted, False if it didn't exist.
        """
        if project_id in self._projects:
            del self._projects[project_id]
            return True
        return False
