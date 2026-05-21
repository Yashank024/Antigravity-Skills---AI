---
name: creating-antigravity-skills
description: Generates high-quality, predictable, and efficient Antigravity skills based on the antigravity-skill-creator.md specification. Use when building new agent capabilities.
---

# Creating Antigravity Skills (Meta-Skill)

This skill empowers the agent to act as a Master Skill Architect. It strictly enforces the standard Antigravity skill structure and YAML rules to ensure newly generated skills are fully functional and predictable.

## Trigger Keywords
Activate this skill if the request mentions:
- create skill
- new skill
- new agent capabilities
- new creation
- create a skill
- build a skill
- antigravity-skill-creator.md
- skill generator
- new agent capability

## The 4-Step Generation Workflow

When tasked with generating a new skill, you MUST follow this 4-step internal process before outputting the final directory structure.

### 1. Research (Concept Understanding) 🔍
- **Simulate Deep Research**: If you lack direct internet access to Antigravity docs and GitHub repos, utilize your internal knowledge of modern software engineering patterns, coding automation tools, and agent workflows.
- Extract the core concepts, common pitfalls, and best practices for the user's requested domain (e.g., React testing, database deployment).

### 2. Plan (Architecture Design) 📝
- Outline an internal plan. Define the exact goal of the new skill.
- Identify the necessary trigger keywords.
- Decide if the new skill requires secondary files (like `scripts/` or `examples/`) based on the task complexity.
- Formulate the markdown checklist the new skill will use to track its own state.

### 3. Validate (Specification Check) ✅
Before generating the files, mentally validate your plan against the strict Antigravity rules:
- [ ] Is the proposed folder structure correct (`<skill-name>/SKILL.md`)?
- [ ] Is the proposed `name` in the YAML frontmatter in **gerund form** (ending in -ing, e.g., `testing-components`, max 64 chars, lowercase/hyphens only)?
- [ ] Is the `description` written in the **third person** and under 1024 characters? Does it contain explicit trigger keywords?
- [ ] Does the proposed `SKILL.md` body follow Progressive Disclosure (under 500 lines, pushing complex logic to secondary files)?
- [ ] Does the proposed logic rely on Bullet Points (high freedom), Code Blocks (templates), or Bash Commands (low freedom) correctly?

### 4. Execute (Generation) ⚡
Output the final skill using the exact format defined in `resources/skill-template.md`.

## Instructions for Execution
When generating the final output, always use forward slashes `/` for paths. Never include "claude" or "anthropic" in any names.
If the requested skill involves complex operations (like database migrations or deployments), force the generated skill to include a "Plan-Validate-Execute" loop of its own.

## Resources
- [Skill Template Blueprint](resources/skill-template.md)
