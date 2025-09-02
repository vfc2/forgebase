"""Tests for error handling and edge cases."""

# pylint: disable=duplicate-code

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from forgebase.core import chat_service
from forgebase.infrastructure import stub_agent, sk_agent


class TestErrorHandling:
    """Test suite for error handling scenarios."""

    @pytest.mark.asyncio
    async def test_chat_service_propagates_agent_exceptions(self):
        """Test that ChatService propagates exceptions from the agent."""
        # Create a mock agent that raises an exception
        mock_agent = MagicMock()

        # Mock send_message_stream to be an async generator that raises
        async def failing_stream(user_text):
            del user_text  # Not used in this mock, but needed for signature
            raise RuntimeError("Agent failed")
            # The following line is necessary to make this an async generator
            # but will never be reached. pylint: disable=unreachable
            yield  # pragma: no cover

        mock_agent.send_message_stream = failing_stream

        service = chat_service.ChatService(agent=mock_agent)

        # Verify the exception is propagated
        with pytest.raises(RuntimeError, match="Agent failed"):
            async for _ in service.send_message_stream("test"):
                pass

    @pytest.mark.asyncio
    async def test_chat_service_reset_propagates_agent_exceptions(self):
        """Test that ChatService propagates reset exceptions from the agent."""
        # Create a mock agent that raises an exception on reset
        mock_agent = AsyncMock()
        mock_agent.reset.side_effect = RuntimeError("Reset failed")

        service = chat_service.ChatService(agent=mock_agent)

        # Verify the exception is propagated
        with pytest.raises(RuntimeError, match="Reset failed"):
            await service.reset()

    @pytest.mark.asyncio
    async def test_stub_agent_handles_concurrent_streams(self):
        """Test that StubAgent can handle multiple concurrent streams."""
        agent = stub_agent.StubAgent()

        # Start multiple concurrent streams
        stream1 = agent.send_message_stream("message1")
        stream2 = agent.send_message_stream("message2")

        # Collect results from both streams
        chunks1 = [chunk async for chunk in stream1]
        chunks2 = [chunk async for chunk in stream2]

        # Both should produce the same expected output
        expected = ["This ", "is ", "a ", "stub ", "reply."]
        assert chunks1 == expected
        assert chunks2 == expected

    @pytest.mark.asyncio
    async def test_sk_agent_handles_content_attribute_error(self):
        """Test that SKAgent gracefully handles responses without content attribute."""
        with patch(
            "forgebase.infrastructure.sk_agent.ChatCompletionAgent"
        ) as mock_agent_class, patch(
            "forgebase.infrastructure.sk_agent.AzureChatCompletion"
        ), patch(
            "forgebase.infrastructure.sk_agent.ChatHistoryAgentThread"
        ):

            # Setup mocks
            mock_agent_instance = MagicMock()
            mock_agent_class.return_value = mock_agent_instance

            # Mock a response without content attribute
            response_without_content = MagicMock()
            del response_without_content.content  # Remove the content attribute

            # Mock a normal response
            normal_response = MagicMock()
            normal_response.content.content = "valid content"

            responses = [response_without_content, normal_response]

            async def mock_stream(**kwargs):
                del kwargs  # Not used in this test, but needed for signature
                for response in responses:
                    yield response

            mock_agent_instance.invoke_stream = mock_stream

            agent = sk_agent.SKAgent("endpoint", "key", "deployment")

            # Collect chunks - should handle the AttributeError gracefully
            chunks = []
            try:
                async for chunk in agent.send_message_stream("hello"):
                    chunks.append(chunk)
            except AttributeError:
                # If an AttributeError is raised, that's a bug we need to fix
                pytest.fail("SKAgent should handle responses without content attribute")

            # Should only get the valid content
            assert chunks == ["valid content"]


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    @pytest.mark.asyncio
    async def test_empty_message_to_stub_agent(self):
        """Test that StubAgent handles empty messages."""
        agent = stub_agent.StubAgent()
        chunks = [chunk async for chunk in agent.send_message_stream("")]

        # Should still return the expected stub response
        assert chunks == ["This ", "is ", "a ", "stub ", "reply."]

    @pytest.mark.asyncio
    async def test_very_long_message_to_stub_agent(self):
        """Test that StubAgent handles very long messages."""
        agent = stub_agent.StubAgent()
        long_message = "x" * 10000  # 10KB message
        chunks = [chunk async for chunk in agent.send_message_stream(long_message)]

        # Should still return the expected stub response regardless of input
        assert chunks == ["This ", "is ", "a ", "stub ", "reply."]

    @pytest.mark.asyncio
    async def test_unicode_message_to_stub_agent(self):
        """Test that StubAgent handles Unicode messages."""
        agent = stub_agent.StubAgent()
        unicode_message = "Hello 世界 🌍 émojis"
        chunks = [chunk async for chunk in agent.send_message_stream(unicode_message)]

        # Should still return the expected stub response
        assert chunks == ["This ", "is ", "a ", "stub ", "reply."]

    @pytest.mark.asyncio
    async def test_multiple_resets_on_stub_agent(self):
        """Test that multiple resets on StubAgent work correctly."""
        agent = stub_agent.StubAgent()

        # Reset multiple times
        await agent.reset()
        await agent.reset()
        await agent.reset()

        # Should still work normally after multiple resets
        chunks = [chunk async for chunk in agent.send_message_stream("test")]
        assert chunks == ["This ", "is ", "a ", "stub ", "reply."]
