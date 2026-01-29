# PRD Phase: Defining What to Build

## Learning Objectives

By the end of this module, you will:
- Understand what a PRD is and why it matters
- Know how to use the `/prd` command to create one
- See an example PRD for our Todo application

## What is a PRD?

A **Product Requirements Document (PRD)** answers the question: **"What are we building?"**

It captures:
- **The problem** you're solving
- **Who** you're solving it for
- **What features** the solution needs
- **How** you'll measure success

### Why PRDs Matter

Without a PRD, you risk:

| Problem | Consequence |
|---------|-------------|
| No clear goal | Building features nobody needs |
| Scope creep | Never finishing the project |
| Miscommunication | Team members building different things |
| No success criteria | Not knowing when you're "done" |

A good PRD keeps everyone aligned and provides a north star for development decisions.

## Using the /prd Command

The `/prd` command guides you through creating a PRD interactively. Claude asks questions about your project and generates a structured document.

### Starting a PRD Session

```bash
# In Claude Code, type:
/prd Todo App

# Or just:
/prd
```

### The Interactive Process

When you run `/prd`, Claude will ask you questions about:

1. **Project basics** - What type of project? What language?
2. **Target users** - Who will use this? What's their skill level?
3. **Features** - What must it do? What's nice-to-have?
4. **Constraints** - Timeline, technical limitations, scope

### Example Interaction

Here's what a `/prd` session might look like:

```
You: /prd Todo App

Claude: I'll help you create a PRD for Todo App. Let me ask a few questions.

┌─────────────────────────────────────────────────┐
│ What type of project is this?                   │
├─────────────────────────────────────────────────┤
│ ○ Web Application                               │
│ ● CLI Tool                                      │
│ ○ Library/Package                               │
│ ○ Mobile App                                    │
└─────────────────────────────────────────────────┘

You: CLI Tool

Claude: Great choice! Next question...

┌─────────────────────────────────────────────────┐
│ What programming language?                      │
├─────────────────────────────────────────────────┤
│ ● Python                                        │
│ ○ JavaScript/TypeScript                         │
│ ○ Go                                            │
│ ○ Other                                         │
└─────────────────────────────────────────────────┘

You: Python

Claude: Perfect. Who is the target audience?
...
```

The command builds a complete PRD based on your answers.

## Anatomy of a PRD

A well-structured PRD typically includes these sections:

```markdown
# Product Requirement Document: [Project Name]

## Executive Summary
Brief overview of what we're building and why.

## Problem Statement
The pain point we're addressing.

## Target Users
Who will use this and what do they need?

## Goals & Success Criteria
How we'll measure if we succeeded.

## Core Features
### Must Have (P0)
- Critical functionality
### Should Have (P1)
- Important but not blocking
### Nice to Have (P2)
- Future considerations

## Technical Approach
High-level technical direction.

## Constraints
Limitations on scope, timeline, technology.

## Out of Scope
What we're explicitly NOT building.
```

## Example: Todo App PRD

Here's a real PRD for the Todo application we'll build:

### Executive Summary

A command-line Todo application that helps users track tasks. Simple, fast, and works entirely in the terminal.

### Problem Statement

Users need a quick way to manage tasks without leaving their terminal. Existing solutions are either too complex (web apps) or too limited (text files).

### Target Users

- **Developers** who live in the terminal
- **Students** learning professional development practices
- **Anyone** who wants a simple, local task manager

### Goals & Success Criteria

| Goal | Success Metric |
|------|----------------|
| Quick task entry | < 2 seconds to add a task |
| Persistent storage | Tasks survive terminal close |
| Easy retrieval | List tasks with single command |
| Completion tracking | Mark tasks done, see progress |

### Core Features

#### Must Have (P0)
- [ ] Add new todo items
- [ ] List all todos
- [ ] Mark todos as complete
- [ ] Delete todos
- [ ] Persist to local file

#### Should Have (P1)
- [ ] Clear completed items
- [ ] Partial ID matching (type "a1b" instead of full ID)
- [ ] Colored output

#### Nice to Have (P2)
- Due dates
- Priorities
- Tags/categories

### Technical Approach

- **Language**: Python 3.9+
- **CLI Framework**: Typer (modern, type-hint based)
- **Storage**: JSON file in user's home directory
- **Testing**: pytest

### Constraints

- CLI only (no web interface)
- Single-user (no authentication)
- Local storage only (no cloud sync)

### Out of Scope

- Web or mobile interface
- Multi-user collaboration
- Cloud synchronization
- Due date reminders/notifications

## Hands-On: Create Your PRD

Now it's your turn! Create a PRD for your own Todo app:

1. **Start Claude Code** in your project directory:
   ```bash
   cd your-project-folder
   claude
   ```

2. **Run the PRD command**:
   ```
   /prd Simple Todo App
   ```

3. **Answer the questions** - choose options that match your needs

4. **Review the output** - Claude generates a complete PRD

5. **Save if needed** - The PRD is typically saved as `PRD.md`

### Tips for Good PRDs

- **Be specific** about who the users are
- **Prioritize ruthlessly** - P0 should be truly essential
- **Define "out of scope"** explicitly to prevent creep
- **Keep it focused** - A PRD isn't a specification doc

## Key Takeaways

- **PRD answers "what"** - What problem? What features? What success looks like?
- **Use `/prd` command** to create PRDs interactively
- **Prioritize features** as P0 (must have), P1 (should have), P2 (nice to have)
- **Define boundaries** with explicit "out of scope" section

## What's Next?

Now that we know *what* we're building, we need to decide *how* to build it technically. That's where the TRD comes in.

→ **[Next: TRD Phase](./02-trd-phase.md)**

---

*Estimated time for this module: 15-20 minutes*
