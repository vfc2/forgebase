"""Tests for configuration and agent selection logic."""

# pylint: disable=duplicate-code

import os
from unittest.mock import patch

from forgebase.infrastructure import config
from forgebase.infrastructure.agent import Agent


class TestConfiguration:
    """Test suite for configuration logic."""

    @patch.dict(os.environ, {}, clear=True)
    def test_get_agent_returns_stub_when_no_env_vars(self):
        """Test that Agent is returned in stub mode when environment variables are missing."""
        agent = config.get_agent()
        assert isinstance(agent, Agent)
        # Agent should be in stub mode (no real agent configured)
        assert agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "",  # Empty key
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_get_agent_returns_stub_when_api_key_empty(self):
        """Test that Agent is returned in stub mode when API key is empty."""
        agent = config.get_agent()
        assert isinstance(agent, Agent)
        assert agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "",  # Empty endpoint
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_get_agent_returns_stub_when_endpoint_empty(self):
        """Test that Agent is returned in stub mode when endpoint is empty."""
        agent = config.get_agent()
        assert isinstance(agent, Agent)
        assert agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "",  # Empty deployment
        },
        clear=True,
    )
    def test_get_agent_returns_stub_when_deployment_empty(self):
        """Test that Agent is returned in stub mode when deployment name is empty."""
        agent = config.get_agent()
        assert isinstance(agent, Agent)
        assert agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            # Missing AZURE_OPENAI_DEPLOYMENT_NAME
        },
        clear=True,
    )
    def test_get_agent_returns_stub_when_deployment_missing(self):
        """Test that Agent is returned in stub mode when deployment name is missing."""
        agent = config.get_agent()
        assert isinstance(agent, Agent)
        assert agent.agent is None

    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_get_agent_returns_agent_with_credentials_when_all_env_vars_present(self):
        """Test that Agent is returned with real agent when all environment variables are present."""
        agent = config.get_agent()

        # Should be Agent instance
        assert isinstance(agent, Agent)
        # Should have real agent configured (not None)
        assert agent.agent is not None
        # Should have the correct role
        assert agent.role == "prd_facilitator"
