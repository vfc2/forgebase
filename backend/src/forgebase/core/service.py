"""Unified service for chat and project management."""

from __future__ import annotations
from typing import AsyncIterator
from uuid import UUID

from forgebase.core.ports import AgentPort, ProjectRepositoryPort
from forgebase.core.entities import Project
from forgebase.core.exceptions import ProjectNotFoundError


class ForgebaseService:
    """Main service orchestrating chat and project management."""

    def __init__(self, agent: AgentPort, project_repository: ProjectRepositoryPort):
        """Initialize the service.

        Args:
            agent: Agent implementation for chat functionality
            project_repository: Repository for project persistence
        """
        self._agent = agent
        self._project_repository = project_repository

    async def send_message_stream(self, user_text: str) -> AsyncIterator[str]:
        """Send message and stream response.

        Args:
            user_text: User input message

        Yields:
            String chunks of the agent's response
        """
        async for chunk in self._agent.send_message_stream(user_text):
            yield chunk

    async def reset_chat(self) -> None:
        """Reset chat state."""
        await self._agent.reset()

    # Project management methods
    async def create_project(self, name: str, prd: str = "") -> Project:
        """Create a new project.

        Args:
            name: The project name
            prd: The initial PRD content (optional)

        Returns:
            The created project

        Raises:
            ValueError: If project name is invalid
        """
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")
        if len(name) > 255:
            raise ValueError("Project name too long (maximum 255 characters)")

        project = Project.create(name=name, prd=prd)
        return await self._project_repository.create(project)

    async def get_project(self, project_id: str) -> Project:
        """Get a project by ID.

        Args:
            project_id: The project ID as a string

        Returns:
            The project if found

        Raises:
            ProjectNotFoundError: If project is not found or ID format is invalid
        """
        try:
            project_uuid = UUID(project_id)
        except ValueError as exc:
            raise ProjectNotFoundError(
                f"Invalid project ID format: {project_id}"
            ) from exc

        project = await self._project_repository.get_by_id(project_uuid)
        if not project:
            raise ProjectNotFoundError(f"Project {project_id} not found")
        return project

    async def list_projects(self) -> list[Project]:
        """List all projects.

        Returns:
            List of all projects, ordered by creation date (newest first)
        """
        return await self._project_repository.get_all()

    async def update_project(
        self, project_id: str, name: str | None = None, prd: str | None = None
    ) -> Project:
        """Update a project.

        Args:
            project_id: The project ID as a string
            name: New name for the project (optional)
            prd: New PRD content for the project (optional)

        Returns:
            The updated project

        Raises:
            ProjectNotFoundError: If project is not found or ID format is invalid
            ValueError: If project name is invalid
        """
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
                raise ValueError("Project name too long (maximum 255 characters)")

        # Get existing project
        existing_project = await self._project_repository.get_by_id(project_uuid)
        if not existing_project:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        # Mutate existing project using entity methods to ensure timestamp logic
        if name is not None and name != existing_project.name:
            existing_project.update_name(name)
        if prd is not None and prd != existing_project.prd:
            existing_project.update_prd(prd)
        # If neither field changed, do not modify updated_at; repository still performs id existence check
        return await self._project_repository.update(existing_project)

    async def delete_project(self, project_id: str) -> bool:
        """Delete a project by ID.

        Args:
            project_id: The project ID as a string

        Returns:
            True if the project was deleted, False if it didn't exist

        Raises:
            ProjectNotFoundError: If ID format is invalid
        """
        try:
            project_uuid = UUID(project_id)
        except ValueError as exc:
            raise ProjectNotFoundError(
                f"Invalid project ID format: {project_id}"
            ) from exc

        return await self._project_repository.delete(project_uuid)
