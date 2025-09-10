"""Project management service for CRUD operations and business logic."""

from __future__ import annotations
from uuid import UUID

from forgebase.core.entities import Project
from forgebase.core.exceptions import ProjectNotFoundError
from forgebase.core.ports import ProjectRepositoryPort


class ProjectService:
    """Service for project CRUD operations and business logic.

    Handles all project-related operations including validation,
    persistence coordination, and business rules.
    """

    def __init__(self, project_repository: ProjectRepositoryPort):
        """Initialize with a project repository.

        Args:
            project_repository: Repository for project persistence
        """
        self._project_repository = project_repository

    async def create_project(self, user_id: str, name: str, prd: str = "") -> Project:
        """Create a new project.

        Args:
            user_id: The ID of the user creating the project
            name: The project name
            prd: The initial PRD content (optional)

        Returns:
            The created project

        Raises:
            ValueError: If project name is invalid or user_id is empty
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")
        if len(name) > 255:
            raise ValueError("Project name too long (maximum 255 characters)")

        project = Project.create(user_id=user_id, name=name, prd=prd)
        return await self._project_repository.create(project)

    async def get_project(self, project_id: str, user_id: str) -> Project:
        """Get a project by ID for a specific user.

        Args:
            project_id: The project ID as a string
            user_id: The user ID that should own the project

        Returns:
            The project if found and owned by the user

        Raises:
            ProjectNotFoundError: If project is not found, doesn't belong to user, or ID format is invalid
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")

        try:
            project_uuid = UUID(project_id)
        except ValueError as exc:
            raise ProjectNotFoundError(
                f"Invalid project ID format: {project_id}"
            ) from exc

        project = await self._project_repository.get_by_id_for_user(project_uuid, user_id)
        if not project:
            raise ProjectNotFoundError(f"Project {project_id} not found")
        return project

    async def list_projects(self, user_id: str) -> list[Project]:
        """List all projects for a specific user.

        Returns:
            List of user's projects, ordered by creation date (newest first)
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        return await self._project_repository.get_all_for_user(user_id)

    async def update_project(
        self, project_id: str, user_id: str, name: str | None = None, prd: str | None = None
    ) -> Project:
        """Update a project for a specific user.

        Args:
            project_id: The project ID as a string
            user_id: The user ID that should own the project
            name: New name for the project (optional)
            prd: New PRD content for the project (optional)

        Returns:
            The updated project

        Raises:
            ProjectNotFoundError: If project is not found, doesn't belong to user, or ID format is invalid
            ValueError: If project name is invalid or user_id is empty
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")

        try:
            project_uuid = UUID(project_id)
        except ValueError as exc:
            raise ProjectNotFoundError(
                f"Invalid project ID format: {project_id}"
            ) from exc

        # Validate name if provided
        if name is not None:
            if not name or not name.strip():
                raise ValueError("Project name cannot be empty")
            if len(name) > 255:
                raise ValueError(
                    "Project name too long (maximum 255 characters)")

        # Get existing project (only if owned by user)
        existing_project = await self._project_repository.get_by_id_for_user(project_uuid, user_id)
        if not existing_project:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        # Mutate existing project using entity methods to ensure timestamp logic
        if name is not None and name != existing_project.name:
            existing_project.update_name(name)
        if prd is not None and prd != existing_project.prd:
            existing_project.update_prd(prd)

        return await self._project_repository.update(existing_project)

    async def delete_project(self, project_id: str, user_id: str) -> bool:
        """Delete a project by ID.

        Args:
            project_id: The project ID as a string
            user_id: The ID of the user attempting to delete the project

        Returns:
            True if the project was deleted, False if it didn't exist

        Raises:
            ProjectNotFoundError: If ID format is invalid
            ValueError: If user_id is empty
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")

        try:
            project_uuid = UUID(project_id)
        except ValueError as exc:
            raise ProjectNotFoundError(
                f"Invalid project ID format: {project_id}"
            ) from exc

        return await self._project_repository.delete_for_user(project_uuid, user_id)
