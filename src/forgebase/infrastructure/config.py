"""Configuration and dependency setup."""

import os
from dotenv import load_dotenv

from forgebase.core import ports
from forgebase.infrastructure import sk_agent, stub_agent

# Load environment variables from .env file
load_dotenv()


def get_agent() -> ports.AgentPort:
    """
    Select and configure the agent based on environment variables.

    Returns:
        AgentPort: An instance of the selected agent.
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    if not endpoint or not api_key or not deployment_name:
        return stub_agent.StubAgent()

    return sk_agent.SKAgent(
        endpoint=endpoint,
        api_key=api_key,
        deployment_name=deployment_name,
    )  # type: ignore
