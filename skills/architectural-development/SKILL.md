---
name: architectural-development
description: Facilitates software engineering discussions, task planning, and project scaffolding. Helps establish solid, modular, and scalable foundations before implementation.
---

# Architectural Development

This skill helps structure conversations around software design, task planning, technical decision-making, and project architecture. It prevents rushing into coding by ensuring requirements and scalable foundations are solid first.

## Trigger Keywords

Activate this skill if the request mentions any of the following:
- project architecture
- project structure
- folder structure
- scalable react
- scaffold project
- modular design
- feature-driven
- separation of concerns
- brainstorm
- discuss design
- architecture
- RFC (Request for Comments)
- design doc
- pair programming
- plan out a feature
- pros and cons
- technical decision

## Core Workflows

Adopt one of the following structured workflows based on the user's intent:

### 1. Architectural Design & Scaffolding 📐
*Goal: Establish a solid, scalable foundation for new or refactored projects.*
- **Scope Phase**: Ask the user about the project scale (prototype, dashboard, enterprise app).
- **Framework Phase**: Determine the primary framework (React, Next.js, Vue) and state management.
- **Structure Phase**: Propose a "Feature-First Organization" (e.g., `src/features/auth`) rather than grouping by file type.
- **Performance Phase**: Discuss data fetching (e.g., React Query) and code-splitting boundaries.
- **Interaction Rule**: Provide the root directory tree using markdown first. Explain the reasoning and ask for confirmation before generating 50 files.

### 2. Engineering RFC Mode 🧠
*Goal: Solidify a specific technical decision before implementation.*
- **Requirements**: Clearly list functional and non-functional requirements.
- **Propose System**: Outline data models, system components, and API contracts.
- **Discuss Trade-offs**: For every major decision, explicitly list **Pros**, **Cons**, and **Alternatives Considered**.
- **Checkpoint**: Ensure the user approves the specific design before suggesting actual code. (Use `resources/rfc-template.md` as a guide).

### 3. Task Planning Mode 📝
*Goal: Break down a large feature into executable steps.*
- **Define Scope**: Define the MVP (Minimum Viable Product).
- **Component Breakdown**: Break the feature into granular, dependent tasks (Database -> API -> UI).
- **Execution Plan**: Present an ordered checklist for implementation. 

## Best Practices & Principles
- **Separation of Concerns**: Separate UI components from business logic. Keep API calls out of React components.
- **Shared Kernel**: Place truly generic code in a `src/shared` or `src/common` folder.
- **Progressive Disclosure**: Do not overwhelm the user with a giant wall of text. Present high-level ideas first.
- **Decision Checkpoints**: Frequently pause and ask for explicit confirmation: "Are you happy with this approach?"
- **Log Decisions**: If a major technical pivot is agreed upon, offer to summarize the outcome using `resources/decision-log-template.md`.
