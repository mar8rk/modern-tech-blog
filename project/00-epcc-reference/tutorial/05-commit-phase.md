# Commit Phase: Finalizing with Confidence

## Learning Objectives

By the end of this module, you will:
- Know how to use the `/epcc-commit` command
- Understand quality checks to run before committing
- Write good commit messages
- Complete the greenfield EPCC workflow

## What is the Commit Phase?

The Commit phase is the final step where you:

1. **Verify quality** - Run all checks to ensure code is ready
2. **Review changes** - Understand what you're committing
3. **Write a good message** - Document what and why
4. **Commit with confidence** - Ship it!

```
Code Complete → Quality Checks → Review Changes → Commit
```

This isn't just `git commit` - it's a quality gate that ensures your code is ready for others (or your future self).

## Using the /epcc-commit Command

The `/epcc-commit` command runs pre-commit checks and helps you create quality commits.

### Starting a Commit Session

```bash
# In Claude Code, after completing your code:
/epcc-commit

# Or with a message hint:
/epcc-commit "Add todo CRUD functionality"
```

### What the Command Does

1. **Runs quality checks** - Format, lint, type check, tests
2. **Shows changes** - What files are modified
3. **Generates commit message** - Based on changes made
4. **Creates the commit** - After verification passes

### Command Options

| Flag | Purpose |
|------|---------|
| `--amend` | Amend the previous commit |
| `--squash` | Squash multiple commits into one |
| (none) | Standard commit flow |

## Quality Checks

Before committing, run these checks:

### 1. Formatting (Black)

```bash
black src tests
```

Black ensures consistent code style. No debates about formatting!

**Before Black:**
```python
def add_todo(title:str,path:Optional[Path]=None)->TodoItem:
    todos=load_todos(path)
    new_todo=TodoItem(title=title)
```

**After Black:**
```python
def add_todo(title: str, path: Optional[Path] = None) -> TodoItem:
    todos = load_todos(path)
    new_todo = TodoItem(title=title)
```

### 2. Linting (Ruff)

```bash
ruff check --fix src tests
```

Ruff catches issues like:
- Unused imports
- Undefined variables
- Style violations
- Potential bugs

**Example Output:**
```
src/todo/cli.py:5:1: F401 [*] `os` imported but unused
Found 1 error.
[*] 1 fixable with the `--fix` option.
```

### 3. Type Checking (Mypy)

```bash
mypy src
```

Mypy verifies type annotations are correct:

**Example Error:**
```
src/todo/storage.py:45: error: Argument 1 to "save_todos" has
incompatible type "str"; expected "list[TodoItem]"
```

### 4. Tests (Pytest)

```bash
pytest -v --cov=src
```

All tests must pass before committing:

```
============= test session starts =============
tests/test_models.py::TestTodoItem::test_create_todo_with_title PASSED
tests/test_models.py::TestTodoItem::test_complete_todo PASSED
tests/test_storage.py::TestLoadSave::test_add_and_load PASSED
...
============= 41 passed in 0.52s ==============

---------- coverage: 96% ----------
```

### All-in-One Check

Run all checks in sequence:

```bash
black --check src tests && \
ruff check src tests && \
mypy src && \
pytest -v --cov=src
```

If any step fails, fix it before committing.

## Reviewing Changes

Before committing, always review what you're about to commit:

### Check Status

```bash
git status
```

Shows modified, added, and untracked files:

```
Changes not staged for commit:
  modified:   src/todo/models.py
  modified:   src/todo/storage.py

Untracked files:
  src/todo/cli.py
  tests/test_cli.py
```

### Check Diff

```bash
git diff
```

Shows line-by-line changes. Look for:
- Unintended changes
- Debug code left in
- Commented-out code
- Sensitive data (API keys, passwords)

## Writing Good Commit Messages

A good commit message explains **what** changed and **why**.

### Format

```
<type>: <short summary>

<detailed explanation if needed>
```

### Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation changes |
| `test` | Adding or updating tests |
| `chore` | Maintenance (deps, configs) |

### Examples

**Good:**
```
feat: Add todo CRUD functionality

- Add TodoItem dataclass with serialization
- Implement JSON storage layer
- Add Typer CLI with add/list/complete/delete commands
- Include pytest tests with 96% coverage
```

**Bad:**
```
updated code
```

```
fix stuff
```

### Tips for Good Messages

1. **Use imperative mood** - "Add feature" not "Added feature"
2. **Be specific** - What exactly changed?
3. **Explain why** - If not obvious, explain the reasoning
4. **Keep first line < 50 chars** - For readability in logs
5. **Reference issues** - If fixing a bug, mention the issue number

## The Complete Commit Flow

Here's the full process from code completion to commit:

```bash
# 1. Run quality checks
black src tests
ruff check --fix src tests
mypy src
pytest -v --cov=src

# 2. Review changes
git status
git diff

# 3. Stage files
git add src/ tests/ pyproject.toml

# 4. Commit with message
git commit -m "feat: Add todo CRUD functionality

- TodoItem dataclass with JSON serialization
- Storage layer with load/save operations
- Typer CLI commands: add, list, complete, delete, clear
- 41 tests with 96% coverage"
```

## Hands-On: Commit Your Todo App

If you've been building along, commit your work:

### Step 1: Run Quality Checks

```bash
cd todo-app

# Format
black src tests

# Lint
ruff check --fix src tests

# Type check
mypy src

# Test
pytest -v --cov=src
```

### Step 2: Review Changes

```bash
git status
git diff
```

### Step 3: Stage and Commit

```bash
# Stage all todo-app files
git add .

# Commit with message
git commit -m "feat: Implement todo CLI application

- TodoItem dataclass with JSON serialization
- Storage layer with CRUD operations
- Typer CLI with add/list/complete/delete/clear commands
- Comprehensive pytest suite with fixtures"
```

Or use the EPCC command:

```
/epcc-commit
```

## What Happens After Commit?

Once committed, your code is:
- **Saved** in version control
- **Documented** with your commit message
- **Ready** for collaboration (push to remote)

### Optional: Push to Remote

```bash
git push origin main
```

## Key Takeaways

- **Always verify before committing** - Format, lint, type check, test
- **Review your changes** - Know exactly what you're committing
- **Write meaningful messages** - Help future you and others
- **Use `/epcc-commit`** for guided commit flow

## Greenfield Workflow Complete!

Congratulations! You've completed the greenfield EPCC workflow:

```
✓ PRD    - Defined what to build
✓ TRD    - Designed how to build it
✓ Plan   - Created implementation roadmap
✓ Code   - Implemented with tests
✓ Commit - Verified and shipped
```

## What's Next?

Want to learn the Explore phase for brownfield development? Practice exploring the Todo app you just built as if it were unfamiliar code:

→ **[Next: Explore Phase (Optional)](./06-explore-phase.md)**

Or jump to the quick reference:

→ **[Quick Reference](./07-quick-reference.md)**

---

*Estimated time for this module: 15-20 minutes*
