"""Multi-agent orchestration service."""

from typing import AsyncIterator, Dict, Any

from forgebase.core.ports import ProjectRepositoryPort
from forgebase.core.agent_config import AGENT_CONFIGS
from forgebase.infrastructure.agent_factory import AgentFactory


class MultiAgentService:
    """
    Service for orchestrating multiple agents with different roles.

    The PRD facilitator is the main user-facing agent, while other agents
    work in the background to provide specialized capabilities.
    """

    def __init__(self, project_repository: ProjectRepositoryPort):
        """Initialize the multi-agent service."""
        self.project_repository = project_repository
        self.agent_factory = AgentFactory(project_repository)

        # Initialize the main user-facing agent
        self.main_agent = self.agent_factory.get_prd_facilitator()

    async def send_message_stream(self, user_text: str) -> AsyncIterator[str]:
        """
        Send a user message to the main agent and stream the response.

        Args:
            user_text: The user's message.

        Yields:
            AsyncIterator[str]: Chunks of the agent's reply.
        """
        async for chunk in self.main_agent.send_message_stream(user_text):
            yield chunk

    async def reset(self) -> None:
        """Reset all agent states."""
        await self.main_agent.reset()
        # Clear the agent cache to reset background agents too
        self.agent_factory.clear_cache()

    async def analyze_technical_requirements(
        self, project_id: str, requirements: str
    ) -> Dict[str, Any]:
        """
        Use the technical analyst agent to analyze requirements.

        Args:
            project_id: The project ID
            requirements: The requirements to analyze

        Returns:
            Dict containing the analysis results
        """
        technical_agent = self.agent_factory.get_technical_analyst()

        # For now, we'll use a simple prompt-based approach
        # In a full implementation, this would use the agent's tools
        prompt = f"Analyze these technical requirements for project {project_id}: {requirements}"

        response_chunks = []
        async for chunk in technical_agent.send_message_stream(prompt):
            response_chunks.append(chunk)

        return {
            "analysis": "".join(response_chunks),
            "agent_role": technical_agent.role,
            "tools_used": technical_agent.available_tools,
        }

    async def collect_project_data(self, project_id: str) -> Dict[str, Any]:
        """
        Use the data collector agent to gather project information.

        Args:
            project_id: The project ID

        Returns:
            Dict containing the collected data
        """
        data_collector = self.agent_factory.get_data_collector()

        prompt = f"Collect and organize data for project {project_id}"

        response_chunks = []
        async for chunk in data_collector.send_message_stream(prompt):
            response_chunks.append(chunk)

        return {
            "collected_data": "".join(response_chunks),
            "agent_role": data_collector.role,
            "tools_used": data_collector.available_tools,
        }

    async def validate_requirements(self, requirements: str) -> Dict[str, Any]:
        """
        Use the requirements validator agent to check completeness.

        Args:
            requirements: The requirements to validate

        Returns:
            Dict containing the validation results
        """
        validator = self.agent_factory.get_requirements_validator()

        prompt = (
            f"Validate these requirements for completeness and clarity: {requirements}"
        )

        response_chunks = []
        async for chunk in validator.send_message_stream(prompt):
            response_chunks.append(chunk)

        return {
            "validation_result": "".join(response_chunks),
            "agent_role": validator.role,
            "tools_used": validator.available_tools,
        }

    def get_available_agents(self) -> Dict[str, str]:
        """Get a list of available agent roles and their descriptions."""
        return {
            config.role.value: config.description for config in AGENT_CONFIGS.values()
        }
