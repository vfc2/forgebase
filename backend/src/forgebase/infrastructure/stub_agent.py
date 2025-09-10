"""Stub agent implementation for development and testing."""

import asyncio
from typing import AsyncIterator, List

from forgebase.core.ports import AgentPort


class StubAgent(AgentPort):
    """Mock agent implementation for development and testing.

    Provides realistic-looking responses without requiring external AI services.
    """

    def __init__(
        self,
        *,
        instructions: str = "You are a helpful assistant.",
        role: str = "assistant",
    ) -> None:
        """Initialize the stub agent.

        Args:
            instructions: System instructions for the agent (ignored in stub)
            role: Role identifier for the agent
        """
        self._role = role
        self._instructions = instructions
        self._message_count = 0

    async def send_message_stream(self, user_text: str) -> AsyncIterator[str]:
        """Send message and stream a mock response.

        Args:
            user_text: User input message

        Yields:
            String chunks of a simulated agent response
        """
        self._message_count += 1

        # Generate a more realistic response based on user input
        response_parts = self._generate_response(user_text)

        # Simulate realistic streaming with slight delays
        for chunk in response_parts:
            yield chunk
            # Small delay to simulate network latency
            await asyncio.sleep(0.02)

    def _generate_response(self, user_text: str) -> List[str]:
        """Generate a mock response based on user input.

        Args:
            user_text: The user's message

        Returns:
            List of response chunks to stream
        """
        # Basic keyword-based responses for more realistic behavior
        user_lower = user_text.lower()

        if any(word in user_lower for word in ["hello", "hi", "hey"]):
            return [
                "Hello! ",
                "I'm ",
                "a ",
                "development ",
                "assistant. ",
                "I'm ",
                "running ",
                "in ",
                "stub ",
                "mode ",
                "right ",
                "now. ",
                f"This ",
                "is ",
                "message ",
                f"#{self._message_count}. ",
                "How ",
                "can ",
                "I ",
                "help ",
                "you?",
            ]
        elif any(word in user_lower for word in ["prd", "product", "requirement"]):
            return [
                "I'd ",
                "be ",
                "happy ",
                "to ",
                "help ",
                "you ",
                "create ",
                "a ",
                "Product ",
                "Requirements ",
                "Document! ",
                "\n\n",
                "**Stub ",
                "Mode ",
                "Note:** ",
                "I'm ",
                "currently ",
                "running ",
                "in ",
                "development ",
                "mode. ",
                "In ",
                "production, ",
                "I ",
                "would ",
                "generate ",
                "detailed ",
                "PRDs ",
                "based ",
                "on ",
                "your ",
                "conversation. ",
                "\n\n",
                "What ",
                "product ",
                "would ",
                "you ",
                "like ",
                "to ",
                "discuss?",
            ]
        elif any(word in user_lower for word in ["help", "what", "how"]):
            return [
                "I'm ",
                "a ",
                "stub ",
                "agent ",
                "for ",
                "development ",
                "purposes. ",
                "In ",
                "production, ",
                "I ",
                "would ",
                "be ",
                "powered ",
                "by ",
                "Azure ",
                "OpenAI ",
                "and ",
                "help ",
                "you ",
                "create ",
                "product ",
                "requirements. ",
                "\n\nTry ",
                "asking ",
                "about ",
                "PRDs ",
                "or ",
                "product ",
                "features!",
            ]
        return [
            "Thank ",
            "you ",
            "for ",
            "your ",
            "message: ",
            f'"{user_text[:50]}"',
            "..." if len(user_text) > 50 else "",
            "\n\n",
            "**Stub ",
            "Response:** ",
            "I'm ",
            "a ",
            "development ",
            "placeholder. ",
            "With ",
            "proper ",
            "Azure ",
            "OpenAI ",
            "configuration, ",
            "I ",
            "would ",
            "provide ",
            "intelligent ",
            "responses ",
            "for ",
            "PRD ",
            "generation.",
        ]

    async def reset(self) -> None:
        """Reset conversation state."""
        self._message_count = 0

    @property
    def role(self) -> str:
        """Get agent role."""
        return self._role

    @property
    def available_tools(self) -> List[str]:
        """Get available tools (placeholder for future)."""
        return []
