# Plan Phase: Designing the Implementation

## Learning Objectives

By the end of this module, you will:
- Understand why we skip Explore for greenfield projects
- Know how to use the `/epcc-plan` command
- See how to break features into actionable tasks
- Have an example implementation plan for our Todo app

## Why Skip Explore for Greenfield?

Remember from the [Introduction](./00-introduction.md):

- **Greenfield** = starting from scratch (no existing code)
- **Brownfield** = working with existing code

When starting fresh, there's nothing to explore! You go directly to planning:

```
Greenfield:  PRD → TRD → Plan → Code → Commit
                      (no Explore)

Brownfield:  PRD → TRD → Explore → Plan → Code → Commit
```

Our Todo app is greenfield, so we'll skip Explore and jump straight to planning.

> **Note**: After building the app, you can practice Explore using it as a "brownfield" codebase. See [Explore Phase](./06-explore-phase.md) for that optional exercise.

## What is Planning?

The Plan phase creates a **roadmap** from requirements to implementation:

```
PRD Features  →  PLAN Tasks  →  Actual Code
   (what)         (how/when)      (done!)
```

A good plan:
- **Breaks down** large features into small, achievable tasks
- **Orders** tasks by dependencies (what must be done first)
- **Estimates** effort to set expectations
- **Identifies risks** before they become blockers

## Using the /epcc-plan Command

The `/epcc-plan` command reads your PRD and TRD, then creates an implementation plan.

### Starting a Plan Session

```bash
# In Claude Code, after you have PRD and TRD:
/epcc-plan

# Or with specific focus:
/epcc-plan implement the Todo app
```

### What the Command Does

1. **Reads context** - PRD.md, TRD.md, any existing code
2. **Breaks down features** - Creates task list from requirements
3. **Determines order** - Identifies dependencies between tasks
4. **Generates plan** - Outputs structured implementation roadmap

### Example Output

```markdown
# Plan: Todo App

## 1. Objective
Build a CLI todo application with JSON persistence.

## 2. Approach
Bottom-up: Models → Storage → CLI

## 3. Tasks
1. Project setup (pyproject.toml, directories)
2. TodoItem dataclass (models.py)
3. JSON storage layer (storage.py)
4. CLI commands (cli.py)
5. Tests (test_*.py)
6. Documentation (README.md)

## 4. Sequence
Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6
```

## Anatomy of a Good Plan

A well-structured plan includes:

```markdown
# Plan: [Project Name]

## 1. Objective
What we're trying to achieve (summary of PRD goals).

## 2. Approach
Overall strategy - top-down, bottom-up, feature-slice, etc.

## 3. Tasks
Detailed task list with:
- Clear description
- Estimated effort
- Dependencies
- Risks

## 4. Quality Strategy
How we'll ensure code quality (tests, coverage targets).

## 5. Risks
What might go wrong and how we'll handle it.

## 6. Implementation Sequence
Ordered list showing task dependencies.
```

## Example: Todo App Plan

Here's a real implementation plan for our Todo app:

### Objective

Build a CLI todo application with:
- Add, list, complete, delete commands
- JSON file persistence
- 80%+ test coverage

### Approach

**Bottom-Up Implementation**

Build foundational layers first, then layer on top:

```
1. Models (data structures)
        ↓
2. Storage (persistence)
        ↓
3. CLI (user interface)
        ↓
4. Tests (verification)
```

**Why bottom-up?** Each layer only depends on layers below it, making testing easier.

### Task Breakdown

| # | Task | Effort | Depends On |
|---|------|--------|------------|
| 1 | Create project structure | 0.5h | - |
| 2 | Implement TodoItem dataclass | 0.5h | 1 |
| 3 | Implement storage.py | 1h | 2 |
| 4 | Implement CLI commands | 1h | 3 |
| 5 | Create entry point | 0.25h | 4 |
| 6 | Write tests | 1h | 5 |
| 7 | Write README | 0.25h | 6 |

**Total**: ~4.5 hours

### Task Details

#### Task 1: Project Structure
```
todo-app/
├── pyproject.toml
├── src/
│   └── todo/
│       └── __init__.py
└── tests/
    └── __init__.py
```

#### Task 2: TodoItem Model
- Create `models.py`
- Define `TodoItem` dataclass
- Add `to_dict()` and `from_dict()` methods

#### Task 3: Storage Layer
- Create `storage.py`
- Functions: `load_todos()`, `save_todos()`, `get_by_id()`
- Handle file not found, corrupted JSON

#### Task 4: CLI Commands
- Create `cli.py`
- Commands: `add`, `list`, `complete`, `delete`, `clear`
- Use Rich for colored output

#### Task 5: Entry Point
- Create `__main__.py`
- Enable `python -m todo` execution

#### Task 6: Tests
- `test_models.py` - TodoItem tests
- `test_storage.py` - Storage tests
- `test_cli.py` - CLI integration tests
- Target: 80%+ coverage

#### Task 7: README
- Installation instructions
- Usage examples
- Development setup

### Implementation Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                    Critical Path                            │
├─────────────────────────────────────────────────────────────┤
│ Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7│
│ setup   models  storage   CLI      entry   tests    docs   │
└─────────────────────────────────────────────────────────────┘
```

### Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| JSON corruption | M | Add error handling, graceful fallback |
| Path issues on Windows | L | Use pathlib consistently |
| Typer API changes | L | Pin version in pyproject.toml |

## Hands-On: Create Your Plan

Create an implementation plan for your Todo app:

1. **Ensure you have PRD and TRD** from previous modules

2. **Run the plan command**:
   ```
   /epcc-plan
   ```

3. **Review the generated plan** - does it cover all PRD features?

4. **Refine if needed** - ask Claude to adjust tasks or estimates

### Tips for Good Plans

- **Small tasks** - If a task takes > 2 hours, break it down further
- **Clear dependencies** - Know what blocks what
- **Test early** - Don't save all testing for the end
- **Be realistic** - Add buffer time for unexpected issues

## Plan vs Backlog

A plan is not a backlog:

| Plan | Backlog |
|------|---------|
| Sequential tasks for one feature | All features for a product |
| Has implementation order | Prioritized but not ordered |
| Time-bounded | Ongoing |
| Created once, follows through | Continuously updated |

Your EPCC plan is for **one coding session** or feature implementation.

## Key Takeaways

- **Skip Explore for greenfield** - nothing to explore yet
- **Use `/epcc-plan`** to generate implementation roadmap
- **Break down features** into small, achievable tasks
- **Identify dependencies** to determine task order
- **Consider risks** before they become blockers

## What's Next?

We have our plan! Time to write some code.

→ **[Next: Code Phase](./04-code-phase.md)**

---

*Estimated time for this module: 15-20 minutes*
