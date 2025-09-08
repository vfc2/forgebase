"""Tests for the multi-agent system."""

import pytest

from forgebase.core.multi_agent_service import MultiAgentService
from forgebase.core.agent_config import AgentRole
from forgebase.infrastructure.agent_factory import AgentFactory
from forgebase.infrastructure.project_repository import InMemoryProjectRepository


class TestMultiAgentService:
    """Test the multi-agent service functionality."""

    @pytest.fixture
    def project_repository(self):
        """Create a test project repository."""
        return InMemoryProjectRepository()

    @pytest.fixture
    def multi_agent_service(self, project_repository):
        """Create a multi-agent service for testing."""
        # Register tools for the test
        from forgebase.infrastructure.config import _register_tools

        _register_tools(project_repository)
        return MultiAgentService(project_repository)

    def test_service_initialization(self, multi_agent_service):
        """Test that the service initializes correctly."""
        assert multi_agent_service is not None
        assert multi_agent_service.main_agent is not None
        assert multi_agent_service.agent_factory is not None

    def test_get_available_agents(self, multi_agent_service):
        """Test getting available agents."""
        agents = multi_agent_service.get_available_agents()

        # Should have all configured agents
        assert "prd_facilitator" in agents
        assert "technical_analyst" in agents
        assert "data_collector" in agents
        assert "requirements_validator" in agents

        # Check descriptions are present
        assert (
            agents["prd_facilitator"]
            == "Interactive agent for conversational PRD creation"
        )
        assert len(agents) == 4

    @pytest.mark.asyncio
    async def test_send_message_stream(self, multi_agent_service):
        """Test that the main agent can handle messages."""
        message = "Hello, I want to create a new app"

        # Collect all chunks
        chunks = []
        async for chunk in multi_agent_service.send_message_stream(message):
            chunks.append(chunk)

        # Should get some response (even if it's a stub)
        assert len(chunks) > 0
        response = "".join(chunks)
        assert len(response) > 0

    @pytest.mark.asyncio
    async def test_analyze_technical_requirements(self, multi_agent_service):
        """Test technical analysis functionality."""
        project_id = "test-project"
        requirements = "Build a mobile app with real-time features"

        result = await multi_agent_service.analyze_technical_requirements(
            project_id, requirements
        )

        assert "analysis" in result
        assert "agent_role" in result
        assert "tools_used" in result
        # In test environment, will use stub agents
        assert result["agent_role"] in ["technical_analyst", "stub"]

    @pytest.mark.asyncio
    async def test_collect_project_data(self, multi_agent_service):
        """Test data collection functionality."""
        project_id = "test-project"

        result = await multi_agent_service.collect_project_data(project_id)

        assert "collected_data" in result
        assert "agent_role" in result
        assert "tools_used" in result
        # In test environment, will use stub agents
        assert result["agent_role"] in ["data_collector", "stub"]

    @pytest.mark.asyncio
    async def test_validate_requirements(self, multi_agent_service):
        """Test requirements validation functionality."""
        requirements = "User can login and view dashboard"

        result = await multi_agent_service.validate_requirements(requirements)

        assert "validation_result" in result
        assert "agent_role" in result
        assert "tools_used" in result
        # In test environment, will use stub agents
        assert result["agent_role"] in ["requirements_validator", "stub"]

    @pytest.mark.asyncio
    async def test_reset(self, multi_agent_service):
        """Test that reset works without errors."""
        await multi_agent_service.reset()
        # If no exception is raised, the test passes


class TestAgentFactory:
    """Test the agent factory functionality."""

    @pytest.fixture
    def project_repository(self):
        """Create a test project repository."""
        return InMemoryProjectRepository()

    @pytest.fixture
    def agent_factory(self, project_repository):
        """Create an agent factory for testing."""
        # Register tools for the test
        from forgebase.infrastructure.config import _register_tools

        _register_tools(project_repository)
        return AgentFactory(project_repository)

    def test_create_agent_prd_facilitator(self, agent_factory):
        """Test creating a PRD facilitator agent."""
        agent = agent_factory.create_agent(AgentRole.PRD_FACILITATOR)

        assert agent is not None
        # In test environment without Azure credentials, will be stub
        assert agent.role in ["prd_facilitator", "stub"]
        # Stub agents have empty tool lists
        if agent.role != "stub":
            assert "save_draft_prd" in agent.available_tools
            assert "save_completed_prd" in agent.available_tools

    def test_create_agent_technical_analyst(self, agent_factory):
        """Test creating a technical analyst agent."""
        agent = agent_factory.create_agent(AgentRole.TECHNICAL_ANALYST)

        assert agent is not None
        # In test environment without Azure credentials, will be stub
        assert agent.role in ["technical_analyst", "stub"]
        # Stub agents have empty tool lists
        if agent.role != "stub":
            assert "analyze_codebase" in agent.available_tools
            assert "suggest_architecture" in agent.available_tools
            assert "get_project_data" in agent.available_tools

    def test_agent_caching(self, agent_factory):
        """Test that agents are cached properly."""
        agent1 = agent_factory.create_agent(AgentRole.PRD_FACILITATOR)
        agent2 = agent_factory.create_agent(AgentRole.PRD_FACILITATOR)

        # Should return the same instance
        assert agent1 is agent2

    def test_convenience_methods(self, agent_factory):
        """Test convenience methods for getting specific agents."""
        prd_agent = agent_factory.get_prd_facilitator()
        tech_agent = agent_factory.get_technical_analyst()
        data_agent = agent_factory.get_data_collector()
        validator_agent = agent_factory.get_requirements_validator()

        # In test environment, these will be stub agents
        assert prd_agent.role in ["prd_facilitator", "stub"]
        assert tech_agent.role in ["technical_analyst", "stub"]
        assert data_agent.role in ["data_collector", "stub"]
        assert validator_agent.role in ["requirements_validator", "stub"]

    def test_clear_cache(self, agent_factory):
        """Test that cache clearing works."""
        agent1 = agent_factory.create_agent(AgentRole.PRD_FACILITATOR)
        agent_factory.clear_cache()
        agent2 = agent_factory.create_agent(AgentRole.PRD_FACILITATOR)

        # Should be different instances after cache clear
        assert agent1 is not agent2
