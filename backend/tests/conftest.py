"""Pytest configuration and fixtures."""

import pytest

from forgebase.infrastructure.agent import Agent


@pytest.fixture
def stub_agent_fixture() -> Agent:
    """Provides an Agent instance in stub mode (no credentials)."""
    return Agent(role="test")
