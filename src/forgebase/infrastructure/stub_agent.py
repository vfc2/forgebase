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

        # Test response with newlines
        reply = [
            "Here is a test response with formatting:\n\n",
            "**First Line**\n",
            "This is the first line of content.\n\n",
            "**Second Line**\n",
            "This is the second line.\n",
            "And this continues on the same line.\n\n",
            "**Final Section**\n",
            "- Bullet point one\n",
            "- Bullet point two\n",
            "- Bullet point three\n\n",
            "End of response."
        ]

        for chunk in reply:
            yield chunk
            await asyncio.sleep(0.1)  # Simulate network latency

    async def reset(self) -> None:
        """Does nothing, as the stub agent is stateless."""
