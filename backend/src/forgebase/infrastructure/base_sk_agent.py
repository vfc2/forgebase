"""Base classes for Semantic Kernel agents."""

from typing import AsyncIterator

from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
)


class BaseSemanticKernelAgent:
    """Base class for Semantic Kernel agents with shared streaming logic."""

    def __init__(self):
        """Initialize base agent."""
        self.agent: ChatCompletionAgent | None = None
        self.thread: ChatHistoryAgentThread | None = None

    async def _stream_response(self, user_text: str) -> AsyncIterator[str]:
        """
        Internal method to stream responses from Semantic Kernel agent.

        Args:
            user_text: The user's message.

        Yields:
            AsyncIterator[str]: Chunks of the agent's reply.
        """
        if self.agent is None:
            raise RuntimeError("Agent not initialized")

        if self.thread is None:
            self.thread = ChatHistoryAgentThread()

        async for response in self.agent.invoke_stream(
            messages=user_text, thread=self.thread
        ):
            try:
                if response.content and response.content.content:
                    yield response.content.content
            except AttributeError:
                # Skip responses that don't have content attribute
                continue

    async def reset(self) -> None:
        """Reset the conversation state."""
        self.thread = None
