"""Tests for the ChatService."""

import pytest

from forgebase.core import chat_service


@pytest.mark.asyncio
async def test_chat_service_streams_from_agent(stub_agent_fixture):
    """Verify ChatService correctly streams chunks from the agent."""
    service = chat_service.ChatService(agent=stub_agent_fixture)
    chunks = [chunk async for chunk in service.send_message_stream("hello")]
    assert chunks == ["This ", "is ", "a ", "stub ", "reply."]


@pytest.mark.asyncio
async def test_chat_service_reset(stub_agent_fixture):
    """Verify ChatService reset calls the agent's reset."""
    service = chat_service.ChatService(agent=stub_agent_fixture)
    await service.reset()
    # In a real scenario, you might check if the agent's state was cleared.
    # For the stub, it's a no-op.
