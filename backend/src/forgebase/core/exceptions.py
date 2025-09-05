"""Core domain exceptions."""


class ProjectError(Exception):
    """Base exception for project-related errors."""


class ProjectNotFoundError(ProjectError):
    """Raised when a project is not found."""

    def __init__(self, project_id: str):
        """
        Initialize the exception.

        Args:
            project_id: The ID of the project that was not found.
        """
        super().__init__(f"Project with ID {project_id} not found")
        self.project_id = project_id


class ProjectAlreadyExistsError(ProjectError):
    """Raised when trying to create a project that already exists."""

    def __init__(self, project_id: str):
        """
        Initialize the exception.

        Args:
            project_id: The ID of the project that already exists.
        """
        super().__init__(f"Project with ID {project_id} already exists")
        self.project_id = project_id
