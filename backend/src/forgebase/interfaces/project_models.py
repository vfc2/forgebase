"""Pydantic models for project API."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    """Request model for creating a project."""

    name: str = Field(..., min_length=1, max_length=255, description="The project name")
    prd: str = Field(default="", description="The PRD content for the project")


class ProjectUpdateRequest(BaseModel):
    """Request model for updating a project."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="The new project name"
    )
    prd: str = Field(default="", description="The new PRD content for the project")


class ProjectUpdateNameRequest(BaseModel):
    """Request model for updating only a project's name."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="The new project name"
    )


class ProjectUpdatePRDRequest(BaseModel):
    """Request model for updating only a project's PRD content."""

    prd: str = Field(..., description="The new PRD content for the project")


class ProjectResponse(BaseModel):
    """Response model for project data."""

    model_config = {"from_attributes": True, "populate_by_name": True}

    id: UUID = Field(..., description="The project ID")
    name: str = Field(..., description="The project name")
    prd: str = Field(..., description="The PRD content for the project")
    created_at: datetime = Field(..., description="When the project was created")
    updated_at: Optional[datetime] = Field(
        None, description="When the project was last updated"
    )
