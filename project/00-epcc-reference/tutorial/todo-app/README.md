# Todo CLI Application

A simple command-line todo list manager built with Python and Typer.

This application is part of the [EPCC Workflow Tutorial](../README.md) and demonstrates:
- Layered architecture (CLI → Models → Storage)
- Type hints and dataclasses
- pytest testing with fixtures
- Typer CLI with Rich output

## Installation

```bash
# Using uv (recommended)
cd todo-app
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Using pip
cd todo-app
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
# Add a todo
todo add "Buy groceries"
todo add "Learn EPCC workflow"

# List todos (hides completed by default)
todo list

# List all todos including completed
todo list --all

# Complete a todo (use full or partial ID)
todo complete abc12345
todo complete abc  # partial match works

# Delete a todo
todo delete abc12345

# Clear all completed todos
todo clear
```

## Example Output

```
$ todo list
┏━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Status ┃ ID       ┃ Title               ┃
┡━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ [ ]    │ a1b2c3d4 │ Buy groceries       │
│ [ ]    │ e5f6g7h8 │ Learn EPCC workflow │
└────────┴──────────┴─────────────────────┘

2 item(s)
```

## Data Storage

Todos are stored in `~/.todo.json` as a simple JSON file:

```json
{
  "version": "1.0",
  "todos": [
    {
      "id": "a1b2c3d4",
      "title": "Buy groceries",
      "completed": false,
      "created_at": "2025-01-15T10:30:00",
      "completed_at": null
    }
  ]
}
```

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Format code
black src tests

# Lint code
ruff check src tests

# Type check
mypy src
```

## Project Structure

```
todo-app/
├── pyproject.toml          # Project config and dependencies
├── README.md               # This file
├── src/
│   └── todo/
│       ├── __init__.py     # Package init, version
│       ├── __main__.py     # Entry point for `python -m todo`
│       ├── cli.py          # Typer CLI commands
│       ├── models.py       # TodoItem dataclass
│       └── storage.py      # JSON file persistence
└── tests/
    ├── __init__.py
    ├── conftest.py         # Shared fixtures
    ├── test_cli.py         # CLI integration tests
    ├── test_models.py      # Model unit tests
    └── test_storage.py     # Storage unit tests
```

## Architecture

```
User Input → CLI (Typer) → Models (dataclass) → Storage (JSON) → File System
                ↓
            Output (Rich)
```

- **CLI Layer** (`cli.py`): Handles user interaction, argument parsing, output formatting
- **Models Layer** (`models.py`): Data structures, validation, serialization
- **Storage Layer** (`storage.py`): File I/O, JSON persistence, path management
