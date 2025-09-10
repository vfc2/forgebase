"""Chat service for agent streaming and conversation management."""

from __future__ import annotations
from typing import AsyncIterator

from forgebase.core.ports import AgentPort


class ChatService:
    """Service for chat streaming and conversation management.

    Handles all agent interactions, conversation state, and streaming responses.
    Focused solely on chat-related concerns.
    """

    def __init__(self, agent: AgentPort):
        """Initialize with an agent implementation.

        Args:
            agent: Agent implementation for chat functionality
        """
        self._agent = agent

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
