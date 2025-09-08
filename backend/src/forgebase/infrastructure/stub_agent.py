"""A deterministic stub agent for testing and development."""

import asyncio
from typing import AsyncIterator, List


class StubAgent:
    """
    A stub agent that produces a fixed, streaming response.
    """

    async def send_message_stream(self, user_text: str) -> AsyncIterator[str]:
        """
        Simulates a streaming response.

        Args:
            user_text: The user's message (ignored).

        Yields:
            AsyncIterator[str]: Chunks of a fixed reply.
        """
        del user_text  # Unused

        # Keep output aligned with tests
        reply = ["This ", "is ", "a ", "stub ", "reply."]

        for chunk in reply:
            yield chunk
            await asyncio.sleep(0.01)  # Small delay to simulate streaming

    async def reset(self) -> None:
        """Does nothing, as the stub agent is stateless."""
        return

    @property
    def role(self) -> str:
        """Get the agent's role identifier."""
        return "stub"

    @property
    def available_tools(self) -> List[str]:
        """Get list of available tool names for this agent."""
        return []
