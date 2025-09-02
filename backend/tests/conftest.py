"""Pytest configuration and fixtures."""

import pytest

from forgebase.infrastructure import stub_agent


@pytest.fixture
def stub_agent_fixture() -> stub_agent.StubAgent:
    """Provides a StubAgent instance."""
    return stub_agent.StubAgent()
