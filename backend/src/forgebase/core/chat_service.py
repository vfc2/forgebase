"""Chat service for agent streaming and conversation management."""

from __future__ import annotations
from typing import AsyncIterator

from forgebase.core.ports import AgentPort


class ChatService:
    """Service for chat streaming and conversation management.

    Handles all agent interactions, conversation state, and streaming responses.
    Focused solely on chat-related concerns.
    """

    def __init__(self, agent: AgentPort, current_project_id: str | None = None):
        """Initialize with an agent implementation.

        Args:
            agent: Agent implementation for chat functionality
            current_project_id: Optional project context for the conversation
        """
        self._agent = agent
        self._current_project_id = current_project_id

        # Set project context in agent if provided
        if current_project_id:
            self._agent.set_project_context(current_project_id)

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
        """Reset chat conversation state."""
        await self._agent.reset()

    def set_project_context(self, project_id: str | None) -> None:
        """Set the current project context for the conversation.

        Args:
            project_id: Project ID to set as current context, or None to clear
        """
        self._current_project_id = project_id
        self._agent.set_project_context(project_id)

    @property
    def current_project_id(self) -> str | None:
        """Get the current project context."""
        return self._current_project_id
