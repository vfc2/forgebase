"""Tests for logging configuration."""

import logging
from unittest.mock import patch, MagicMock

from forgebase.infrastructure import logging_config


class TestLoggingConfig:
    """Test suite for logging configuration."""

    @patch("forgebase.infrastructure.logging_config.logging.basicConfig")
    def test_setup_logging_debug_mode(self, mock_basic_config):
        """Test that debug mode sets DEBUG level."""
        logging_config.setup_logging(debug=True)

        # Verify basicConfig was called with DEBUG level
        mock_basic_config.assert_called_once_with(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    @patch("forgebase.infrastructure.logging_config.logging.basicConfig")
    def test_setup_logging_production_mode(self, mock_basic_config):
        """Test that production mode sets WARNING level."""
        logging_config.setup_logging(debug=False)

        # Verify basicConfig was called with WARNING level
        mock_basic_config.assert_called_once_with(
            level=logging.WARNING,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    @patch("forgebase.infrastructure.logging_config.logging.basicConfig")
    def test_setup_logging_default_is_production(self, mock_basic_config):
        """Test that default behavior is production mode (WARNING level)."""
        logging_config.setup_logging()

        # Verify basicConfig was called with WARNING level
        mock_basic_config.assert_called_once_with(
            level=logging.WARNING,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    @patch("forgebase.infrastructure.logging_config.logging.getLogger")
    @patch("forgebase.infrastructure.logging_config.logging.basicConfig")
    def test_setup_logging_suppresses_azure_http_logging(
        self, mock_basic_config, mock_get_logger
    ):
        """Test that Azure HTTP logging is suppressed to prevent secret leakage."""
        del mock_basic_config  # Not used in this test, but patched for isolation
        mock_azure_logger = MagicMock()
        mock_get_logger.return_value = mock_azure_logger

        logging_config.setup_logging(debug=True)

        # Verify Azure HTTP logger was retrieved and set to WARNING
        mock_get_logger.assert_called_once_with(
            "azure.core.pipeline.policies.http_logging_policy"
        )
        mock_azure_logger.setLevel.assert_called_once_with(logging.WARNING)
