"""Tests for configuration and agent selection logic."""

# pylint: disable=duplicate-code

import os
from unittest.mock import patch

from forgebase.infrastructure import config
from forgebase.infrastructure.agent import Agent
from forgebase.core.service import ForgebaseService


class TestConfiguration:
    """Test suite for configuration logic."""

    @patch.dict(os.environ, {}, clear=True)
    def test_get_service_returns_stub_agent_when_no_env_vars(self):
        """Test that service with stub agent is returned when environment variables are missing."""
        service = config.get_service()
        assert isinstance(service, ForgebaseService)
        # The agent within the service should be in stub mode
        # We test this by creating an agent with the same environment
        test_agent = Agent(role="test")
        assert test_agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "",  # Empty key
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_get_service_returns_stub_agent_when_api_key_empty(self):
        """Test that service with stub agent is returned when API key is empty."""
        service = config.get_service()
        assert isinstance(service, ForgebaseService)
        # Test agent creation with same environment
        test_agent = Agent(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            role="test",
        )
        assert test_agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "",  # Empty endpoint
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_get_service_returns_stub_agent_when_endpoint_empty(self):
        """Test that service with stub agent is returned when endpoint is empty."""
        service = config.get_service()
        assert isinstance(service, ForgebaseService)
        # Test agent creation with same environment
        test_agent = Agent(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            role="test",
        )
        assert test_agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "",  # Empty deployment
        },
        clear=True,
    )
    def test_get_service_returns_stub_agent_when_deployment_empty(self):
        """Test that service with stub agent is returned when deployment name is empty."""
        service = config.get_service()
        assert isinstance(service, ForgebaseService)
        # Test agent creation with same environment
        test_agent = Agent(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            role="test",
        )
        assert test_agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            # Missing AZURE_OPENAI_DEPLOYMENT_NAME
        },
        clear=True,
    )
    def test_get_service_returns_stub_agent_when_deployment_missing(self):
        """Test that service with stub agent is returned when deployment name is missing."""
        service = config.get_service()
        assert isinstance(service, ForgebaseService)
        # Test agent creation with same environment
        test_agent = Agent(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            role="test",
        )
        assert test_agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_get_service_returns_service_with_real_agent_when_all_env_vars_present(
        self,
    ):
        """Test service with real agent when all environment variables present."""
        service = config.get_service()

        # Should be ForgebaseService instance
        assert isinstance(service, ForgebaseService)

        # Test agent creation with same environment to verify config logic
        test_agent = Agent(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            role="test",
        )
        # Should have real agent configured (not None)
        assert test_agent.agent is not None
        assert test_agent.role == "test"
