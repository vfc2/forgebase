"""Semantic Kernel implementation of the AgentPort."""

from typing import AsyncIterator

from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


class SKAgent:
    """
    An agent that uses Semantic Kernel to generate responses.
    """

    def __init__(self, endpoint: str, api_key: str, deployment_name: str) -> None:
        """
        Initializes the SKAgent with Azure OpenAI configuration.

        Args:
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            deployment_name: Azure OpenAI deployment name
        """
        self.agent = ChatCompletionAgent(
            service=AzureChatCompletion(
                deployment_name=deployment_name,
                endpoint=endpoint,
                api_key=api_key,
            ),
            name="forgebase-agent",
            instructions="You are a helpful chatbot.",
        )
        self.thread: ChatHistoryAgentThread | None = None

    async def send_message_stream(
        self, user_text: str
    ) -> AsyncIterator[str]:
        """
        Send a user message and stream the assistant's reply.

        Args:
            user_text: The user's message.

        Yields:
            AsyncIterator[str]: Chunks of the agent's reply.
        """
        if self.thread is None:
            self.thread = ChatHistoryAgentThread()

        async for response in self.agent.invoke_stream(
            messages=user_text, thread=self.thread
        ):
            if response.content:
                yield response.content.content

    async def reset(self) -> None:
        """Reset the conversation state."""
        self.thread = None
