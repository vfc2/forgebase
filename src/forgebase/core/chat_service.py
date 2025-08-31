"""Core service orchestrating chat interactions."""

from typing import AsyncIterator

from forgebase.core import ports


class ChatService:
    """
    Orchestrates chat messages between a user and an agent.

    This service is the primary entry point for the core application logic,
    delegating the actual message handling to a configured agent.
    """

    def __init__(self, agent: ports.AgentPort):
        """
        Initialize the ChatService.

        Args:
            agent: The agent that will handle message processing.
        """
        self._agent = agent

    async def send_message_stream(self, user_text: str) -> AsyncIterator[str]:
        """
        Send a user message and stream the agent's reply.

        Args:
            user_text: The user's message.

        Yields:
            AsyncIterator[str]: Chunks of the agent's reply.
        """
        async for chunk in self._agent.send_message_stream(user_text):
            yield chunk

    async def reset(self) -> None:
        """Reset the conversation state."""
        await self._agent.reset()
