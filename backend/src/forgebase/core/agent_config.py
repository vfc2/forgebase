"""Agent configuration and registry."""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum


class AgentRole(Enum):
    """Defined agent roles in the system."""

    PRD_FACILITATOR = "prd_facilitator"
    TECHNICAL_ANALYST = "technical_analyst"
    DATA_COLLECTOR = "data_collector"
    REQUIREMENTS_VALIDATOR = "requirements_validator"


@dataclass
class AgentConfig:
    """Configuration for an agent type."""

    role: AgentRole
    name: str
    instructions_file: str
    tools: List[str]
    description: str
    is_user_facing: bool = False


# Registry of available agent configurations
AGENT_CONFIGS: Dict[AgentRole, AgentConfig] = {
    AgentRole.PRD_FACILITATOR: AgentConfig(
        role=AgentRole.PRD_FACILITATOR,
        name="PRD Facilitator",
        instructions_file="prompts/prd.system.md",
        tools=["save_draft_prd", "save_completed_prd"],
        description="Interactive agent for conversational PRD creation",
        is_user_facing=True,
    ),
    AgentRole.TECHNICAL_ANALYST: AgentConfig(
        role=AgentRole.TECHNICAL_ANALYST,
        name="Technical Analyst",
        instructions_file="prompts/technical_analyst.system.md",
        tools=["analyze_codebase", "suggest_architecture", "get_project_data"],
        description="Analyzes technical requirements and suggests solutions",
        is_user_facing=False,
    ),
    AgentRole.DATA_COLLECTOR: AgentConfig(
        role=AgentRole.DATA_COLLECTOR,
        name="Data Collector",
        instructions_file="prompts/data_collector.system.md",
        tools=["fetch_project_data", "gather_requirements", "get_project_data"],
        description="Collects and organizes project data from repositories",
        is_user_facing=False,
    ),
    AgentRole.REQUIREMENTS_VALIDATOR: AgentConfig(
        role=AgentRole.REQUIREMENTS_VALIDATOR,
        name="Requirements Validator",
        instructions_file="prompts/requirements_validator.system.md",
        tools=["validate_requirements", "check_completeness", "get_project_data"],
        description="Validates and ensures completeness of requirements",
        is_user_facing=False,
    ),
}


def get_agent_config(role: AgentRole) -> AgentConfig:
    """Get configuration for a specific agent role."""
    return AGENT_CONFIGS[role]


def get_user_facing_roles() -> List[AgentRole]:
    """Get all agent roles that are user-facing."""
    return [role for role, config in AGENT_CONFIGS.items() if config.is_user_facing]


def get_background_roles() -> List[AgentRole]:
    """Get all agent roles that operate in the background."""
    return [role for role, config in AGENT_CONFIGS.items() if not config.is_user_facing]
