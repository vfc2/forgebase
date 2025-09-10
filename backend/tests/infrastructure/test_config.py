"""Tests for configuration and agent selection logic."""

import os
from unittest.mock import patch

from forgebase.infrastructure import config
from forgebase.infrastructure.stub_agent import StubAgent
from forgebase.infrastructure.agent import Agent
from forgebase.core.chat_service import ChatService
from forgebase.core.project_service import ProjectService
from forgebase.infrastructure.project_repository import InMemoryProjectRepository


class TestConfiguration:
    """Test suite for configuration logic."""

    @patch.dict(os.environ, {}, clear=True)
    def test_create_agent_returns_stub_when_no_env_vars(self):
        """Test that _create_agent returns StubAgent when environment variables are missing."""
        project_service = ProjectService(InMemoryProjectRepository())
        agent = config._create_agent(project_service)
        assert isinstance(agent, StubAgent)

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "",  # Empty key
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_create_agent_returns_stub_when_api_key_empty(self):
        """Test that _create_agent returns StubAgent when API key is empty."""
        project_service = ProjectService(InMemoryProjectRepository())
        agent = config._create_agent(project_service)
        assert isinstance(agent, StubAgent)

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "",  # Empty endpoint
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_create_agent_returns_stub_when_endpoint_empty(self):
        """Test that _create_agent returns StubAgent when endpoint is empty."""
        project_service = ProjectService(InMemoryProjectRepository())
        agent = config._create_agent(project_service)
        assert isinstance(agent, StubAgent)

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "",  # Empty deployment
        },
        clear=True,
    )
    def test_create_agent_returns_stub_when_deployment_empty(self):
        """Test that _create_agent returns StubAgent when deployment name is empty."""
        project_service = ProjectService(InMemoryProjectRepository())
        agent = config._create_agent(project_service)
        assert isinstance(agent, StubAgent)

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_create_agent_returns_real_agent_when_all_env_vars_present(self):
        """Test that _create_agent returns Agent when all environment variables are present."""
        project_service = ProjectService(InMemoryProjectRepository())
        agent = config._create_agent(project_service)
        assert isinstance(agent, Agent)

    @patch.dict(os.environ, {}, clear=True)
    def test_get_chat_service_returns_valid_service_with_stub(self):
        """Test that get_chat_service returns a valid ChatService with stub agent."""
        service = config.get_chat_service()
        assert isinstance(service, ChatService)

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_get_chat_service_returns_valid_service_with_real_agent(self):
        """Test that get_chat_service returns a valid ChatService with real agent."""
        service = config.get_chat_service()
        assert isinstance(service, ChatService)

    @patch.dict(os.environ, {}, clear=True)
    def test_get_project_service_returns_valid_service(self):
        """Test that get_project_service returns a valid ProjectService."""
        service = config.get_project_service()
        assert isinstance(service, ProjectService)


class TestPRDInstructionsLoading:
    """Test suite for PRD instructions loading."""

    def test_load_prd_instructions_fallback(self):
        """Test that _load_prd_instructions provides fallback when file not found."""
        instructions = config._load_prd_instructions()
        assert isinstance(instructions, str)
        assert len(instructions) > 0
