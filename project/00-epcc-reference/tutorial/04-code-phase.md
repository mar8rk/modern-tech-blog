# Code Phase: Implementing with Confidence

## Learning Objectives

By the end of this module, you will:
- Know how to use the `/epcc-code` command
- Understand the TDD (Test-Driven Development) workflow
- Walk through implementing the Todo app layer by layer
- See real code examples from our implementation

## What is the Code Phase?

The Code phase is where you actually write code! But not just any code:

- **Guided by your plan** - follow the tasks you defined
- **Quality-focused** - write tests alongside implementation
- **Iterative** - small chunks, frequent verification

```
Plan Tasks → Code Each Task → Test → Verify → Next Task
```

## Using the /epcc-code Command

The `/epcc-code` command helps you implement tasks from your plan.

### Starting a Code Session

```bash
# In Claude Code, after you have a plan:
/epcc-code

# Or with specific task:
/epcc-code implement the storage layer
```

### What the Command Does

1. **Reads your plan** - knows what tasks need to be done
2. **Tracks progress** - updates feature tracking as you work
3. **Maintains quality** - encourages tests and verification
4. **Follows patterns** - respects your TRD architecture decisions

### Code Session Options

| Flag | Purpose |
|------|---------|
| `--tdd` | Strict TDD: write tests first |
| `--quick` | Faster iteration, tests after |
| `--full` | Comprehensive with documentation |

## TDD: Test-Driven Development

TDD is a development practice where you:

1. **Write a failing test** (Red)
2. **Write code to make it pass** (Green)
3. **Refactor** while keeping tests passing

```
┌─────────────────────────────────────────┐
│            TDD Cycle                    │
│                                         │
│    ┌───────┐                            │
│    │  RED  │ Write failing test         │
│    └───┬───┘                            │
│        ↓                                │
│    ┌───────┐                            │
│    │ GREEN │ Make it pass               │
│    └───┬───┘                            │
│        ↓                                │
│    ┌─────────┐                          │
│    │REFACTOR │ Improve code             │
│    └────┬────┘                          │
│         └────→ Repeat                   │
└─────────────────────────────────────────┘
```

### Why TDD?

- **Forces you to think about design** before coding
- **Ensures testable code** by nature
- **Documents behavior** through tests
- **Catches regressions** immediately

## Implementing the Todo App

Let's walk through implementing our Todo app layer by layer.

### Layer 1: Data Model (models.py)

First, we define our core data structure.

**The TodoItem Dataclass**

```python
# File: src/todo/models.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
import uuid

@dataclass
class TodoItem:
    """A single todo item."""

    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def complete(self) -> None:
        """Mark this todo item as completed."""
        self.completed = True
        self.completed_at = datetime.now()
```

**Key Design Decisions:**

| Choice | Rationale |
|--------|-----------|
| `@dataclass` | Less boilerplate, auto-generates methods |
| Short UUID (`[:8]`) | User-friendly IDs like "a1b2c3d4" |
| `field(default_factory=...)` | Fresh values per instance |
| Timestamps | Track when things happen |

**Serialization Methods**

For JSON storage, we need to convert to/from dictionaries:

```python
def to_dict(self) -> dict[str, Any]:
    """Convert to dictionary for JSON serialization."""
    return {
        "id": self.id,
        "title": self.title,
        "completed": self.completed,
        "created_at": self.created_at.isoformat(),
        "completed_at": (
            self.completed_at.isoformat() if self.completed_at else None
        ),
    }

@classmethod
def from_dict(cls, data: dict[str, Any]) -> "TodoItem":
    """Create a TodoItem from a dictionary."""
    return cls(
        id=data["id"],
        title=data["title"],
        completed=data["completed"],
        created_at=datetime.fromisoformat(data["created_at"]),
        completed_at=(
            datetime.fromisoformat(data["completed_at"])
            if data["completed_at"]
            else None
        ),
    )
```

**Testing the Model**

```python
# File: tests/test_models.py

def test_create_todo_with_title():
    """Test creating a todo with just a title."""
    todo = TodoItem(title="Buy groceries")

    assert todo.title == "Buy groceries"
    assert todo.completed is False
    assert len(todo.id) == 8  # Short UUID

def test_complete_todo():
    """Test marking a todo as completed."""
    todo = TodoItem(title="Task to complete")

    todo.complete()

    assert todo.completed is True
    assert todo.completed_at is not None
```

### Layer 2: Storage (storage.py)

The storage layer handles persistence to JSON.

**Core Functions**

```python
# File: src/todo/storage.py

from pathlib import Path
import json
from typing import Optional
from .models import TodoItem

def get_storage_path() -> Path:
    """Get the default storage file path."""
    return Path.home() / ".todo.json"

def load_todos(path: Optional[Path] = None) -> list[TodoItem]:
    """Load todos from the storage file."""
    storage_path = path or get_storage_path()

    if not storage_path.exists():
        return []

    try:
        with open(storage_path, "r") as f:
            data = json.load(f)
            return [TodoItem.from_dict(item) for item in data.get("todos", [])]
    except json.JSONDecodeError:
        return []  # Corrupted file - return empty

def save_todos(todos: list[TodoItem], path: Optional[Path] = None) -> None:
    """Save todos to the storage file."""
    storage_path = path or get_storage_path()

    data = {
        "version": "1.0",
        "todos": [todo.to_dict() for todo in todos],
    }

    with open(storage_path, "w") as f:
        json.dump(data, f, indent=2)
```

**Convenience Functions**

```python
def add_todo(title: str, path: Optional[Path] = None) -> TodoItem:
    """Create and save a new todo item."""
    todos = load_todos(path)
    new_todo = TodoItem(title=title)
    todos.append(new_todo)
    save_todos(todos, path)
    return new_todo

def complete_todo(todo_id: str, path: Optional[Path] = None) -> Optional[TodoItem]:
    """Mark a todo item as completed."""
    todos = load_todos(path)

    for todo in todos:
        if todo.id == todo_id or todo.id.startswith(todo_id):
            todo.complete()
            save_todos(todos, path)
            return todo

    return None
```

**Testing with Fixtures**

```python
# File: tests/conftest.py

import pytest
from pathlib import Path

@pytest.fixture
def temp_storage(tmp_path: Path) -> Path:
    """Provide temporary storage file for tests."""
    return tmp_path / "test_todos.json"
```

```python
# File: tests/test_storage.py

def test_add_and_load(temp_storage):
    """Test adding and loading todos."""
    storage.add_todo("First task", temp_storage)
    storage.add_todo("Second task", temp_storage)

    todos = storage.load_todos(temp_storage)

    assert len(todos) == 2
    assert todos[0].title == "First task"
```

### Layer 3: CLI (cli.py)

The CLI layer provides user interaction via Typer.

**Basic Setup**

```python
# File: src/todo/cli.py

import typer
from rich import print
from rich.table import Table
from . import storage

app = typer.Typer(help="Simple todo list manager")
```

**Commands**

```python
@app.command()
def add(title: str = typer.Argument(..., help="Todo description")) -> None:
    """Add a new todo item."""
    todo = storage.add_todo(title)
    print(f"[green]Added:[/green] {todo.title} [dim]({todo.id})[/dim]")

@app.command("list")
def list_todos(
    all: bool = typer.Option(False, "--all", "-a", help="Include completed items")
) -> None:
    """List todo items."""
    todos = storage.load_todos()

    if not all:
        todos = [t for t in todos if not t.completed]

    if not todos:
        print("[dim]No todos found.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Status", width=3)
    table.add_column("ID", style="dim")
    table.add_column("Title")

    for todo in todos:
        status = "[green]✓[/green]" if todo.completed else "[ ]"
        table.add_row(status, todo.id, todo.title)

    print(table)
    print(f"\n[dim]{len(todos)} item(s)[/dim]")
```

**CLI Testing with CliRunner**

```python
# File: tests/test_cli.py

from typer.testing import CliRunner
from todo.cli import app

runner = CliRunner()

def test_add_todo(mock_storage):
    """Test adding a todo via CLI."""
    result = runner.invoke(app, ["add", "Buy milk"])

    assert result.exit_code == 0
    assert "Added:" in result.output
    assert "Buy milk" in result.output
```

## Hands-On: Implement Your Todo App

Follow these steps to build your own Todo app:

### Step 1: Create Project Structure

```bash
mkdir -p todo-app/src/todo todo-app/tests
cd todo-app
```

### Step 2: Initialize with pyproject.toml

```toml
[project]
name = "todo"
version = "1.0.0"
description = "Simple CLI todo app"
requires-python = ">=3.9"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "black>=24.0.0",
    "mypy>=1.0.0",
]

[project.scripts]
todo = "todo.cli:app"
```

### Step 3: Install Dependencies

```bash
# With uv (recommended)
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Or with pip
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Step 4: Implement Each Layer

Use `/epcc-code` to guide implementation:

```
/epcc-code implement models.py
```

After each layer, run tests:

```bash
pytest -v
```

### Step 5: Verify Quality

```bash
# Format
black src tests

# Lint
ruff check --fix src tests

# Type check
mypy src

# Full test with coverage
pytest --cov=src --cov-report=term-missing
```

## Reference Implementation

The complete working implementation is in `todo-app/`:

```
todo-app/
├── src/todo/
│   ├── __init__.py          # Package init
│   ├── models.py             # TodoItem dataclass
│   ├── storage.py            # JSON persistence
│   ├── cli.py                # Typer commands
│   └── __main__.py           # Entry point
└── tests/
    ├── conftest.py           # Test fixtures
    ├── test_models.py        # Model tests
    ├── test_storage.py       # Storage tests
    └── test_cli.py           # CLI tests
```

See the [todo-app README](./todo-app/README.md) for usage instructions.

## Key Takeaways

- **Use `/epcc-code`** to implement tasks from your plan
- **Consider TDD** - write tests first when possible
- **Build layer by layer** - models → storage → CLI
- **Test each layer** before moving to the next
- **Run quality checks** frequently (format, lint, type check)

## What's Next?

We've written the code! Now it's time to verify everything works and commit our changes.

→ **[Next: Commit Phase](./05-commit-phase.md)**

---

*Estimated time for this module: 30-45 minutes*
