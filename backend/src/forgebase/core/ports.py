"""Protocols for core components."""

from typing import AsyncIterator, List, Optional, Protocol
from uuid import UUID

from forgebase.core.entities import Project


class AgentPort(Protocol):
    """
    Defines the interface for a chat agent.

    An agent is responsible for receiving user messages and generating
    a streaming response, potentially with access to tools and data repositories.
    """

    def send_message_stream(self, user_text: str) -> AsyncIterator[str]:
        """
        Send a user message and stream the assistant's reply.

        Args:
            user_text: The raw user message to send.

        Yields:
            Chunks of the assistant's reply as they become available.
        """
        ...

    async def reset(self) -> None:
        """Reset any conversation/thread state for the agent."""
        ...

    @property
    def role(self) -> str:
        """Get the agent's role identifier."""
        ...

    @property
    def available_tools(self) -> List[str]:
        """Get list of available tool names for this agent."""
        ...


class ProjectRepositoryPort(Protocol):
    """
    Defines the interface for project persistence.

    This protocol abstracts the storage mechanism for projects,
    allowing different implementations (in-memory, database, etc.).
    """

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
        ...

    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        """
        Retrieve a project by its ID.

        Args:
            project_id: The project ID to look up.

        Returns:
            The project if found, None otherwise.
        """
        ...

    async def get_all(self) -> List[Project]:
        """
        Retrieve all projects.

        Returns:
            List of all projects, ordered by creation date (newest first).
        """
        ...

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
        ...

    async def delete(self, project_id: UUID) -> bool:
        """
        Delete a project by its ID.

        Args:
            project_id: The project ID to delete.

        Returns:
            True if the project was deleted, False if it didn't exist.
        """
        ...
