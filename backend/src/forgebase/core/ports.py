"""Protocols for core components."""

from typing import AsyncIterator, Protocol


class AgentPort(Protocol):
    """
    Defines the interface for a chat agent.

    An agent is responsible for receiving user messages and generating
    a streaming response.
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
