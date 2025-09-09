"""Tests for the unified agent implementation."""

import pytest

from forgebase.infrastructure.agent import Agent


class TestUnifiedAgent:
    """Test the unified Agent implementation."""

    def test_agent_initialization_stub(self):
        """Test agent initialization without credentials (stub mode)."""
        agent = Agent(role="test_agent")

        assert agent.role == "test_agent"
        assert agent.agent is None  # Should be None for stub mode
        assert not agent.available_tools

    def test_agent_initialization_with_credentials(self):
        """Test agent initialization with credentials."""
        agent = Agent(
            endpoint="https://test.openai.azure.com/",
            api_key="test-key",
            deployment_name="test-deployment",
            instructions="Test instructions",
            role="test_role",
        )

        assert agent.role == "test_role"
        assert agent.agent is not None  # Should have real agent

    @pytest.mark.asyncio
    async def test_send_message_stream_stub(self):
        """Test message streaming in stub mode."""
        agent = Agent(role="test_agent")

        chunks = []
        async for chunk in agent.send_message_stream("Hello"):
            chunks.append(chunk)

        assert len(chunks) == 5
        assert "".join(chunks) == "This is a stub reply."

    @pytest.mark.asyncio
    async def test_reset(self):
        """Test agent reset."""
        agent = Agent(role="test_agent")

        # Should not raise an exception
        await agent.reset()

        # Thread should be None after reset
        assert agent.thread is None

    @pytest.mark.asyncio
    async def test_multiple_messages_create_thread(self):
        """Test that multiple messages work correctly."""
        agent = Agent(role="test_agent")

        # First message
        chunks1 = []
        async for chunk in agent.send_message_stream("Hello"):
            chunks1.append(chunk)

        # Second message (should reuse thread in real implementation)
        chunks2 = []
        async for chunk in agent.send_message_stream("How are you?"):
            chunks2.append(chunk)

        # Both should work
        assert len(chunks1) == 5
        assert len(chunks2) == 5

    @pytest.mark.asyncio
    async def test_reset_clears_state(self):
        """Test that reset clears the agent state."""
        agent = Agent(role="test_agent")

        # Send a message to potentially create state
        async for _ in agent.send_message_stream("Hello"):
            pass

        # Reset
        await agent.reset()

        # Thread should be cleared
        assert agent.thread is None
