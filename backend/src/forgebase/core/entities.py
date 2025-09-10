"""Core domain entities."""

from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Project:
    """
    Represents a project in the system.

    A project is an entity with a name, PRD content, user ownership, and creation timestamp,
    which can be used to organize conversations and work.
    """

    id: UUID
    user_id: str
    name: str
    prd: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, user_id: str, name: str, prd: str = "") -> "Project":
        """
        Create a new project with generated ID and current timestamp.

        Args:
            user_id: The ID of the user who owns this project.
            name: The name of the project.
            prd: The PRD content for the project (defaults to empty string).

        Returns:
            A new Project instance.
        """
        now = datetime.now(UTC)
        return cls(id=uuid4(), user_id=user_id, name=name, prd=prd, created_at=now, updated_at=None)

    def update_name(self, name: str) -> None:
        """
        Update the project name and set updated timestamp.

        Args:
            name: The new name for the project.
        """
        self.name = name
        self.updated_at = datetime.now(UTC)

    def update_prd(self, prd: str) -> None:
        """
        Update the project PRD content and set updated timestamp.

        Args:
            prd: The new PRD content for the project.
        """
        self.prd = prd
        self.updated_at = datetime.now(UTC)
