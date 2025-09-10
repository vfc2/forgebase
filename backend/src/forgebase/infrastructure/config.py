"""Simplified configuration."""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

from forgebase.core.chat_service import ChatService
from forgebase.core.project_service import ProjectService
from forgebase.core.ports import AgentPort
from forgebase.core.tool_port import ToolPort
from forgebase.infrastructure.agent import Agent
from forgebase.infrastructure.stub_agent import StubAgent
from forgebase.infrastructure.project_repository import InMemoryProjectRepository
from forgebase.tools.prd_tools import PRDTools

load_dotenv()


# Global singleton repository instance
_project_repository: InMemoryProjectRepository | None = None


def get_project_repository() -> InMemoryProjectRepository:
    """Get the shared project repository instance.

    Returns:
        Shared InMemoryProjectRepository instance
    """
    global _project_repository
    if _project_repository is None:
        _project_repository = InMemoryProjectRepository()
    return _project_repository


def get_chat_service() -> ChatService:
    """Get the chat service.

    Returns:
        Configured ChatService instance
    """
    # Use the shared project service to ensure same repository
    project_service = get_project_service()
    agent = _create_agent(project_service)
    return ChatService(agent)


def get_project_service() -> ProjectService:
    """Get the project service.

    Returns:
        Configured ProjectService instance
    """
    repository = get_project_repository()
    return ProjectService(repository)


def _create_agent(project_service: ProjectService) -> AgentPort:
    """Create an agent based on available configuration.

    Args:
        project_service: Shared project service instance

    Returns:
        Agent if Azure OpenAI config is available, else StubAgent
    """
    # Create tools with the shared project service
    prd_tools = PRDTools(project_service)
    tools: List[ToolPort] = [prd_tools]

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    if endpoint and api_key and deployment_name:
        return Agent(
            endpoint=endpoint,
            api_key=api_key,
            deployment_name=deployment_name,
            instructions=_load_prd_instructions(),
            role="prd_facilitator",
            tools=tools,
        )
    return StubAgent(
        instructions=_load_prd_instructions(),
        role="prd_facilitator",
        tools=tools,
    )


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
