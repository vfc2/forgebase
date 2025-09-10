"""Agent implementation using Semantic Kernel and Azure OpenAI."""

from typing import AsyncIterator, List

from semantic_kernel import Kernel
from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from forgebase.core.ports import AgentPort
from forgebase.core.tool_port import ToolPort


class Agent(AgentPort):
    """Main agent implementation using Semantic Kernel and Azure OpenAI."""

    def __init__(
        self,
        *,
        endpoint: str,
        api_key: str,
        deployment_name: str,
        instructions: str = "You are a helpful assistant.",
        role: str = "assistant",
        tools: List[ToolPort] | None = None,
    ) -> None:
        """Initialize the agent.

        Args:
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            deployment_name: Azure OpenAI deployment name
            instructions: System instructions for the agent
            role: Role identifier for the agent
            tools: List of tools to make available to this agent
        """
        self._role = role
        self._tools = tools or []

        # Create kernel and register tools
        self.kernel = Kernel()

        # Register all tools with the kernel
        for tool in self._tools:
            tool.register_with_kernel(self.kernel)

        self.agent = ChatCompletionAgent(
            service=AzureChatCompletion(
                deployment_name=deployment_name,
                endpoint=endpoint,
                api_key=api_key,
            ),
            kernel=self.kernel,  # Pass kernel with registered tools
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
        """Get available tool names."""
        return [tool.plugin_name for tool in self._tools]

    def set_project_context(self, project_id: str | None) -> None:
        """Set the current project context for agent tools."""
        for tool in self._tools:
            if hasattr(tool, "set_project_context"):
                tool.set_project_context(project_id)
