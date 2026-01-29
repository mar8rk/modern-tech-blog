"""Shared test fixtures for todo application."""

from pathlib import Path

import pytest

from todo.models import TodoItem


@pytest.fixture
def temp_storage(tmp_path: Path) -> Path:
    """Provide a temporary storage file path for tests.

    This fixture creates a fresh temporary file for each test,
    ensuring test isolation.
    """
    return tmp_path / "test_todos.json"


@pytest.fixture
def sample_todo() -> TodoItem:
    """Provide a single sample todo item."""
    return TodoItem(id="test1234", title="Test todo item")


@pytest.fixture
def sample_todos() -> list[TodoItem]:
    """Provide a list of sample todo items for testing."""
    todo1 = TodoItem(id="abc12345", title="First task")
    todo2 = TodoItem(id="def67890", title="Second task")
    todo2.complete()  # Mark second one as completed
    todo3 = TodoItem(id="ghi11111", title="Third task")
    return [todo1, todo2, todo3]
