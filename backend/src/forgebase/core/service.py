"""Unified service for chat and project management."""

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

    async def send_message_stream(
        self, user_text: str, project_id: str | None = None
    ) -> AsyncIterator[str]:
        """Send message and stream response.

        Args:
            user_text: User input message
            project_id: Optional project context (for future use)

        Yields:
            String chunks of the agent's response
        """
        # Future: Could inject project context here
        del project_id  # Unused for now
        async for chunk in await self._agent.send_message_stream(user_text):
            yield chunk

    async def reset_chat(self) -> None:
        """Reset chat state."""
        await self._agent.reset()

    # Project management methods
    async def create_project(self, name: str, prd: str = "") -> Project:
        """Create a new project.

        Args:
            name: Project name
            prd: Initial PRD content

        Returns:
            Created project
        """
        project = Project.create(name, prd)
        return await self._project_repository.create(project)

    async def get_project(self, project_id: str) -> Project:
        """Get project by ID.

        Args:
            project_id: Project UUID as string

        Returns:
            Project if found

        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        project_uuid = UUID(project_id)
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
        """Update project.

        Args:
            project_id: Project UUID as string
            name: New name (optional)
            prd: New PRD content (optional)

        Returns:
            Updated project

        Raises:
            ProjectNotFoundError: If project doesn't exist
        """
        project_uuid = UUID(project_id)

        # Get existing project
        existing_project = await self._project_repository.get_by_id(project_uuid)
        if not existing_project:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        # Update fields
        if name is not None:
            existing_project.update_name(name)
        if prd is not None:
            existing_project.update_prd(prd)

        # Save updated project
        return await self._project_repository.update(existing_project)

    async def delete_project(self, project_id: str) -> bool:
        """Delete project.

        Args:
            project_id: Project UUID as string

        Returns:
            True if deleted, False if not found
        """
        project_uuid = UUID(project_id)
        return await self._project_repository.delete(project_uuid)
