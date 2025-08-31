"""Tests for configuration and agent selection logic."""

# pylint: disable=duplicate-code

import os
from unittest.mock import patch, MagicMock

from forgebase.infrastructure import config, stub_agent


class TestConfiguration:
    """Test suite for configuration logic."""

    @patch.dict(os.environ, {}, clear=True)
    def test_get_agent_returns_stub_when_no_env_vars(self):
        """Test that StubAgent is returned when environment variables are missing."""
        agent = config.get_agent()
        assert isinstance(agent, stub_agent.StubAgent)

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
        """Test that StubAgent is returned when API key is empty."""
        agent = config.get_agent()
        assert isinstance(agent, stub_agent.StubAgent)

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
        """Test that StubAgent is returned when endpoint is empty."""
        agent = config.get_agent()
        assert isinstance(agent, stub_agent.StubAgent)

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
        """Test that StubAgent is returned when deployment name is empty."""
        agent = config.get_agent()
        assert isinstance(agent, stub_agent.StubAgent)

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
        """Test that StubAgent is returned when deployment name is missing."""
        agent = config.get_agent()
        assert isinstance(agent, stub_agent.StubAgent)

    @patch("forgebase.infrastructure.config.sk_agent.SKAgent")
    @patch.dict(
        os.environ,
        {
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        },
        clear=True,
    )
    def test_get_agent_returns_sk_agent_when_all_env_vars_present(self, mock_sk_agent):
        """Test that SKAgent is returned when all environment variables are present."""
        mock_instance = MagicMock()
        mock_sk_agent.return_value = mock_instance

        agent = config.get_agent()

        # Verify SKAgent was created with correct parameters
        mock_sk_agent.assert_called_once_with(
            endpoint="https://test.openai.azure.com/",
            api_key="test-key",
            deployment_name="test-deployment",
        )

        # Verify the returned agent is the mock instance
        assert agent == mock_instance
