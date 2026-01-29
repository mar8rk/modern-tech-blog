"""Tests for todo.models module."""

from datetime import datetime

from todo.models import TodoItem


class TestTodoItem:
    """Tests for the TodoItem dataclass."""

    def test_create_todo_with_title(self) -> None:
        """Test creating a todo with just a title."""
        todo = TodoItem(title="Buy groceries")

        assert todo.title == "Buy groceries"
        assert todo.completed is False
        assert todo.completed_at is None
        assert len(todo.id) == 8  # UUID prefix

    def test_create_todo_with_custom_id(self) -> None:
        """Test creating a todo with a custom ID."""
        todo = TodoItem(id="custom12", title="Custom ID todo")

        assert todo.id == "custom12"
        assert todo.title == "Custom ID todo"

    def test_todo_has_created_at(self) -> None:
        """Test that todos have a creation timestamp."""
        before = datetime.now()
        todo = TodoItem(title="Test")
        after = datetime.now()

        assert before <= todo.created_at <= after

    def test_complete_todo(self) -> None:
        """Test marking a todo as completed."""
        todo = TodoItem(title="Task to complete")

        assert todo.completed is False
        assert todo.completed_at is None

        todo.complete()

        assert todo.completed is True
        assert todo.completed_at is not None

    def test_to_dict(self) -> None:
        """Test converting todo to dictionary."""
        todo = TodoItem(id="test1234", title="Test task")
        data = todo.to_dict()

        assert data["id"] == "test1234"
        assert data["title"] == "Test task"
        assert data["completed"] is False
        assert data["completed_at"] is None
        assert "created_at" in data

    def test_to_dict_completed(self) -> None:
        """Test converting completed todo to dictionary."""
        todo = TodoItem(id="test1234", title="Test task")
        todo.complete()
        data = todo.to_dict()

        assert data["completed"] is True
        assert data["completed_at"] is not None

    def test_from_dict(self) -> None:
        """Test creating todo from dictionary."""
        data = {
            "id": "abc12345",
            "title": "From dict",
            "completed": False,
            "created_at": "2025-01-15T10:30:00",
            "completed_at": None,
        }

        todo = TodoItem.from_dict(data)

        assert todo.id == "abc12345"
        assert todo.title == "From dict"
        assert todo.completed is False
        assert todo.completed_at is None

    def test_from_dict_completed(self) -> None:
        """Test creating completed todo from dictionary."""
        data = {
            "id": "abc12345",
            "title": "Completed task",
            "completed": True,
            "created_at": "2025-01-15T10:30:00",
            "completed_at": "2025-01-15T11:00:00",
        }

        todo = TodoItem.from_dict(data)

        assert todo.completed is True
        assert todo.completed_at is not None

    def test_roundtrip_serialization(self) -> None:
        """Test that to_dict and from_dict are inverses."""
        original = TodoItem(title="Roundtrip test")
        original.complete()

        data = original.to_dict()
        restored = TodoItem.from_dict(data)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.completed == original.completed
        # Note: datetime precision may differ slightly
        assert restored.created_at.isoformat() == original.created_at.isoformat()

    def test_unique_ids(self) -> None:
        """Test that auto-generated IDs are unique."""
        todos = [TodoItem(title=f"Todo {i}") for i in range(100)]
        ids = [todo.id for todo in todos]

        assert len(ids) == len(set(ids)), "Generated IDs should be unique"
