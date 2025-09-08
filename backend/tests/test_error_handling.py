"""Tests for error handling and edge cases with unified architecture."""

from unittest.mock import AsyncMock, MagicMock
import asyncio

import pytest

from forgebase.core.service import ForgebaseService
from forgebase.infrastructure.agent import Agent
from forgebase.infrastructure.project_repository import InMemoryProjectRepository


class TestErrorHandling:
    """Test suite for error handling scenarios."""

    @pytest.fixture
    def service(self):
        """Create a service for testing."""
        agent = Agent(role="test")  # Stub mode
        repository = InMemoryProjectRepository()
        return ForgebaseService(agent, repository)

    @pytest.mark.asyncio
    async def test_service_propagates_agent_exceptions(self, service):
        """Test that service properly propagates agent exceptions."""

        # Create an async generator that raises an exception
        async def failing_stream():
            raise RuntimeError("Agent error")
            yield  # This will never be reached

        # Mock the agent to return the failing stream
        mock_agent = MagicMock()
        mock_agent.send_message_stream = MagicMock(return_value=failing_stream())
        service._agent = mock_agent

        # Should propagate the exception
        with pytest.raises(RuntimeError, match="Agent error"):
            async for _ in service.send_message_stream("test message"):
                pass

    @pytest.mark.asyncio
    async def test_service_reset_propagates_agent_exceptions(self, service):
        """Test that service reset properly propagates agent exceptions."""
        # Mock the agent to raise an exception on reset
        mock_agent = MagicMock()
        mock_agent.reset = AsyncMock(side_effect=RuntimeError("Reset error"))
        service._agent = mock_agent

        # Should propagate the exception
        with pytest.raises(RuntimeError, match="Reset error"):
            await service.reset_chat()

    @pytest.mark.asyncio
    async def test_agent_handles_concurrent_streams(self):
        """Test that agent handles concurrent streaming properly."""
        agent = Agent(role="test")

        # Start multiple concurrent streams
        async def collect_stream(message):
            chunks = []
            async for chunk in agent.send_message_stream(message):
                chunks.append(chunk)
            return chunks

        # Run multiple streams concurrently
        tasks = [
            collect_stream("Message 1"),
            collect_stream("Message 2"),
            collect_stream("Message 3"),
        ]

        results = await asyncio.gather(*tasks)

        # All should complete successfully
        assert len(results) == 3
        for result in results:
            assert len(result) == 5  # Stub returns 5 chunks
            assert "".join(result) == "This is a stub reply."

    @pytest.mark.asyncio
    async def test_agent_handles_content_attribute_error(self):
        """Test that agent handles AttributeError gracefully in real mode."""
        # Create agent with credentials to test real mode
        agent = Agent(
            endpoint="https://test.openai.azure.com/",
            api_key="test-key",
            deployment_name="test-deployment",
            role="test",
        )

        # Mock the agent to simulate AttributeError in response processing
        mock_response = MagicMock()
        del mock_response.content  # Remove content to cause AttributeError

        mock_agent = MagicMock()

        async def mock_invoke_stream(*args, **kwargs):
            yield mock_response

        mock_agent.invoke_stream = mock_invoke_stream
        agent.agent = mock_agent
        agent.thread = MagicMock()  # Mock thread

        chunks = []
        async for chunk in agent.send_message_stream("test"):
            chunks.append(chunk)

        # Should handle the AttributeError gracefully and not yield any chunks
        assert len(chunks) == 0


class TestEdgeCases:
    """Test suite for edge cases."""

    @pytest.mark.asyncio
    async def test_empty_message_to_agent(self):
        """Test sending empty message to agent."""
        agent = Agent(role="test")

        chunks = []
        async for chunk in agent.send_message_stream(""):
            chunks.append(chunk)

        # Should still work (stub agent ignores message content)
        assert len(chunks) == 5

    @pytest.mark.asyncio
    async def test_very_long_message_to_agent(self):
        """Test sending very long message to agent."""
        agent = Agent(role="test")

        long_message = "x" * 10000  # 10KB message
        chunks = []
        async for chunk in agent.send_message_stream(long_message):
            chunks.append(chunk)

        # Should still work (stub agent ignores message content)
        assert len(chunks) == 5

    @pytest.mark.asyncio
    async def test_unicode_message_to_agent(self):
        """Test sending unicode message to agent."""
        agent = Agent(role="test")

        unicode_message = "Hello 世界! 🌍 Ñoño"
        chunks = []
        async for chunk in agent.send_message_stream(unicode_message):
            chunks.append(chunk)

        # Should still work (stub agent ignores message content)
        assert len(chunks) == 5

    @pytest.mark.asyncio
    async def test_multiple_resets_on_agent(self):
        """Test multiple consecutive resets on agent."""
        agent = Agent(role="test")

        # Multiple resets should not cause issues
        await agent.reset()
        await agent.reset()
        await agent.reset()

        # Agent should still work after resets
        chunks = []
        async for chunk in agent.send_message_stream("test after resets"):
            chunks.append(chunk)

        assert len(chunks) == 5

    @pytest.mark.asyncio
    async def test_service_with_invalid_project_id(self):
        """Test service operations with invalid project IDs."""
        agent = Agent(role="test")
        repository = InMemoryProjectRepository()
        service = ForgebaseService(agent, repository)

        from forgebase.core.exceptions import ProjectNotFoundError

        # Invalid UUID format
        with pytest.raises(ValueError):  # UUID parsing error
            await service.get_project("not-a-uuid")

        # Valid UUID but non-existent project
        with pytest.raises(ProjectNotFoundError):
            await service.get_project("12345678-1234-1234-1234-123456789012")

    @pytest.mark.asyncio
    async def test_service_project_operations_with_empty_strings(self):
        """Test service project operations with empty/invalid strings."""
        agent = Agent(role="test")
        repository = InMemoryProjectRepository()
        service = ForgebaseService(agent, repository)

        # Empty project name should be handled by validation
        # Note: Our current implementation allows empty names, but this could be changed
        project = await service.create_project("")
        assert project.name == ""

        # Empty PRD should work
        project = await service.create_project("Test", "")
        assert project.prd == ""
