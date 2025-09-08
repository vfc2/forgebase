"""Factory for creating configured agents."""

import os
from typing import Dict

from forgebase.core.agent_config import AgentRole, get_agent_config
from forgebase.core.ports import AgentPort, ProjectRepositoryPort
from forgebase.infrastructure.configurable_agent import ConfigurableAgent
from forgebase.infrastructure.stub_agent import StubAgent


class AgentFactory:
    """Factory for creating and managing different types of agents."""

    def __init__(self, project_repository: ProjectRepositoryPort):
        """Initialize the agent factory.

        Args:
            project_repository: Repository for project data access
        """
        self.project_repository = project_repository
        self._agent_cache: Dict[AgentRole, AgentPort] = {}

        # Azure OpenAI configuration
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    def create_agent(self, role: AgentRole) -> AgentPort:
        """Create an agent for the specified role."""
        # Check cache first
        if role in self._agent_cache:
            return self._agent_cache[role]

        # Get configuration for this role
        config = get_agent_config(role)

        # Create agent based on environment
        agent: AgentPort
        if not self.endpoint or not self.api_key or not self.deployment_name:
            # Fall back to stub agent for development/testing
            agent = StubAgent()
        else:
            # Create configured agent
            agent = ConfigurableAgent(
                config=config,
                project_repository=self.project_repository,
                endpoint=self.endpoint,
                api_key=self.api_key,
                deployment_name=self.deployment_name,
            )

        # Cache and return
        self._agent_cache[role] = agent
        return agent

    def get_prd_facilitator(self) -> AgentPort:
        """Get the main PRD facilitator agent (user-facing)."""
        return self.create_agent(AgentRole.PRD_FACILITATOR)

    def get_technical_analyst(self) -> AgentPort:
        """Get the technical analyst agent (background)."""
        return self.create_agent(AgentRole.TECHNICAL_ANALYST)

    def get_data_collector(self) -> AgentPort:
        """Get the data collector agent (background)."""
        return self.create_agent(AgentRole.DATA_COLLECTOR)

    def get_requirements_validator(self) -> AgentPort:
        """Get the requirements validator agent (background)."""
        return self.create_agent(AgentRole.REQUIREMENTS_VALIDATOR)

    def clear_cache(self) -> None:
        """Clear the agent cache."""
        self._agent_cache.clear()
