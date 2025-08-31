"""Tests for the SKAgent."""

# pylint: disable=duplicate-code

from unittest.mock import MagicMock, patch

import pytest

from forgebase.infrastructure import sk_agent


class TestSKAgent:
    """Test suite for SKAgent."""

    def test_sk_agent_initialization(self):
        """Test that SKAgent initializes with correct parameters."""
        endpoint = "https://test.openai.azure.com/"
        api_key = "test-key"
        deployment_name = "test-deployment"

        with patch(
            "forgebase.infrastructure.sk_agent.ChatCompletionAgent"
        ) as mock_agent, patch(
            "forgebase.infrastructure.sk_agent.AzureChatCompletion"
        ) as mock_azure:

            agent = sk_agent.SKAgent(
                endpoint=endpoint, api_key=api_key, deployment_name=deployment_name
            )

            # Verify agent was created
            assert agent is not None
            assert agent.thread is None

            # Verify Azure service was created with correct params
            mock_azure.assert_called_once_with(
                deployment_name=deployment_name,
                endpoint=endpoint,
                api_key=api_key,
            )

            # Verify ChatCompletionAgent was created with the service
            mock_agent.assert_called_once()
            call_args = mock_agent.call_args
            assert call_args[1]["name"] == "forgebase-agent"
            assert call_args[1]["instructions"] == "You are a helpful chatbot."
            assert call_args[1]["service"] == mock_azure.return_value

    @pytest.mark.asyncio
    async def test_send_message_stream_creates_thread(self):
        """Test that sending a message creates a thread if none exists."""
        with patch(
            "forgebase.infrastructure.sk_agent.ChatCompletionAgent"
        ) as mock_agent_class, patch(
            "forgebase.infrastructure.sk_agent.AzureChatCompletion"
        ), patch(
            "forgebase.infrastructure.sk_agent.ChatHistoryAgentThread"
        ) as mock_thread_class:

            # Setup mocks
            mock_agent_instance = MagicMock()
            mock_agent_class.return_value = mock_agent_instance
            mock_thread_instance = MagicMock()
            mock_thread_class.return_value = mock_thread_instance

            # Mock the streaming response
            mock_response = MagicMock()
            mock_response.content.content = "test response"

            # Create a proper async generator with call tracking
            call_args_list = []

            async def mock_stream(*args, **kwargs):
                call_args_list.append((args, kwargs))
                yield mock_response

            mock_agent_instance.invoke_stream = mock_stream

            agent = sk_agent.SKAgent("endpoint", "key", "deployment")

            # Verify thread is None initially
            assert agent.thread is None

            # Send message and collect response
            chunks = []
            async for chunk in agent.send_message_stream("hello"):
                chunks.append(chunk)

            # Verify thread was created
            mock_thread_class.assert_called_once()
            assert agent.thread == mock_thread_instance

            # Verify agent was called with correct parameters
            assert len(call_args_list) == 1
            _, kwargs = call_args_list[0]
            assert kwargs["messages"] == "hello"
            assert kwargs["thread"] == mock_thread_instance

            # Verify response was yielded
            assert chunks == ["test response"]

    @pytest.mark.asyncio
    async def test_send_message_stream_reuses_thread(self):
        """Test that subsequent messages reuse the existing thread."""
        with patch(
            "forgebase.infrastructure.sk_agent.ChatCompletionAgent"
        ) as mock_agent_class, patch(
            "forgebase.infrastructure.sk_agent.AzureChatCompletion"
        ), patch(
            "forgebase.infrastructure.sk_agent.ChatHistoryAgentThread"
        ) as mock_thread_class:

            # Setup mocks
            mock_agent_instance = MagicMock()
            mock_agent_class.return_value = mock_agent_instance
            mock_thread_instance = MagicMock()
            mock_thread_class.return_value = mock_thread_instance

            # Mock the streaming response
            mock_response = MagicMock()
            mock_response.content.content = "response"

            # Track calls
            call_args_list = []

            async def mock_stream(*args, **kwargs):
                call_args_list.append((args, kwargs))
                yield mock_response

            mock_agent_instance.invoke_stream = mock_stream

            agent = sk_agent.SKAgent("endpoint", "key", "deployment")

            # Send first message
            async for _ in agent.send_message_stream("hello"):
                pass

            # Send second message
            async for _ in agent.send_message_stream("world"):
                pass

            # Verify thread was created only once
            mock_thread_class.assert_called_once()

            # Verify both calls used the same thread
            assert len(call_args_list) == 2
            _, kwargs1 = call_args_list[0]
            _, kwargs2 = call_args_list[1]
            assert kwargs1["thread"] == mock_thread_instance
            assert kwargs2["thread"] == mock_thread_instance

    @pytest.mark.asyncio
    async def test_send_message_stream_filters_empty_content(self):
        """Test that empty or None content is filtered out."""
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

            # Mock responses with mixed content
            responses = []

            # Response with content
            response1 = MagicMock()
            response1.content.content = "good"
            responses.append(response1)

            # Response with None content
            response2 = MagicMock()
            response2.content = None
            responses.append(response2)

            # Response with empty content
            response3 = MagicMock()
            response3.content.content = ""
            responses.append(response3)

            # Another response with content
            response4 = MagicMock()
            response4.content.content = "content"
            responses.append(response4)

            async def mock_stream(**kwargs):
                del kwargs  # Not used in this test, but needed for signature
                for response in responses:
                    yield response

            mock_agent_instance.invoke_stream = mock_stream

            agent = sk_agent.SKAgent("endpoint", "key", "deployment")

            # Collect all chunks
            chunks = []
            async for chunk in agent.send_message_stream("hello"):
                chunks.append(chunk)

            # Verify only non-empty content was yielded
            assert chunks == ["good", "content"]

    @pytest.mark.asyncio
    async def test_reset_clears_thread(self):
        """Test that reset clears the conversation thread."""
        with patch("forgebase.infrastructure.sk_agent.ChatCompletionAgent"), patch(
            "forgebase.infrastructure.sk_agent.AzureChatCompletion"
        ):

            agent = sk_agent.SKAgent("endpoint", "key", "deployment")

            # Set a thread manually
            agent.thread = MagicMock()
            assert agent.thread is not None

            # Reset
            await agent.reset()

            # Verify thread is cleared
            assert agent.thread is None
