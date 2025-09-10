"""Tool interface for agent plugins."""

from typing import Protocol
from semantic_kernel import Kernel


class ToolPort(Protocol):
    """Interface for agent tools that can be registered as SK plugins."""

    @property
    def plugin_name(self) -> str:
        """Name for the SK plugin."""
        ...

    def register_with_kernel(self, kernel: Kernel) -> None:
        """Register this tool's functions with the SK kernel."""
        ...

    def set_project_context(self, project_id: str | None) -> None:
        """Set the current project context for operations."""
        ...
