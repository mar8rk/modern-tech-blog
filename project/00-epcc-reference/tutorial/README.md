# EPCC Workflow Tutorial

Learn the **EPCC (Explore → Plan → Code → Commit)** workflow by building a Python Todo application.

## What You'll Learn

This tutorial teaches professional software development practices:

- **PRD** - Defining what to build (Product Requirements)
- **TRD** - Designing how to build it (Technical Requirements)
- **Explore** - Understanding existing codebases (brownfield)
- **Plan** - Creating implementation roadmaps
- **Code** - Implementing with quality practices (TDD)
- **Commit** - Verifying and shipping with confidence

## Prerequisites

- Python 3.9+
- Claude Code installed and authenticated
- EPCC plugin installed

## Tutorial Structure

### Main Tutorial (Greenfield Workflow)

Follow these modules in order to build a Todo app from scratch:

| Module | Topic | Time |
|--------|-------|------|
| [00-introduction](./00-introduction.md) | EPCC Overview | 5-10 min |
| [01-prd-phase](./01-prd-phase.md) | Product Requirements | 15-20 min |
| [02-trd-phase](./02-trd-phase.md) | Technical Requirements | 15-20 min |
| [03-plan-phase](./03-plan-phase.md) | Implementation Planning | 15-20 min |
| [04-code-phase](./04-code-phase.md) | Development | 30-45 min |
| [05-commit-phase](./05-commit-phase.md) | Quality & Commit | 15-20 min |

**Total: ~2-3 hours**

### Optional (Brownfield Practice)

After completing the main tutorial:

| Module | Topic | Time |
|--------|-------|------|
| [06-explore-phase](./06-explore-phase.md) | Codebase Exploration | 20-30 min |

### Reference

| Resource | Description |
|----------|-------------|
| [07-quick-reference](./07-quick-reference.md) | Command cheat sheet |
| [todo-app/](./todo-app/) | Working reference implementation |

## Quick Start

1. **Start with the introduction**:
   ```bash
   # Open the tutorial
   cd tutorial
   ```

2. **Follow the modules in order**, starting with [00-introduction.md](./00-introduction.md)

3. **Build your own Todo app** as you progress through each module

4. **Use the reference implementation** in `todo-app/` to verify your work

## Workflow Paths

### Greenfield (New Projects)

When starting from scratch, skip Explore:

```
PRD → TRD → Plan → Code → Commit
```

### Brownfield (Existing Code)

When working with existing code, start with Explore:

```
PRD → TRD → Explore → Plan → Code → Commit
```

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/prd` | Create Product Requirements Document |
| `/trd` | Create Technical Requirements Document |
| `/epcc-explore` | Understand existing codebase |
| `/epcc-plan` | Create implementation plan |
| `/epcc-code` | Implement with guidance |
| `/epcc-commit` | Verify and commit changes |

## Reference Implementation

The `todo-app/` directory contains a complete working implementation:

```
todo-app/
├── src/todo/
│   ├── models.py      # TodoItem dataclass
│   ├── storage.py     # JSON persistence
│   └── cli.py         # Typer commands
└── tests/             # pytest test suite
```

**Features:**
- Add, list, complete, delete todos
- JSON file persistence
- 96% test coverage
- Type-annotated code

See [todo-app/README.md](./todo-app/README.md) for usage instructions.

## Tips for Success

1. **Follow the order** - Each module builds on the previous
2. **Type the commands** - Don't just read, do!
3. **Check your work** - Use the reference implementation to verify
4. **Ask questions** - The EPCC commands are interactive

## Feedback

Found an issue or have suggestions? Let us know!

---

**Happy learning!** 🚀
