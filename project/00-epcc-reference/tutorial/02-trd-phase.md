# TRD Phase: Defining How to Build

## Learning Objectives

By the end of this module, you will:
- Understand what a TRD is and why it matters
- Know how to use the `/trd` command
- See an example TRD with technical decisions for our Todo app

## What is a TRD?

A **Technical Requirements Document (TRD)** answers the question: **"How will we build this?"**

While the PRD defined *what* we're building, the TRD specifies:
- **Technology choices** (languages, frameworks, libraries)
- **Architecture decisions** (how components fit together)
- **Data models** (how data is structured)
- **Development practices** (testing, linting, formatting)

### PRD vs TRD

| Aspect | PRD | TRD |
|--------|-----|-----|
| Focus | What to build | How to build it |
| Audience | Everyone | Developers |
| Content | Features, users, goals | Tech stack, architecture |
| Example | "Users can add tasks" | "Typer CLI with JSON storage" |

### Why TRDs Matter

A TRD:
- **Documents decisions** before you forget why you made them
- **Aligns the team** on technical approach
- **Catches issues early** before coding starts
- **Serves as reference** during implementation

## Using the /trd Command

The `/trd` command helps you create a TRD by asking about technical decisions. It typically reads your PRD first for context.

### Starting a TRD Session

```bash
# In Claude Code, after you have a PRD:
/trd

# Or with context:
/trd Todo CLI Application
```

### The Interactive Process

Claude asks about:

1. **Architecture** - Layered? Monolithic? Service-based?
2. **Technology stack** - Which frameworks, libraries?
3. **Data storage** - Database? Files? Format?
4. **Testing strategy** - What framework? Coverage targets?
5. **Code quality** - Linting, formatting tools?

### Example Interaction

```
You: /trd

Claude: I'll create a TRD based on your PRD. Let me ask about technical details.

┌─────────────────────────────────────────────────┐
│ What's the focus for technical decisions?       │
├─────────────────────────────────────────────────┤
│ ○ Application only                              │
│ ● Both app and documentation                    │
│ ○ Documentation/tutorial only                   │
└─────────────────────────────────────────────────┘

You: Both app and documentation

Claude: For CLI frameworks, I recommend...

┌─────────────────────────────────────────────────┐
│ Which CLI framework?                            │
├─────────────────────────────────────────────────┤
│ ○ argparse (standard library)                   │
│ ● Typer (modern, type-hints)                    │
│ ○ Click (mature, flexible)                      │
│ ○ Fire (auto-generates CLI)                     │
└─────────────────────────────────────────────────┘

You: Typer

Claude: Great choice! Typer provides excellent type safety...
```

## Anatomy of a TRD

A well-structured TRD includes:

```markdown
# Technical Requirements Document: [Project Name]

## Executive Summary
Brief technical overview.

## Architecture
### Pattern
How components are organized.

### Data Flow
How data moves through the system.

## Technology Stack
### Language & Runtime
Python version, etc.

### Dependencies
Packages and their purposes.

## Data Model
### Entities
Core data structures.

### Storage Format
How data is persisted.

## Development Practices
### Testing Strategy
Framework, coverage targets.

### Code Quality
Linting, formatting tools.

## Error Handling
How errors are managed.

## PRD Alignment
Mapping requirements to implementation.
```

## Example: Todo App TRD

Here are the key technical decisions for our Todo app:

### Architecture Pattern

**Layered Package Structure**

```
todo-app/
├── src/
│   └── todo/
│       ├── cli.py      # User interaction layer
│       ├── models.py   # Data structures layer
│       └── storage.py  # Persistence layer
└── tests/
```

**Why?** Clear separation of concerns makes code easier to test and maintain.

### Data Flow

```
User Input → CLI (Typer) → Models (dataclass) → Storage (JSON) → File
                ↓
            Output (Rich)
```

### Technology Choices

| Choice | Selected | Why |
|--------|----------|-----|
| Language | Python 3.9+ | Wide compatibility, excellent for CLI |
| CLI Framework | Typer | Modern, type-hint based, auto-generates help |
| Output Styling | Rich | Beautiful terminal output (comes with Typer) |
| Data Format | JSON | Human-readable, no extra dependencies |
| Testing | pytest | Industry standard, excellent fixtures |
| Linting | ruff | Fast, replaces multiple tools |
| Formatting | black | Consistent, no debates |
| Type Checking | mypy | Catches bugs before runtime |

### Data Model

**TodoItem** as a dataclass:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class TodoItem:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
```

**Why dataclass?**
- Less boilerplate than regular classes
- Built-in `__init__`, `__repr__`, etc.
- Works well with type hints

### Storage Format

**Location**: `~/.todo.json`

```json
{
  "version": "1.0",
  "todos": [
    {
      "id": "a1b2c3d4",
      "title": "Learn EPCC workflow",
      "completed": false,
      "created_at": "2025-11-30T10:00:00",
      "completed_at": null
    }
  ]
}
```

**Why JSON?**
- Human-readable (can inspect manually)
- No external database needed
- Python has built-in support

### Testing Strategy

| Test Type | File | Coverage |
|-----------|------|----------|
| Unit | test_models.py | TodoItem creation, serialization |
| Unit | test_storage.py | Load, save, edge cases |
| Integration | test_cli.py | Full command execution |

**Target**: 80%+ line coverage

### Development Workflow

```bash
# Quality commands
black src tests              # Format
ruff check --fix src tests   # Lint + auto-fix
mypy src                     # Type check
pytest -v --cov=src          # Test with coverage
```

## Hands-On: Create Your TRD

Now create a TRD for your Todo app:

1. **Ensure you have a PRD** from the previous module

2. **Run the TRD command**:
   ```
   /trd
   ```

3. **Answer technical questions** about your preferences

4. **Review the output** - it generates a complete TRD

5. **Save if needed** - typically saved as `TRD.md` or `TECH_REQ.md`

### Tips for Good TRDs

- **Justify decisions** - explain "why", not just "what"
- **Consider alternatives** - note what you didn't choose and why
- **Keep it practical** - focus on decisions that affect implementation
- **Reference the PRD** - show how technical choices support features

## Decision-Making Framework

When making technical decisions, consider:

```
┌─────────────────────────────────────────────────┐
│           Technical Decision Framework          │
├─────────────────────────────────────────────────┤
│ 1. Does it solve the requirement?               │
│ 2. Is it the simplest solution?                 │
│ 3. Is it maintainable?                          │
│ 4. Does the team know it?                       │
│ 5. Is it well-supported/documented?             │
└─────────────────────────────────────────────────┘
```

For our Todo app, Typer beats argparse because:
- ✅ Solves the requirement (CLI framework)
- ✅ Simple (uses type hints you already write)
- ✅ Maintainable (clean, readable code)
- ✅ Well-documented with active development

## Key Takeaways

- **TRD answers "how"** - Technology, architecture, data models
- **Use `/trd` command** to create TRDs interactively
- **Document decisions** with rationale (the "why")
- **Keep it practical** - focus on what affects implementation
- **Map to PRD** - show how technical choices support features

## What's Next?

We now know *what* we're building (PRD) and *how* we'll build it (TRD). Time to create an implementation plan!

→ **[Next: Plan Phase](./03-plan-phase.md)**

---

*Estimated time for this module: 15-20 minutes*
