"""Simplified configuration."""

import os
from dotenv import load_dotenv

from forgebase.core.service import ForgebaseService
from forgebase.infrastructure.agent import Agent
from forgebase.infrastructure.project_repository import InMemoryProjectRepository

load_dotenv()


def get_service() -> ForgebaseService:
    """Get the main forgebase service.

    Returns:
        Configured ForgebaseService instance
    """
    # Create agent
    agent = Agent(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        instructions=_load_prd_instructions(),
        role="prd_facilitator",
    )

    # Create repository
    repository = InMemoryProjectRepository()

    return ForgebaseService(agent, repository)


def _load_prd_instructions() -> str:
    """Load PRD facilitator instructions.

    Returns:
        Instructions text for the PRD facilitator agent
    """
    try:
        from pathlib import Path

        path = Path(__file__).parent.parent / "prompts" / "prd.system.md"
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "You are a helpful PRD facilitator."


# Legacy compatibility functions - deprecated, use get_service() instead
def get_agent():
    """Legacy function - use get_service() instead."""
    # Create agent directly for backwards compatibility
    return Agent(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        instructions=_load_prd_instructions(),
        role="prd_facilitator",
    )


def get_multi_agent_service():
    """Legacy function - use get_service() instead."""
    return get_service()
