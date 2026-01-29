"""Tests for todo.cli module."""

from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from todo import storage
from todo.cli import app

runner = CliRunner()


@pytest.fixture
def mock_storage(temp_storage: Path):
    """Mock storage to use temporary file."""
    with patch.object(storage, "get_storage_path", return_value=temp_storage):
        yield temp_storage


class TestAddCommand:
    """Tests for the add command."""

    def test_add_todo(self, mock_storage: Path) -> None:
        """Test adding a todo via CLI."""
        result = runner.invoke(app, ["add", "Buy milk"])

        assert result.exit_code == 0
        assert "Added:" in result.output
        assert "Buy milk" in result.output

        # Verify it was saved
        todos = storage.load_todos(mock_storage)
        assert len(todos) == 1
        assert todos[0].title == "Buy milk"

    def test_add_todo_with_spaces(self, mock_storage: Path) -> None:
        """Test adding a todo with spaces in title."""
        result = runner.invoke(app, ["add", "Go to the grocery store"])

        assert result.exit_code == 0
        todos = storage.load_todos(mock_storage)
        assert todos[0].title == "Go to the grocery store"


class TestListCommand:
    """Tests for the list command."""

    def test_list_empty(self, mock_storage: Path) -> None:
        """Test listing when no todos exist."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "No todos found" in result.output

    def test_list_todos(self, mock_storage: Path) -> None:
        """Test listing todos."""
        storage.add_todo("First task", mock_storage)
        storage.add_todo("Second task", mock_storage)

        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "First task" in result.output
        assert "Second task" in result.output
        assert "2 item(s)" in result.output

    def test_list_hides_completed(self, mock_storage: Path) -> None:
        """Test that list hides completed todos by default."""
        storage.add_todo("Incomplete", mock_storage)
        todo2 = storage.add_todo("Complete", mock_storage)
        storage.complete_todo(todo2.id, mock_storage)

        result = runner.invoke(app, ["list"])

        assert "Incomplete" in result.output
        assert "Complete" not in result.output
        assert "1 item(s)" in result.output

    def test_list_all(self, mock_storage: Path) -> None:
        """Test listing all todos including completed."""
        storage.add_todo("Incomplete", mock_storage)
        todo2 = storage.add_todo("Complete", mock_storage)
        storage.complete_todo(todo2.id, mock_storage)

        result = runner.invoke(app, ["list", "--all"])

        assert "Incomplete" in result.output
        assert "Complete" in result.output
        assert "2 item(s)" in result.output


class TestCompleteCommand:
    """Tests for the complete command."""

    def test_complete_todo(self, mock_storage: Path) -> None:
        """Test completing a todo via CLI."""
        todo = storage.add_todo("Task to complete", mock_storage)

        result = runner.invoke(app, ["complete", todo.id])

        assert result.exit_code == 0
        assert "Completed:" in result.output

        # Verify it was completed
        updated = storage.get_todo_by_id(todo.id, mock_storage)
        assert updated is not None
        assert updated.completed is True

    def test_complete_by_partial_id(self, mock_storage: Path) -> None:
        """Test completing by partial ID."""
        todo = storage.add_todo("Task", mock_storage)
        partial_id = todo.id[:4]

        result = runner.invoke(app, ["complete", partial_id])

        assert result.exit_code == 0

    def test_complete_nonexistent(self, mock_storage: Path) -> None:
        """Test completing nonexistent todo shows error."""
        result = runner.invoke(app, ["complete", "notreal"])

        assert result.exit_code == 1
        assert "not found" in result.output


class TestDeleteCommand:
    """Tests for the delete command."""

    def test_delete_todo(self, mock_storage: Path) -> None:
        """Test deleting a todo via CLI."""
        todo = storage.add_todo("Task to delete", mock_storage)

        result = runner.invoke(app, ["delete", todo.id])

        assert result.exit_code == 0
        assert "Deleted:" in result.output
        assert "Task to delete" in result.output

        # Verify it was deleted
        todos = storage.load_todos(mock_storage)
        assert len(todos) == 0

    def test_delete_nonexistent(self, mock_storage: Path) -> None:
        """Test deleting nonexistent todo shows error."""
        result = runner.invoke(app, ["delete", "notreal"])

        assert result.exit_code == 1
        assert "not found" in result.output


class TestClearCommand:
    """Tests for the clear command."""

    def test_clear_completed(self, mock_storage: Path) -> None:
        """Test clearing completed todos via CLI."""
        storage.add_todo("Keep this", mock_storage)
        todo2 = storage.add_todo("Clear this", mock_storage)
        storage.complete_todo(todo2.id, mock_storage)

        result = runner.invoke(app, ["clear"])

        assert result.exit_code == 0
        assert "Cleared:" in result.output
        assert "1 completed item(s)" in result.output

        # Verify only incomplete remains
        todos = storage.load_todos(mock_storage)
        assert len(todos) == 1
        assert todos[0].title == "Keep this"

    def test_clear_nothing(self, mock_storage: Path) -> None:
        """Test clearing when nothing to clear."""
        storage.add_todo("Not completed", mock_storage)

        result = runner.invoke(app, ["clear"])

        assert result.exit_code == 0
        assert "No completed items" in result.output
