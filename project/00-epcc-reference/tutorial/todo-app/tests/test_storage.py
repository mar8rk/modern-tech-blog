"""Tests for todo.storage module."""

import json
from pathlib import Path

from todo import storage
from todo.models import TodoItem


class TestLoadSaveTodos:
    """Tests for load_todos and save_todos functions."""

    def test_load_empty_file(self, temp_storage: Path) -> None:
        """Test loading from non-existent file returns empty list."""
        todos = storage.load_todos(temp_storage)
        assert todos == []

    def test_save_and_load(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test saving and loading todos."""
        storage.save_todos(sample_todos, temp_storage)
        loaded = storage.load_todos(temp_storage)

        assert len(loaded) == len(sample_todos)
        assert loaded[0].title == sample_todos[0].title
        assert loaded[1].completed == sample_todos[1].completed

    def test_load_corrupted_file(self, temp_storage: Path) -> None:
        """Test loading from corrupted JSON file returns empty list."""
        temp_storage.write_text("not valid json {{{")

        todos = storage.load_todos(temp_storage)
        assert todos == []

    def test_storage_version(self, temp_storage: Path) -> None:
        """Test that saved files include version number."""
        storage.save_todos([], temp_storage)

        with open(temp_storage) as f:
            data = json.load(f)

        assert "version" in data
        assert data["version"] == storage.STORAGE_VERSION


class TestGetTodoById:
    """Tests for get_todo_by_id function."""

    def test_get_by_exact_id(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test finding todo by exact ID match."""
        storage.save_todos(sample_todos, temp_storage)

        found = storage.get_todo_by_id("abc12345", temp_storage)
        assert found is not None
        assert found.title == "First task"

    def test_get_by_partial_id(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test finding todo by ID prefix."""
        storage.save_todos(sample_todos, temp_storage)

        # "abc" should match "abc12345"
        found = storage.get_todo_by_id("abc", temp_storage)
        assert found is not None
        assert found.id == "abc12345"

    def test_get_nonexistent_id(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test that nonexistent ID returns None."""
        storage.save_todos(sample_todos, temp_storage)

        found = storage.get_todo_by_id("xyz99999", temp_storage)
        assert found is None

    def test_get_empty_storage(self, temp_storage: Path) -> None:
        """Test getting from empty storage returns None."""
        found = storage.get_todo_by_id("any", temp_storage)
        assert found is None


class TestAddTodo:
    """Tests for add_todo function."""

    def test_add_todo(self, temp_storage: Path) -> None:
        """Test adding a new todo."""
        todo = storage.add_todo("New task", temp_storage)

        assert todo.title == "New task"
        assert todo.completed is False

        # Verify it was saved
        loaded = storage.load_todos(temp_storage)
        assert len(loaded) == 1
        assert loaded[0].title == "New task"

    def test_add_multiple_todos(self, temp_storage: Path) -> None:
        """Test adding multiple todos."""
        storage.add_todo("First", temp_storage)
        storage.add_todo("Second", temp_storage)
        storage.add_todo("Third", temp_storage)

        loaded = storage.load_todos(temp_storage)
        assert len(loaded) == 3


class TestCompleteTodo:
    """Tests for complete_todo function."""

    def test_complete_todo(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test completing a todo."""
        storage.save_todos(sample_todos, temp_storage)

        result = storage.complete_todo("abc12345", temp_storage)

        assert result is not None
        assert result.completed is True

        # Verify it was saved
        loaded = storage.load_todos(temp_storage)
        completed = [t for t in loaded if t.id == "abc12345"][0]
        assert completed.completed is True

    def test_complete_nonexistent(self, temp_storage: Path) -> None:
        """Test completing nonexistent todo returns None."""
        result = storage.complete_todo("notreal", temp_storage)
        assert result is None

    def test_complete_by_partial_id(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test completing by partial ID."""
        storage.save_todos(sample_todos, temp_storage)

        result = storage.complete_todo("ghi", temp_storage)  # Matches ghi11111
        assert result is not None
        assert result.id == "ghi11111"


class TestDeleteTodo:
    """Tests for delete_todo function."""

    def test_delete_todo(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test deleting a todo."""
        storage.save_todos(sample_todos, temp_storage)

        result = storage.delete_todo("abc12345", temp_storage)

        assert result is True
        loaded = storage.load_todos(temp_storage)
        assert len(loaded) == 2
        assert all(t.id != "abc12345" for t in loaded)

    def test_delete_nonexistent(self, temp_storage: Path) -> None:
        """Test deleting nonexistent todo returns False."""
        result = storage.delete_todo("notreal", temp_storage)
        assert result is False

    def test_delete_by_partial_id(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test deleting by partial ID."""
        storage.save_todos(sample_todos, temp_storage)

        result = storage.delete_todo("def", temp_storage)  # Matches def67890
        assert result is True

        loaded = storage.load_todos(temp_storage)
        assert all(t.id != "def67890" for t in loaded)


class TestClearCompleted:
    """Tests for clear_completed function."""

    def test_clear_completed(
        self, temp_storage: Path, sample_todos: list[TodoItem]
    ) -> None:
        """Test clearing completed todos."""
        storage.save_todos(sample_todos, temp_storage)

        removed = storage.clear_completed(temp_storage)

        assert removed == 1  # Only one was completed in sample_todos
        loaded = storage.load_todos(temp_storage)
        assert len(loaded) == 2
        assert all(not t.completed for t in loaded)

    def test_clear_completed_empty(self, temp_storage: Path) -> None:
        """Test clearing when no completed todos."""
        todos = [TodoItem(title="Not done")]
        storage.save_todos(todos, temp_storage)

        removed = storage.clear_completed(temp_storage)

        assert removed == 0
        loaded = storage.load_todos(temp_storage)
        assert len(loaded) == 1
