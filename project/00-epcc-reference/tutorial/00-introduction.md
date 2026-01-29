# Introduction to the EPCC Workflow

## Learning Objectives

By the end of this module, you will:
- Understand what EPCC stands for and the purpose of each phase
- Know the difference between greenfield and brownfield development
- Have your environment set up and ready to follow the tutorial

## What is EPCC?

**EPCC** stands for **Explore → Plan → Code → Commit**. It's a structured workflow for software development that helps you:

1. **Understand** before you build
2. **Plan** before you code
3. **Implement** with confidence
4. **Ship** with quality

```
┌─────────────────────────────────────────────────────────────────┐
│                       EPCC Workflow                             │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│   EXPLORE   │    PLAN     │    CODE     │      COMMIT         │
├─────────────┼─────────────┼─────────────┼─────────────────────┤
│ Understand  │ Design the  │ Implement   │ Verify & ship       │
│ the context │ approach    │ features    │ with confidence     │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
```

### The Four Phases

| Phase | Command | Purpose |
|-------|---------|---------|
| **Explore** | `/epcc-explore` | Understand existing code, patterns, and architecture |
| **Plan** | `/epcc-plan` | Design implementation strategy and break down tasks |
| **Code** | `/epcc-code` | Implement features with TDD and quality practices |
| **Commit** | `/epcc-commit` | Verify quality and finalize changes |

## Prerequisites: PRD and TRD

Before starting EPCC, you should have:

1. **PRD (Product Requirements Document)** - Defines *what* you're building
   - Created using the `/prd` command
   - Captures user needs, features, and success criteria

2. **TRD (Technical Requirements Document)** - Defines *how* you'll build it
   - Created using the `/trd` command
   - Documents technology choices and architecture decisions

The complete flow looks like this:

```
PRD → TRD → EPCC (Explore → Plan → Code → Commit)
```

## Greenfield vs Brownfield

The EPCC workflow adapts based on whether you're starting fresh or working with existing code:

### Greenfield Development (New Projects)

When you're building something **from scratch**, there's no existing code to explore. You:

- **Skip the Explore phase** (nothing to explore yet!)
- Start directly with **Plan**

```
PRD → TRD → Plan → Code → Commit
         (skip Explore)
```

**Examples**: New apps, new features in empty repos, prototypes

### Brownfield Development (Existing Codebases)

When you're adding features to **existing code**, the Explore phase is essential:

- **Use Explore first** to understand patterns, conventions, and architecture
- Then **Plan** based on what you learned

```
PRD → TRD → Explore → Plan → Code → Commit
```

**Examples**: Bug fixes, adding features to existing apps, refactoring

### Decision Tree

```
Starting a new feature?
        │
        ▼
┌───────────────────┐
│ Is there existing │
│ code to work with?│
└───────────────────┘
        │
   ┌────┴────┐
   │         │
   ▼         ▼
  YES        NO
   │         │
   ▼         ▼
Brownfield  Greenfield
(Explore    (Skip to
 first)      Plan)
```

## About This Tutorial

In this tutorial, you'll learn EPCC by building a **Python Todo application**. We'll follow the **greenfield workflow** since we're starting from scratch:

1. **[PRD Phase](./01-prd-phase.md)** - Define what the Todo app should do
2. **[TRD Phase](./02-trd-phase.md)** - Choose technologies and architecture
3. **[Plan Phase](./03-plan-phase.md)** - Break down the implementation
4. **[Code Phase](./04-code-phase.md)** - Build the app with tests
5. **[Commit Phase](./05-commit-phase.md)** - Verify quality and commit

After completing the main tutorial, you can practice the **Explore phase** using the provided reference implementation:

6. **[Explore Phase](./06-explore-phase.md)** - Practice exploring "unfamiliar" code

## Prerequisites

Before starting, ensure you have:

### Required Software

- [ ] **Python 3.9+** installed
  ```bash
  python --version  # Should show 3.9 or higher
  ```

- [ ] **Claude Code** installed and authenticated
  ```bash
  claude --version
  ```

- [ ] **EPCC Plugin** installed
  - The plugin provides `/prd`, `/trd`, and `/epcc-*` commands

### Recommended: uv Package Manager

We recommend using `uv` for faster package management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

**Alternative**: You can use `pip` with a virtual environment instead:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Verify Your Setup

Run this quick check to confirm you're ready:

```bash
# Check Python
python --version

# Check Claude Code
claude --version

# Check EPCC commands are available (in Claude Code)
# Type /epcc- and you should see autocomplete suggestions
```

## Key Takeaways

- **EPCC** = Explore → Plan → Code → Commit
- **Greenfield** (new project) = Skip Explore, start with Plan
- **Brownfield** (existing code) = Start with Explore
- **PRD** defines *what*, **TRD** defines *how*
- Always plan before you code, verify before you commit

## Next Steps

Ready to begin? Let's start by learning how to create a PRD:

→ **[Next: PRD Phase](./01-prd-phase.md)**

---

*Estimated time for this module: 5-10 minutes*
