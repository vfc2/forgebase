"""Tests for the split service layer."""

from uuid import uuid4
import pytest

from forgebase.core.chat_service import ChatService
from forgebase.core.project_service import ProjectService
from forgebase.core.exceptions import ProjectNotFoundError
from forgebase.infrastructure.stub_agent import StubAgent
from forgebase.infrastructure.project_repository import InMemoryProjectRepository


class TestChatService:
    """Test the ChatService."""

    @pytest.fixture
    def chat_service(self):
        """Create a chat service for testing."""
        agent = StubAgent(role="test_agent")
        return ChatService(agent)

    @pytest.mark.asyncio
    async def test_send_message_stream(self, chat_service):
        """Test that the chat service can stream messages."""
        message = "Hello, test!"
        chunks = []
        async for chunk in chat_service.send_message_stream(message):
            chunks.append(chunk)

        # Stub agent should return some response chunks
        assert len(chunks) > 0
        response = "".join(chunks)
        assert len(response) > 0
        assert "Hello!" in response  # StubAgent responds to greetings

    @pytest.mark.asyncio
    async def test_reset_chat(self, chat_service):
        """Test that the chat service can reset chat."""
        # Should not raise an exception
        await chat_service.reset_chat()


class TestProjectService:
    """Test the ProjectService."""

    @pytest.fixture
    def project_service(self):
        """Create a project service for testing."""
        repository = InMemoryProjectRepository()
        return ProjectService(repository)

    @pytest.mark.asyncio
    async def test_create_project(self, project_service):
        """Test creating a project."""
        project = await project_service.create_project("Test Project", "Test PRD")

        assert project.name == "Test Project"
        assert project.prd == "Test PRD"
        assert project.id is not None

    @pytest.mark.asyncio
    async def test_get_project(self, project_service):
        """Test getting a project."""
        # Create a project first
        created_project = await project_service.create_project("Test Project")

        # Get it back
        retrieved_project = await project_service.get_project(str(created_project.id))

        assert retrieved_project.id == created_project.id
        assert retrieved_project.name == "Test Project"

    @pytest.mark.asyncio
    async def test_get_project_not_found(self, project_service):
        """Test getting a non-existent project."""
        with pytest.raises(ProjectNotFoundError):
            await project_service.get_project(str(uuid4()))

    @pytest.mark.asyncio
    async def test_list_projects(self, project_service):
        """Test listing projects."""
        # Start with empty list
        projects = await project_service.list_projects()
        assert len(projects) == 0

        # Add some projects
        await project_service.create_project("Project 1")
        await project_service.create_project("Project 2")

        projects = await project_service.list_projects()
        assert len(projects) == 2
        project_names = {p.name for p in projects}
        assert project_names == {"Project 1", "Project 2"}

    @pytest.mark.asyncio
    async def test_update_project(self, project_service):
        """Test updating a project."""
        # Create a project
        project = await project_service.create_project("Original Name", "Original PRD")

        # Update it
        updated_project = await project_service.update_project(
            str(project.id), name="New Name", prd="New PRD"
        )

        assert updated_project.id == project.id
        assert updated_project.name == "New Name"
        assert updated_project.prd == "New PRD"
        assert updated_project.updated_at is not None

    @pytest.mark.asyncio
    async def test_update_project_partial(self, project_service):
        """Test updating only some fields of a project."""
        # Create a project
        project = await project_service.create_project("Original Name", "Original PRD")

        # Update only name
        updated_project = await project_service.update_project(
            str(project.id), name="New Name"
        )

        assert updated_project.name == "New Name"
        assert updated_project.prd == "Original PRD"  # Should remain unchanged

    @pytest.mark.asyncio
    async def test_update_project_not_found(self, project_service):
        """Test updating a non-existent project."""
        with pytest.raises(ProjectNotFoundError):
            await project_service.update_project(str(uuid4()), name="New Name")

    @pytest.mark.asyncio
    async def test_delete_project(self, project_service):
        """Test deleting a project."""
        # Create a project
        project = await project_service.create_project("Test Project")

        # Delete it
        deleted = await project_service.delete_project(str(project.id))
        assert deleted is True

        # Try to get it (should fail)
        with pytest.raises(ProjectNotFoundError):
            await project_service.get_project(str(project.id))

    @pytest.mark.asyncio
    async def test_delete_project_not_found(self, project_service):
        """Test deleting a non-existent project."""
        deleted = await project_service.delete_project(str(uuid4()))
        assert deleted is False

    @pytest.mark.asyncio
    async def test_create_project_empty_name(self, project_service):
        """Test creating a project with empty name."""
        with pytest.raises(ValueError, match="Project name cannot be empty"):
            await project_service.create_project("")

        with pytest.raises(ValueError, match="Project name cannot be empty"):
            await project_service.create_project("   ")  # Whitespace only

    @pytest.mark.asyncio
    async def test_create_project_long_name(self, project_service):
        """Test creating a project with too long name."""
        long_name = "x" * 256  # Exceeds 255 character limit
        with pytest.raises(ValueError, match="Project name too long"):
            await project_service.create_project(long_name)

    @pytest.mark.asyncio
    async def test_update_project_empty_name(self, project_service):
        """Test updating a project with empty name."""
        project = await project_service.create_project("Original Name")

        with pytest.raises(ValueError, match="Project name cannot be empty"):
            await project_service.update_project(str(project.id), name="")

        with pytest.raises(ValueError, match="Project name cannot be empty"):
            await project_service.update_project(str(project.id), name="   ")

    @pytest.mark.asyncio
    async def test_update_project_long_name(self, project_service):
        """Test updating a project with too long name."""
        project = await project_service.create_project("Original Name")
        long_name = "x" * 256  # Exceeds 255 character limit

        with pytest.raises(ValueError, match="Project name too long"):
            await project_service.update_project(str(project.id), name=long_name)

    @pytest.mark.asyncio
    async def test_invalid_project_id_format(self, project_service):
        """Test operations with invalid project ID format."""
        with pytest.raises(ProjectNotFoundError, match="Invalid project ID format"):
            await project_service.get_project("not-a-uuid")

        with pytest.raises(ProjectNotFoundError, match="Invalid project ID format"):
            await project_service.update_project("not-a-uuid", name="New Name")

        with pytest.raises(ProjectNotFoundError, match="Invalid project ID format"):
            await project_service.delete_project("not-a-uuid")
