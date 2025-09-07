"""Tests for core entities."""

from datetime import datetime
from uuid import UUID

from forgebase.core.entities import Project


class TestProject:
    """Test cases for the Project entity."""

    def test_create_project(self):
        """Test creating a project with the factory method."""
        name = "Test Project"
        project = Project.create(name)

        assert project.name == name
        assert project.prd == ""  # Default empty PRD
        assert isinstance(project.id, UUID)
        assert isinstance(project.created_at, datetime)
        assert project.updated_at is None

    def test_create_project_with_prd(self):
        """Test creating a project with PRD content."""
        name = "Test Project"
        prd = "This is a test PRD content"
        project = Project.create(name, prd)

        assert project.name == name
        assert project.prd == prd
        assert isinstance(project.id, UUID)
        assert isinstance(project.created_at, datetime)
        assert project.updated_at is None

    def test_create_projects_have_unique_ids(self):
        """Test that multiple projects have unique IDs."""
        project1 = Project.create("Project 1")
        project2 = Project.create("Project 2")

        assert project1.id != project2.id

    def test_update_name(self):
        """Test updating a project's name."""
        project = Project.create("Original Name")
        original_created_at = project.created_at

        new_name = "Updated Name"
        project.update_name(new_name)

        assert project.name == new_name
        assert project.created_at == original_created_at
        assert project.updated_at is not None
        assert project.updated_at >= original_created_at

    def test_update_prd(self):
        """Test updating a project's PRD content."""
        project = Project.create("Test Project")
        original_created_at = project.created_at

        new_prd = "Updated PRD content"
        project.update_prd(new_prd)

        assert project.prd == new_prd
        assert project.created_at == original_created_at
        assert project.updated_at is not None
        assert project.updated_at >= original_created_at

    def test_project_dataclass_properties(self):
        """Test that Project behaves as expected as a dataclass."""
        project1 = Project.create("Test")
        project2 = Project(
            id=project1.id,
            name=project1.name,
            prd=project1.prd,
            created_at=project1.created_at,
            updated_at=project1.updated_at,
        )

        assert project1 == project2
        assert project1 is not project2
