"""PRD management tools for agents."""

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

from forgebase.core.tool_port import ToolPort
from forgebase.core.project_service import ProjectService


class PRDTools(ToolPort):
    """PRD management tools for agents."""

    def __init__(
        self, project_service: ProjectService, current_project_id: str | None = None, user_id: str = "test-user-123"
    ):
        self._project_service = project_service
        self._current_project_id = current_project_id
        self._user_id = user_id

    @property
    def plugin_name(self) -> str:
        return "PRDTools"

    def register_with_kernel(self, kernel: Kernel) -> None:
        """Register PRD functions with the kernel."""
        kernel.add_plugin(self, plugin_name=self.plugin_name)

    def set_project_context(self, project_id: str | None) -> None:
        """Set the current project context for operations."""
        print(f"DEBUG PRDTools: Setting project context to: {project_id}")
        self._current_project_id = project_id

    @kernel_function(
        description="Update the PRD content of the current project", name="update_prd"
    )
    async def update_prd(self, prd_content: str) -> str:
        """Update the PRD content of the current project.

        Args:
            prd_content: The new PRD content to save

        Returns:
            Success message confirming the update
        """
        print(
            f"DEBUG PRDTools.update_prd: current_project_id = {self._current_project_id}")
        if not self._current_project_id:
            return "Error: No project context set. Please select a project first."

        try:
            project = await self._project_service.update_project(
                self._current_project_id, self._user_id, prd=prd_content
            )
            return f"PRD updated successfully for project '{project.name}'"
        except ValueError as e:
            return f"Error updating PRD: {str(e)}"
