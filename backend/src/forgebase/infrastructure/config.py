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


def get_chat_service() -> ChatService:
    """Get the chat service.

    Returns:
        Configured ChatService instance
    """
    agent = _create_agent()
    return ChatService(agent)


def get_project_service() -> ProjectService:
    """Get the project service.

    Returns:
        Configured ProjectService instance
    """
    repository = InMemoryProjectRepository()
    return ProjectService(repository)


def _create_agent() -> AgentPort:
    """Create an agent based on available configuration.

    Returns:
        Agent if Azure OpenAI config is available, else StubAgent
    """
    # Create tools
    project_service = get_project_service()
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
