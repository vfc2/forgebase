"""Configuration and dependency setup."""

import os
from dotenv import load_dotenv

from forgebase.core import ports
from forgebase.core.multi_agent_service import MultiAgentService
from forgebase.infrastructure import sk_agent, stub_agent, project_repository
from forgebase.infrastructure import tools
from forgebase.core.tool_registry import tool_registry

# Load environment variables from .env file
load_dotenv()


def get_agent() -> ports.AgentPort:
    """
    Select and configure the agent based on environment variables.

    This is the legacy function for backward compatibility.
    Consider using get_multi_agent_service() for new implementations.

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


def get_multi_agent_service() -> MultiAgentService:
    """
    Get the multi-agent service with all configured agents.

    Returns:
        MultiAgentService: Service orchestrating multiple specialized agents.
    """
    # Set up project repository
    repo = project_repository.InMemoryProjectRepository()

    # Register tools in the global registry
    _register_tools(repo)

    # Create and return the multi-agent service
    return MultiAgentService(repo)


def _register_tools(repo: ports.ProjectRepositoryPort) -> None:
    """Register all available tools in the tool registry."""
    # Create tool instances
    project_data_tool = tools.ProjectDataTool(repo)
    save_draft_prd_tool = tools.SaveDraftPRDTool(repo)
    save_completed_prd_tool = tools.SaveCompletedPRDTool(repo)
    analyze_codebase_tool = tools.AnalyzeCodebaseTool(repo)
    validate_requirements_tool = tools.ValidateRequirementsTool(repo)
    suggest_architecture_tool = tools.SuggestArchitectureTool(repo)
    fetch_project_data_tool = tools.FetchProjectDataTool(repo)
    gather_requirements_tool = tools.GatherRequirementsTool(repo)
    check_completeness_tool = tools.CheckCompletenessTool(repo)

    # Register tools
    tool_registry.register(project_data_tool)
    tool_registry.register(save_draft_prd_tool)
    tool_registry.register(save_completed_prd_tool)
    tool_registry.register(analyze_codebase_tool)
    tool_registry.register(validate_requirements_tool)
    tool_registry.register(suggest_architecture_tool)
    tool_registry.register(fetch_project_data_tool)
    tool_registry.register(gather_requirements_tool)
    tool_registry.register(check_completeness_tool)
