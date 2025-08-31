"""A deterministic stub agent for testing and development."""

import asyncio
from typing import AsyncIterator


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
        reply = ["This ", "is ", "a ", "stub ", "reply."]
        for chunk in reply:
            yield chunk
            await asyncio.sleep(0.01)  # Simulate network latency

    async def reset(self) -> None:
        """Does nothing, as the stub agent is stateless."""
