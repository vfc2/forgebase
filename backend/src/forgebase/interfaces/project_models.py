"""Pydantic models for project API."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    """Request model for creating a project."""

    name: str = Field(..., min_length=1, max_length=255, description="The project name")


class ProjectUpdateRequest(BaseModel):
    """Request model for updating a project."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="The new project name"
    )


class ProjectResponse(BaseModel):
    """Response model for project data."""

    id: UUID = Field(..., description="The project ID")
    name: str = Field(..., description="The project name")
    created_at: datetime = Field(..., description="When the project was created")
    updated_at: Optional[datetime] = Field(
        None, description="When the project was last updated"
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True
