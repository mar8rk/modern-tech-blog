# Quick Reference

A cheat sheet for the EPCC workflow and commands.

## EPCC Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/prd` | Create Product Requirements | Start of any project |
| `/trd` | Create Technical Requirements | After PRD is complete |
| `/epcc-explore` | Understand existing code | Brownfield only |
| `/epcc-plan` | Create implementation plan | Before coding |
| `/epcc-code` | Implement with guidance | During development |
| `/epcc-commit` | Verify and commit | After code complete |
| `/epcc-resume` | Resume multi-session work | Continuing work |

## Workflow Decision Tree

```
Starting a new feature?
        │
        ▼
┌───────────────────┐
│ Do you have a PRD?│
└───────────────────┘
        │
   ┌────┴────┐
   NO        YES
   │         │
   ▼         ▼
 /prd    ┌───────────────────┐
         │ Do you have a TRD?│
         └───────────────────┘
                 │
            ┌────┴────┐
            NO        YES
            │         │
            ▼         ▼
          /trd   ┌─────────────────────┐
                 │ Is there existing   │
                 │ code to work with?  │
                 └─────────────────────┘
                         │
                    ┌────┴────┐
                    NO        YES
                    │         │
                    ▼         ▼
              /epcc-plan   /epcc-explore
                    │         │
                    ▼         ▼
              /epcc-code   /epcc-plan
                    │         │
                    ▼         ▼
              /epcc-commit /epcc-code
                              │
                              ▼
                         /epcc-commit
```

## Greenfield vs Brownfield

| Aspect | Greenfield | Brownfield |
|--------|------------|------------|
| Definition | New project from scratch | Existing codebase |
| Use Explore? | No | Yes |
| Workflow | PRD → TRD → Plan → Code → Commit | PRD → TRD → Explore → Plan → Code → Commit |
| Examples | New apps, prototypes | Bug fixes, new features |

## Command Options

### /epcc-explore

| Flag | Purpose |
|------|---------|
| `--deep` | Thorough analysis |
| `--quick` | Overview only |
| `--refresh` | Ignore cached knowledge |

### /epcc-plan

```bash
/epcc-plan                    # Generate plan from PRD/TRD
/epcc-plan implement auth     # Focus on specific area
```

### /epcc-code

| Flag | Purpose |
|------|---------|
| `--tdd` | Test-first development |
| `--quick` | Faster iteration |
| `--full` | Comprehensive with docs |

### /epcc-commit

| Flag | Purpose |
|------|---------|
| `--amend` | Amend previous commit |
| `--squash` | Squash commits |

## Quality Check Commands

```bash
# Format code
black src tests

# Lint and auto-fix
ruff check --fix src tests

# Type check
mypy src

# Run tests with coverage
pytest -v --cov=src

# All-in-one check
black --check src tests && ruff check src tests && mypy src && pytest
```

## Commit Message Format

```
<type>: <short summary>

<detailed explanation if needed>
```

### Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring |
| `docs` | Documentation |
| `test` | Tests |
| `chore` | Maintenance |

### Example

```
feat: Add todo CRUD functionality

- TodoItem dataclass with serialization
- JSON storage layer
- Typer CLI commands
- 96% test coverage
```

## Python Quality Tools

| Tool | Purpose | Command |
|------|---------|---------|
| black | Formatting | `black .` |
| ruff | Linting | `ruff check .` |
| mypy | Type checking | `mypy src` |
| pytest | Testing | `pytest -v` |
| pytest-cov | Coverage | `pytest --cov=src` |

## Project Setup Commands

### With uv (Recommended)

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

### With pip

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Common Patterns

### TDD Cycle

```
1. Write failing test (Red)
2. Write code to pass (Green)
3. Refactor (Clean)
4. Repeat
```

### Layer Order (Bottom-Up)

```
1. Models (data structures)
2. Storage (persistence)
3. CLI (user interface)
4. Tests (verification)
```

### Exploration Order

```
1. README/docs
2. Config files (pyproject.toml)
3. Tests (expected behavior)
4. Entry points
5. Core logic
```

## Useful Links

- [Introduction](./00-introduction.md) - EPCC overview
- [PRD Phase](./01-prd-phase.md) - Product requirements
- [TRD Phase](./02-trd-phase.md) - Technical requirements
- [Plan Phase](./03-plan-phase.md) - Implementation planning
- [Code Phase](./04-code-phase.md) - Development
- [Commit Phase](./05-commit-phase.md) - Quality and commit
- [Explore Phase](./06-explore-phase.md) - Codebase exploration
- [Todo App](./todo-app/README.md) - Reference implementation

---

*Keep this page handy as you use the EPCC workflow!*
