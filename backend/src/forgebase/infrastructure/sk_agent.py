"""Semantic Kernel agent implementation."""

from typing import AsyncIterator, List

from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from forgebase.core.ports import AgentPort


class SemanticKernelAgent(AgentPort):
    """Semantic Kernel-based agent implementation using Azure OpenAI."""

    def __init__(
        self,
        *,
        endpoint: str,
        api_key: str,
        deployment_name: str,
        instructions: str = "You are a helpful assistant.",
        role: str = "assistant",
    ) -> None:
        """Initialize the Semantic Kernel agent.

        Args:
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            deployment_name: Azure OpenAI deployment name
            instructions: System instructions for the agent
            role: Role identifier for the agent
        """
        self._role = role

        self.agent = ChatCompletionAgent(
            service=AzureChatCompletion(
                deployment_name=deployment_name,
                endpoint=endpoint,
                api_key=api_key,
            ),
            name=f"forgebase-{role}",
            instructions=instructions,
        )

        self.thread: ChatHistoryAgentThread | None = None

    async def send_message_stream(
        self, user_text: str
    ) -> AsyncIterator[str]:  # pylint: disable=invalid-overridden-method
        """Send message and stream response from Azure OpenAI.

        Args:
            user_text: User input message

        Yields:
            String chunks of the agent's response
        """
        if self.thread is None:
            self.thread = ChatHistoryAgentThread()

        async for response in self.agent.invoke_stream(
            messages=user_text, thread=self.thread
        ):
            try:
                if response.content and response.content.content:
                    yield response.content.content
            except AttributeError:
                continue

    async def reset(self) -> None:
        """Reset conversation state."""
        self.thread = None

    @property
    def role(self) -> str:
        """Get agent role."""
        return self._role

    @property
    def available_tools(self) -> List[str]:
        """Get available tools (placeholder for future)."""
        return []
