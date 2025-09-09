"""Tests for the unified service layer."""

from uuid import uuid4
import pytest

from forgebase.core.service import ForgebaseService
from forgebase.core.exceptions import ProjectNotFoundError
from forgebase.infrastructure.stub_agent import StubAgent
from forgebase.infrastructure.project_repository import InMemoryProjectRepository


class TestForgebaseService:
    """Test the unified ForgebaseService."""

    @pytest.fixture
    def service(self):
        """Create a service for testing."""
        agent = StubAgent(role="test_agent")  # Use StubAgent for testing
        repository = InMemoryProjectRepository()
        return ForgebaseService(agent, repository)

    @pytest.mark.asyncio
    async def test_send_message_stream(self, service):
        """Test that the service can stream messages."""
        message = "Hello, test!"
        chunks = []
        async for chunk in service.send_message_stream(message):
            chunks.append(chunk)

        # Stub agent should return some response chunks
        assert len(chunks) > 0
        response = "".join(chunks)
        assert len(response) > 0
        assert "Hello!" in response  # StubAgent responds to greetings

    @pytest.mark.asyncio
    async def test_reset_chat(self, service):
        """Test that the service can reset chat."""
        # Should not raise an exception
        await service.reset_chat()

    @pytest.mark.asyncio
    async def test_create_project(self, service):
        """Test creating a project."""
        project = await service.create_project("Test Project", "Test PRD")

        assert project.name == "Test Project"
        assert project.prd == "Test PRD"
        assert project.id is not None

    @pytest.mark.asyncio
    async def test_get_project(self, service):
        """Test getting a project."""
        # Create a project first
        created_project = await service.create_project("Test Project")

        # Get it back
        retrieved_project = await service.get_project(str(created_project.id))

        assert retrieved_project.id == created_project.id
        assert retrieved_project.name == "Test Project"

    @pytest.mark.asyncio
    async def test_get_project_not_found(self, service):
        """Test getting a non-existent project."""
        with pytest.raises(ProjectNotFoundError):
            await service.get_project(str(uuid4()))

    @pytest.mark.asyncio
    async def test_list_projects(self, service):
        """Test listing projects."""
        # Start with empty list
        projects = await service.list_projects()
        assert len(projects) == 0

        # Add some projects
        await service.create_project("Project 1")
        await service.create_project("Project 2")

        projects = await service.list_projects()
        assert len(projects) == 2
        project_names = {p.name for p in projects}
        assert project_names == {"Project 1", "Project 2"}

    @pytest.mark.asyncio
    async def test_update_project(self, service):
        """Test updating a project."""
        # Create a project
        project = await service.create_project("Original Name", "Original PRD")

        # Update it
        updated_project = await service.update_project(
            str(project.id), name="New Name", prd="New PRD"
        )

        assert updated_project.id == project.id
        assert updated_project.name == "New Name"
        assert updated_project.prd == "New PRD"
        assert updated_project.updated_at is not None

    @pytest.mark.asyncio
    async def test_update_project_partial(self, service):
        """Test updating only some fields of a project."""
        # Create a project
        project = await service.create_project("Original Name", "Original PRD")

        # Update only name
        updated_project = await service.update_project(str(project.id), name="New Name")

        assert updated_project.name == "New Name"
        assert updated_project.prd == "Original PRD"  # Should remain unchanged

    @pytest.mark.asyncio
    async def test_update_project_not_found(self, service):
        """Test updating a non-existent project."""
        with pytest.raises(ProjectNotFoundError):
            await service.update_project(str(uuid4()), name="New Name")

    @pytest.mark.asyncio
    async def test_delete_project(self, service):
        """Test deleting a project."""
        # Create a project
        project = await service.create_project("Test Project")

        # Delete it
        deleted = await service.delete_project(str(project.id))
        assert deleted is True

        # Try to get it (should fail)
        with pytest.raises(ProjectNotFoundError):
            await service.get_project(str(project.id))

    @pytest.mark.asyncio
    async def test_delete_project_not_found(self, service):
        """Test deleting a non-existent project."""
        deleted = await service.delete_project(str(uuid4()))
        assert deleted is False

    @pytest.mark.asyncio
    async def test_create_project_empty_name(self, service):
        """Test creating a project with empty name."""
        with pytest.raises(ValueError, match="Project name cannot be empty"):
            await service.create_project("")

        with pytest.raises(ValueError, match="Project name cannot be empty"):
            await service.create_project("   ")  # Whitespace only

    @pytest.mark.asyncio
    async def test_create_project_long_name(self, service):
        """Test creating a project with too long name."""
        long_name = "x" * 256  # Exceeds 255 character limit
        with pytest.raises(ValueError, match="Project name too long"):
            await service.create_project(long_name)

    @pytest.mark.asyncio
    async def test_update_project_empty_name(self, service):
        """Test updating a project with empty name."""
        project = await service.create_project("Original Name")

        with pytest.raises(ValueError, match="Project name cannot be empty"):
            await service.update_project(str(project.id), name="")

        with pytest.raises(ValueError, match="Project name cannot be empty"):
            await service.update_project(str(project.id), name="   ")

    @pytest.mark.asyncio
    async def test_update_project_long_name(self, service):
        """Test updating a project with too long name."""
        project = await service.create_project("Original Name")
        long_name = "x" * 256  # Exceeds 255 character limit

        with pytest.raises(ValueError, match="Project name too long"):
            await service.update_project(str(project.id), name=long_name)

    @pytest.mark.asyncio
    async def test_invalid_project_id_format(self, service):
        """Test operations with invalid project ID format."""
        with pytest.raises(ProjectNotFoundError, match="Invalid project ID format"):
            await service.get_project("not-a-uuid")

        with pytest.raises(ProjectNotFoundError, match="Invalid project ID format"):
            await service.update_project("not-a-uuid", name="New Name")

        with pytest.raises(ProjectNotFoundError, match="Invalid project ID format"):
            await service.delete_project("not-a-uuid")
