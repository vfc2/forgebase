"""Core domain entities."""

from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Project:
    """
    Represents a project in the system.

    A project is an entity with a name and creation timestamp,
    which can be used to organize conversations and work.
    """

    id: UUID
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, name: str) -> "Project":
        """
        Create a new project with generated ID and current timestamp.

        Args:
            name: The name of the project.

        Returns:
            A new Project instance.
        """
        now = datetime.now(UTC)
        return cls(id=uuid4(), name=name, created_at=now, updated_at=None)

    def update_name(self, name: str) -> None:
        """
        Update the project name and set updated timestamp.

        Args:
            name: The new name for the project.
        """
        self.name = name
        self.updated_at = datetime.now(UTC)
