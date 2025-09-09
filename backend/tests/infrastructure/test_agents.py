"""Tests for the agent implementations."""

import pytest

from forgebase.infrastructure.agent import Agent
from forgebase.infrastructure.stub_agent import StubAgent


class TestAgent:
    """Test the main Agent implementation."""

    def test_agent_initialization_with_credentials(self):
        """Test agent initialization with credentials."""
        agent = Agent(
            endpoint="https://test.openai.azure.com/",
            api_key="test-key",
            deployment_name="test-deployment",
            instructions="Test instructions",
            role="test_agent",
        )

        assert agent.role == "test_agent"
        assert agent.agent is not None  # Should have real agent instance
        assert not agent.available_tools


class TestStubAgent:
    """Test the StubAgent implementation."""

    def test_stub_agent_initialization(self):
        """Test stub agent initialization."""
        agent = StubAgent(role="test_agent")

        assert agent.role == "test_agent"
        assert not agent.available_tools

    @pytest.mark.asyncio
    async def test_send_message_stream_stub(self):
        """Test streaming messages with stub agent."""
        agent = StubAgent(role="test_agent")

        chunks = []
        async for chunk in agent.send_message_stream("Hello"):
            chunks.append(chunk)

        # Stub agent should return some response
        assert len(chunks) > 0
        response = "".join(chunks)
        assert len(response) > 0

    @pytest.mark.asyncio
    async def test_reset(self):
        """Test resetting agent state."""
        agent = StubAgent(role="test_agent")
        await agent.reset()
        # Should not raise any exceptions

    @pytest.mark.asyncio
    async def test_multiple_messages_create_proper_responses(self):
        """Test that multiple messages work correctly."""
        agent = StubAgent(role="test_agent")

        # First message
        chunks1 = []
        async for chunk in agent.send_message_stream("Hello"):
            chunks1.append(chunk)

        # Second message
        chunks2 = []
        async for chunk in agent.send_message_stream("How are you?"):
            chunks2.append(chunk)

        # Both should have responses
        assert len(chunks1) > 0
        assert len(chunks2) > 0

    @pytest.mark.asyncio
    async def test_reset_clears_state(self):
        """Test that reset clears internal state."""
        agent = StubAgent(role="test_agent")

        # Send a message
        chunks = []
        async for chunk in agent.send_message_stream("Test"):
            chunks.append(chunk)

        # Reset
        await agent.reset()

        # Send another message - should work fine
        chunks2 = []
        async for chunk in agent.send_message_stream("Test again"):
            chunks2.append(chunk)

        assert len(chunks2) > 0
