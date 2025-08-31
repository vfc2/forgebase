"""Tests for the StubAgent."""

import pytest

from forgebase.infrastructure import stub_agent


@pytest.mark.asyncio
async def test_stub_agent_streams_chunks():
    """Test that StubAgent streams the expected chunks."""
    agent = stub_agent.StubAgent()
    chunks = [chunk async for chunk in agent.send_message_stream("test")]
    assert chunks == ["This ", "is ", "a ", "stub ", "reply."]
    assert "".join(chunks) == "This is a stub reply."


@pytest.mark.asyncio
async def test_stub_agent_reset_is_noop():
    """Verify the stub agent's reset method does nothing."""
    agent = stub_agent.StubAgent()
    # Simply call it to ensure it runs without error.
    await agent.reset()
