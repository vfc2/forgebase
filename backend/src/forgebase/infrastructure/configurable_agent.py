"""Enhanced Semantic     def __init__(
    self,
    config: AgentConfig,
    project_repository: ProjectRepositoryPort,
    endpoint: str,
    api_key: str,
    deployment_name: str,
) -> None:gent with tool support and role-based configuration."""

from typing import AsyncIterator, List
from pathlib import Path

from semantic_kernel.agents.chat_completion.chat_completion_agent import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from forgebase.core.agent_config import AgentConfig
from forgebase.core.tool_registry import tool_registry
from forgebase.core.ports import ProjectRepositoryPort


class ConfigurableAgent:
    """
    An agent that uses Semantic Kernel with configurable roles, prompts, and tools.
    """

    def __init__(
        self,
        config: AgentConfig,
        project_repository: ProjectRepositoryPort,
        endpoint: str,
        api_key: str,
        deployment_name: str,
    ) -> None:
        """
        Initialize the ConfigurableAgent.

        Args:
            config: Agent configuration defining role, prompts, and tools
            project_repository: Repository for project data access
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            deployment_name: Azure OpenAI deployment name
        """
        self.config = config
        self.project_repository = project_repository

        # Load instructions from file
        instructions = self._load_instructions(config.instructions_file)

        # Get tools for this agent
        self.tools = tool_registry.get_tools_for_agent(config.tools)

        # Initialize the Semantic Kernel agent
        self.agent = ChatCompletionAgent(
            service=AzureChatCompletion(
                deployment_name=deployment_name,
                endpoint=endpoint,
                api_key=api_key,
            ),
            name=f"forgebase-{config.role.value}",
            instructions=instructions,
        )
        self.thread: ChatHistoryAgentThread | None = None

    def _load_instructions(self, instructions_file: str) -> str:
        """Load instructions from file."""
        try:
            instructions_path = Path(__file__).parent.parent / instructions_file
            return instructions_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return f"You are a {self.config.name}. {self.config.description}"

    async def send_message_stream(self, user_text: str) -> AsyncIterator[str]:
        """
        Send a user message and stream the assistant's reply.

        Args:
            user_text: The user's message.

        Yields:
            AsyncIterator[str]: Chunks of the agent's reply.
        """
        if self.thread is None:
            self.thread = ChatHistoryAgentThread()

        # For now, just stream the basic response
        # Future enhancement: integrate full tool calling with Semantic Kernel
        async for response in self.agent.invoke_stream(
            messages=user_text, thread=self.thread
        ):
            try:
                if response.content and response.content.content:
                    yield response.content.content
            except AttributeError:
                continue

    async def reset(self) -> None:
        """Reset the conversation state."""
        self.thread = None

    @property
    def role(self) -> str:
        """Get the agent's role identifier."""
        return self.config.role.value

    @property
    def available_tools(self) -> List[str]:
        """Get list of available tool names for this agent."""
        return self.config.tools

    def is_user_facing(self) -> bool:
        """Check if this agent is user-facing."""
        return self.config.is_user_facing
