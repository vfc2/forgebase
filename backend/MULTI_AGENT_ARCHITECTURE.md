# Multi-Agent Architecture

This document describes the multi-agent architecture implemented in Forgebase, which extends the original single-agent system to support multiple specialized agents while maintaining simplicity and extensibility.

## Architecture Overview

The multi-agent system is built on these key principles:

1. **Single User-Facing Agent**: Only the PRD Facilitator interacts directly with users
2. **Specialized Background Agents**: Other agents perform specific tasks behind the scenes
3. **Tool-Based Architecture**: Agents access data and functionality through registered tools
4. **Repository Access**: All tools can access project data via the repository pattern
5. **Simple Configuration**: Agent roles, prompts, and tools are configured declaratively

## Components

### Core Components

- **`AgentPort`** - Protocol defining the agent interface (enhanced with role and tools)
- **`AgentConfig`** - Configuration dataclass for agent roles, prompts, and tools
- **`ToolRegistry`** - Central registry for managing agent tools
- **`MultiAgentService`** - Main orchestration service

### Agent Roles

1. **PRD Facilitator** (`prd_facilitator`)
   - **User-facing**: Yes
   - **Purpose**: Interactive conversational PRD creation
   - **Tools**: `save_draft_prd`, `save_completed_prd`
   - **Prompt**: `prompts/prd.system.md`

2. **Technical Analyst** (`technical_analyst`)
   - **User-facing**: No
   - **Purpose**: Analyze technical requirements and suggest solutions
   - **Tools**: `analyze_codebase`, `suggest_architecture`, `get_project_data`
   - **Prompt**: `prompts/technical_analyst.system.md`

3. **Data Collector** (`data_collector`)
   - **User-facing**: No
   - **Purpose**: Collect and organize project data from repositories
   - **Tools**: `fetch_project_data`, `gather_requirements`, `get_project_data`
   - **Prompt**: `prompts/data_collector.system.md`

4. **Requirements Validator** (`requirements_validator`)
   - **User-facing**: No
   - **Purpose**: Validate and ensure completeness of requirements
   - **Tools**: `validate_requirements`, `check_completeness`, `get_project_data`
   - **Prompt**: `prompts/requirements_validator.system.md`

### Tool System

Tools provide agents with capabilities to access data and perform actions:

- **`ProjectDataTool`** - Access project data from repository
- **`SaveDraftPRDTool`** - Save draft PRD documents
- **`SaveCompletedPRDTool`** - Save completed PRD documents
- **`AnalyzeCodebaseTool`** - Analyze codebase structure
- **`ValidateRequirementsTool`** - Validate requirements completeness

## Usage Examples

### Basic Setup

```python
from forgebase.infrastructure.config import get_multi_agent_service

# Get the multi-agent service
service = get_multi_agent_service()

# Main conversation (user-facing)
async for chunk in service.send_message_stream("I want to create a new app"):
    print(chunk, end="", flush=True)
```

### Background Agent Usage

```python
# Technical analysis (background)
analysis = await service.analyze_technical_requirements(
    project_id="project-123",
    requirements="Real-time mobile app with offline sync"
)

# Data collection (background)
data = await service.collect_project_data("project-123")

# Requirements validation (background)
validation = await service.validate_requirements("User can login with email")
```

### Adding New Agents

1. **Define the role** in `core/agent_config.py`:
```python
class AgentRole(Enum):
    NEW_ROLE = "new_role"

AGENT_CONFIGS[AgentRole.NEW_ROLE] = AgentConfig(
    role=AgentRole.NEW_ROLE,
    name="New Agent",
    instructions_file="prompts/new_agent.system.md",
    tools=["tool1", "tool2"],
    description="Description of the new agent",
    is_user_facing=False,
)
```

2. **Create the prompt file** at `prompts/new_agent.system.md`

3. **Create any new tools** in `infrastructure/tools.py`

4. **Register tools** in `infrastructure/config.py`

### Adding New Tools

1. **Create the tool class**:
```python
class NewTool:
    def __init__(self, project_repository: ProjectRepositoryPort):
        self.project_repository = project_repository
    
    async def execute(self, **kwargs: Any) -> Any:
        # Tool implementation
        return {"result": "success"}
    
    @property
    def name(self) -> str:
        return "new_tool"
    
    @property
    def description(self) -> str:
        return "Description of the new tool"
```

2. **Register the tool** in `config.py`:
```python
def _register_tools(repo: ports.ProjectRepositoryPort) -> None:
    new_tool = tools.NewTool(repo)
    tool_registry.register(new_tool)
```

3. **Add to agent configurations** that should use it

## Integration with Existing Code

The multi-agent system is designed to be backward compatible:

- **`get_agent()`** still works for legacy code
- **`get_multi_agent_service()`** is the new recommended approach
- **Existing interfaces** (CLI, Web) can be updated incrementally

### Updating ChatService

```python
# Old approach
chat_service = ChatService(get_agent())

# New approach
multi_agent_service = get_multi_agent_service()
# Use multi_agent_service.send_message_stream() instead
```

## Benefits

1. **Separation of Concerns**: Each agent has a specific, well-defined role
2. **Extensibility**: Easy to add new agents and tools
3. **Maintainability**: Clear boundaries and responsibilities
4. **Repository Access**: All agents can access project data through tools
5. **Backward Compatibility**: Existing code continues to work
6. **Simple Configuration**: Declarative setup of agents and capabilities

## Demo

Run the demo script to see the multi-agent system in action:

```bash
python demo_multi_agent.py
```

This demonstrates:
- Main conversational agent interaction
- Background technical analysis
- Data collection capabilities
- Requirements validation

## Future Enhancements

1. **Tool Calling Integration**: Full Semantic Kernel function calling support
2. **Agent Orchestration**: Smart routing between agents based on user intent
3. **Persistent State**: Agent conversation state persistence
4. **Performance Optimization**: Agent caching and request optimization
5. **Monitoring**: Agent interaction logging and metrics
