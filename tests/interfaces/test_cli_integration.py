"""Integration tests for CLI functionality."""

from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from forgebase.interfaces.cli import main


class TestCLIIntegration:
    """Test suite for CLI integration."""

    def test_main_command_group_exists(self):
        """Test that the main command group is accessible."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Forgebase CLI" in result.output

    def test_chat_command_exists(self):
        """Test that the chat command is available."""
        runner = CliRunner()
        result = runner.invoke(main, ["chat", "--help"])
        assert result.exit_code == 0
        assert "Starts an interactive chat session" in result.output
        assert "--debug" in result.output

    @patch("forgebase.interfaces.cli.asyncio.run")
    @patch("forgebase.interfaces.cli.config.get_agent")
    @patch("forgebase.interfaces.cli.logging_config.setup_logging")
    def test_chat_command_setup(
        self, mock_setup_logging, mock_get_agent, mock_asyncio_run
    ):
        """Test that chat command sets up dependencies correctly."""
        # Setup mocks
        mock_agent = MagicMock()
        mock_get_agent.return_value = mock_agent

        runner = CliRunner()
        runner.invoke(main, ["chat"])

        # Verify setup was called correctly
        mock_setup_logging.assert_called_once_with(False)  # debug=False by default
        mock_get_agent.assert_called_once()
        mock_asyncio_run.assert_called_once()

    @patch("forgebase.interfaces.cli.asyncio.run")
    @patch("forgebase.interfaces.cli.config.get_agent")
    @patch("forgebase.interfaces.cli.logging_config.setup_logging")
    def test_chat_command_debug_flag(
        self, mock_setup_logging, mock_get_agent, mock_asyncio_run
    ):
        """Test that chat command respects debug flag."""
        # Setup mocks
        mock_agent = MagicMock()
        mock_get_agent.return_value = mock_agent

        runner = CliRunner()
        runner.invoke(main, ["chat", "--debug"])

        # Verify debug logging was enabled
        mock_setup_logging.assert_called_once_with(True)  # debug=True
        mock_get_agent.assert_called_once()
        mock_asyncio_run.assert_called_once()
