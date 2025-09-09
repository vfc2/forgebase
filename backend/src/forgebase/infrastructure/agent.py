"""Unified agent implementation."""

from typing import AsyncIterator, List, Optional

from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from forgebase.core.ports import AgentPort


class Agent(AgentPort):
    """Simple, unified agent implementation."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        deployment_name: Optional[str] = None,
        instructions: str = "You are a helpful assistant.",
        role: str = "assistant",
    ) -> None:
        """Initialize the agent.

        Args:
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            deployment_name: Azure OpenAI deployment name
            instructions: System instructions for the agent
            role: Role identifier for the agent
        """
        self._role = role

        if endpoint and api_key and deployment_name:
            self.agent: Optional[ChatCompletionAgent] = ChatCompletionAgent(
                service=AzureChatCompletion(
                    deployment_name=deployment_name,
                    endpoint=endpoint,
                    api_key=api_key,
                ),
                name=f"forgebase-{role}",
                instructions=instructions,
            )
        else:
            # Fallback to stub for development
            self.agent = None

        self.thread: Optional[ChatHistoryAgentThread] = None

    async def send_message_stream(
        self, user_text: str
    ) -> AsyncIterator[str]:  # pylint: disable=invalid-overridden-method
        """Send message and stream response.

        Args:
            user_text: User input message

        Yields:
            String chunks of the agent's response
        """
        if self.agent is None:
            # Stub implementation for development
            for chunk in ["This ", "is ", "a ", "stub ", "reply."]:
                yield chunk
            return

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
