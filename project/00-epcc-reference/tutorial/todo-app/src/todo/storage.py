"""JSON file persistence for todo items."""

import json
from pathlib import Path
from typing import Optional

from .models import TodoItem

# Storage format version for future migrations
STORAGE_VERSION = "1.0"


def get_storage_path() -> Path:
    """Get the default storage file path.

    Returns:
        Path to ~/.todo.json
    """
    return Path.home() / ".todo.json"


def load_todos(path: Optional[Path] = None) -> list[TodoItem]:
    """Load todos from the storage file.

    Args:
        path: Optional custom path (defaults to ~/.todo.json)

    Returns:
        List of TodoItem objects. Empty list if file doesn't exist.
    """
    storage_path = path or get_storage_path()

    if not storage_path.exists():
        return []

    try:
        with open(storage_path, "r") as f:
            data = json.load(f)
            return [TodoItem.from_dict(item) for item in data.get("todos", [])]
    except json.JSONDecodeError:
        # Corrupted file - return empty list
        return []


def save_todos(todos: list[TodoItem], path: Optional[Path] = None) -> None:
    """Save todos to the storage file.

    Args:
        todos: List of TodoItem objects to save.
        path: Optional custom path (defaults to ~/.todo.json)
    """
    storage_path = path or get_storage_path()

    data = {
        "version": STORAGE_VERSION,
        "todos": [todo.to_dict() for todo in todos],
    }

    with open(storage_path, "w") as f:
        json.dump(data, f, indent=2)


def get_todo_by_id(todo_id: str, path: Optional[Path] = None) -> Optional[TodoItem]:
    """Find a todo item by its ID.

    Args:
        todo_id: The ID to search for (can be partial match).
        path: Optional custom path (defaults to ~/.todo.json)

    Returns:
        The matching TodoItem, or None if not found.
    """
    todos = load_todos(path)

    # Try exact match first
    for todo in todos:
        if todo.id == todo_id:
            return todo

    # Try prefix match (allows short IDs like "a1b" to match "a1b2c3d4")
    matches = [todo for todo in todos if todo.id.startswith(todo_id)]
    if len(matches) == 1:
        return matches[0]

    return None


def add_todo(title: str, path: Optional[Path] = None) -> TodoItem:
    """Create and save a new todo item.

    Args:
        title: The todo description.
        path: Optional custom path (defaults to ~/.todo.json)

    Returns:
        The newly created TodoItem.
    """
    todos = load_todos(path)
    new_todo = TodoItem(title=title)
    todos.append(new_todo)
    save_todos(todos, path)
    return new_todo


def complete_todo(todo_id: str, path: Optional[Path] = None) -> Optional[TodoItem]:
    """Mark a todo item as completed.

    Args:
        todo_id: The ID of the todo to complete.
        path: Optional custom path (defaults to ~/.todo.json)

    Returns:
        The updated TodoItem, or None if not found.
    """
    todos = load_todos(path)

    for todo in todos:
        if todo.id == todo_id or todo.id.startswith(todo_id):
            todo.complete()
            save_todos(todos, path)
            return todo

    return None


def delete_todo(todo_id: str, path: Optional[Path] = None) -> bool:
    """Delete a todo item.

    Args:
        todo_id: The ID of the todo to delete.
        path: Optional custom path (defaults to ~/.todo.json)

    Returns:
        True if deleted, False if not found.
    """
    todos = load_todos(path)
    original_count = len(todos)

    todos = [
        todo
        for todo in todos
        if not (todo.id == todo_id or todo.id.startswith(todo_id))
    ]

    if len(todos) < original_count:
        save_todos(todos, path)
        return True

    return False


def clear_completed(path: Optional[Path] = None) -> int:
    """Remove all completed todos.

    Args:
        path: Optional custom path (defaults to ~/.todo.json)

    Returns:
        Number of items removed.
    """
    todos = load_todos(path)
    original_count = len(todos)

    todos = [todo for todo in todos if not todo.completed]
    removed_count = original_count - len(todos)

    if removed_count > 0:
        save_todos(todos, path)

    return removed_count
