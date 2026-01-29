# Explore Phase: Understanding Existing Code

## Learning Objectives

By the end of this module, you will:
- Understand when and why to use the Explore phase
- Know how to use the `/epcc-explore` command
- Practice exploring the Todo app as "unfamiliar" code
- Learn techniques for understanding code patterns

## When to Use Explore

The Explore phase is for **brownfield development** - when you're working with existing code.

### Greenfield vs Brownfield Reminder

| Type | Definition | Explore? |
|------|------------|----------|
| **Greenfield** | Starting from scratch | Skip |
| **Brownfield** | Existing codebase | Use Explore |

### Signs You Need Explore

Use Explore when:
- Joining an existing project
- Adding features to unfamiliar code
- Fixing bugs in code you didn't write
- Refactoring legacy systems

### What Explore Helps You Find

```
┌─────────────────────────────────────────────────┐
│           What Explore Reveals                  │
├─────────────────────────────────────────────────┤
│ • Project structure and organization            │
│ • Naming conventions and patterns               │
│ • Data flow and architecture                    │
│ • Testing approaches                            │
│ • Entry points and commands                     │
│ • Dependencies and their usage                  │
└─────────────────────────────────────────────────┘
```

## Using the /epcc-explore Command

The `/epcc-explore` command helps you understand a codebase systematically.

### Starting an Explore Session

```bash
# In Claude Code, in an existing project:
/epcc-explore

# Or with specific focus:
/epcc-explore how does the storage layer work
```

### Command Options

| Flag | Purpose |
|------|---------|
| `--deep` | Thorough analysis, slower |
| `--quick` | Overview only, faster |
| `--refresh` | Re-scan, ignore cached knowledge |

### What the Command Does

1. **Scans the project** - Files, structure, patterns
2. **Identifies architecture** - Layers, components, data flow
3. **Documents patterns** - Naming, testing, error handling
4. **Summarizes findings** - What you need to know

## Exercise: Explore the Todo App

Let's practice Explore using the Todo app as if you were seeing it for the first time.

### Setup

Navigate to the todo-app directory:

```bash
cd tutorial/todo-app
```

Pretend you've never seen this code before. You're a new developer tasked with adding a feature.

### Step 1: Project Overview

Start by understanding the high-level structure:

```
/epcc-explore --quick
```

**What to look for:**
- What is this project?
- What language/framework?
- How is it organized?

**Expected Findings:**

```
Project: todo (CLI application)
Language: Python 3.9+
Framework: Typer (CLI)
Structure: src/todo/ (application), tests/ (pytest)
Entry point: todo.cli:app
```

### Step 2: Architecture Discovery

Explore how components are organized:

```
/epcc-explore what is the architecture pattern
```

**Expected Findings:**

```
Architecture: Layered

┌─────────────────┐
│    cli.py       │  User interface (Typer commands)
├─────────────────┤
│   models.py     │  Data structures (TodoItem)
├─────────────────┤
│   storage.py    │  Persistence (JSON file)
└─────────────────┘

Data Flow: CLI → Models → Storage → File System
```

### Step 3: Pattern Identification

Look for conventions and patterns:

```
/epcc-explore what patterns are used
```

**Expected Findings:**

| Pattern | Example |
|---------|---------|
| Dataclass | `TodoItem` in models.py |
| Dependency injection | Optional `path` parameter in storage functions |
| Partial ID matching | `todo.id.startswith(todo_id)` |
| Rich formatting | `[green]Added:[/green]` for colored output |
| Type hints | All functions have type annotations |

### Step 4: Testing Approach

Understand how the codebase is tested:

```
/epcc-explore how are tests organized
```

**Expected Findings:**

```
Testing Framework: pytest
Fixtures: conftest.py (temp_storage, sample_todos)

Test Organization:
├── test_models.py    # Unit tests for TodoItem
├── test_storage.py   # Storage operations
└── test_cli.py       # Integration tests using CliRunner

Pattern: Mocking storage path for isolation
Coverage: 96%
```

### Step 5: Entry Points

Find how to run and use the application:

```
/epcc-explore what are the entry points and commands
```

**Expected Findings:**

```
Entry Points:
- python -m todo (via __main__.py)
- todo (via pyproject.toml script)

Commands:
- todo add <title>       # Add new item
- todo list [--all]      # List items
- todo complete <id>     # Mark done
- todo delete <id>       # Remove item
- todo clear             # Remove completed
```

## Exploration Techniques

### Reading Order

When exploring unfamiliar code, read in this order:

1. **README/docs** - Official explanation
2. **pyproject.toml/setup.py** - Dependencies and entry points
3. **Tests** - Show expected behavior
4. **Entry points** - How things start
5. **Core logic** - Deep dive into implementation

### Questions to Ask

Ask yourself these questions as you explore:

```
Structure:
- How are files organized?
- What is each file responsible for?
- How do components connect?

Patterns:
- What naming conventions are used?
- How is data passed between layers?
- How are errors handled?

Testing:
- What testing framework is used?
- How are tests organized?
- What fixtures exist?

Dependencies:
- What external packages are used?
- Why were they chosen?
- How are they used?
```

### Creating Mental Models

Build a mental model of the codebase:

```
┌────────────────────────────────────────────────────────────┐
│                    Todo App Mental Model                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   User types command                                       │
│          ↓                                                 │
│   Typer parses arguments (cli.py)                         │
│          ↓                                                 │
│   CLI function calls storage layer                         │
│          ↓                                                 │
│   Storage loads/saves via JSON (storage.py)               │
│          ↓                                                 │
│   TodoItem handles data structure (models.py)             │
│          ↓                                                 │
│   Rich formats output                                      │
│          ↓                                                 │
│   User sees result                                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Practice Exercise: Add a Feature

Now that you've explored the codebase, try adding a feature:

**Task**: Add a `count` command that shows todo statistics.

### Step 1: Explore First

What do you need to know?
- How are commands defined? (Check cli.py)
- How to get todos? (Check storage.py)
- What output format to use? (Check existing commands)

### Step 2: Plan Based on Exploration

Based on your exploration:
```python
# Pattern: Command decorator with typer.Option
# Data access: storage.load_todos()
# Output: Rich formatting [green]...[/green]
```

### Step 3: Implement

```python
@app.command()
def count() -> None:
    """Show todo statistics."""
    todos = storage.load_todos()
    completed = len([t for t in todos if t.completed])
    pending = len([t for t in todos if not t.completed])

    print(f"[bold]Todo Statistics[/bold]")
    print(f"Pending:   [yellow]{pending}[/yellow]")
    print(f"Completed: [green]{completed}[/green]")
    print(f"Total:     {len(todos)}")
```

See how exploration made implementation straightforward? You knew:
- Where to add the command
- How to access data
- What output pattern to follow

## Key Takeaways

- **Use Explore for brownfield** - When working with existing code
- **Use `/epcc-explore`** to systematically understand a codebase
- **Read in order** - README → config → tests → entry points → core
- **Build mental models** - Understand data flow and architecture
- **Match existing patterns** - New code should feel native

## Full EPCC Workflow

You now know all phases of EPCC:

| Phase | When | Command |
|-------|------|---------|
| **Explore** | Brownfield (existing code) | `/epcc-explore` |
| **Plan** | Always | `/epcc-plan` |
| **Code** | Always | `/epcc-code` |
| **Commit** | Always | `/epcc-commit` |

```
Brownfield: Explore → Plan → Code → Commit
Greenfield: Plan → Code → Commit (skip Explore)
```

## What's Next?

Ready for a quick reference of all commands?

→ **[Quick Reference](./07-quick-reference.md)**

---

*Estimated time for this module: 20-30 minutes*
