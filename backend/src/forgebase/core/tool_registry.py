"""Tool registry for agent capabilities."""

from typing import Dict, Any, Protocol
from abc import abstractmethod


class ToolProtocol(Protocol):
    """Protocol for agent tools."""

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the tool with given parameters."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name identifier."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for the agent."""
        ...


class ToolRegistry:
    """Registry for managing agent tools."""

    def __init__(self):
        self._tools: Dict[str, ToolProtocol] = {}

    def register(self, tool: ToolProtocol) -> None:
        """Register a tool in the registry."""
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> ToolProtocol:
        """Get a tool by name."""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry")
        return self._tools[name]

    def get_tools_for_agent(self, tool_names: list[str]) -> Dict[str, ToolProtocol]:
        """Get multiple tools for an agent."""
        return {name: self.get_tool(name) for name in tool_names}

    def list_available_tools(self) -> list[str]:
        """List all available tool names."""
        return list(self._tools.keys())


# Global tool registry instance
tool_registry = ToolRegistry()
