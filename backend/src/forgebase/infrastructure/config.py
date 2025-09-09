"""Simplified configuration."""

import os
from pathlib import Path
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
        path = Path(__file__).parent.parent / "prompts" / "prd.system.md"
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "You are a helpful PRD facilitator."
