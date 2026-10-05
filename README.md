# skills

A collection of AI agent skills compatible with [skills.sh](https://skills.sh/) and the `skills` CLI.

## Available Skills

### [`plexy-clean-code`](./plexy-clean-code/SKILL.md)

- Relies on exceptions and stack traces instead of custom error messages.
- Makes fields private whenever possible.

### [`plexy-do-less`](./plexy-do-less/SKILL.md)

- Keeps exploration, analysis, delegation, and explanation proportional to the task.
    - Preserves necessary context and verification.

### [`plexy-follow-the-rules`](./plexy-follow-the-rules/SKILL.md)

- Follows explicit guidelines, user-designated references, and established project idioms.
    - Matches implementation conventions beyond formatting, including libraries and boilerplate-reduction tools.

### [`plexy-kiss`](./plexy-kiss/SKILL.md)

- Keeps the requested solution readable and maintainable without speculative complexity.
    - Uses precise abstractions and meaningful `DRY` rather than minimizing lines or dependencies blindly.

### [`plexy-markdown`](./plexy-markdown/SKILL.md)

Formats Markdown as tight bullets: one statement per bullet, sub-bullets for sub-statements, lines under 120 chars.

### [`plexy-nukeduck`](./plexy-nukeduck/SKILL.md)

Rewrites arbitrary works of literature with full commitment by turning every character into a duck.

### [`plexy-spawn`](./plexy-spawn/SKILL.md)

Decomposes complex tasks into concurrent subagents (swarm execution) with clear boundaries and join points.

### [`plexy-teach`](./plexy-teach/SKILL.md)

Builds dense, research-grounded HTML lessons with mechanisms, contrasts, retrieval practice, and transfer tasks.

### [`plexy-tickets`](./plexy-tickets/SKILL.md)

- Turns plans into verifiable local tickets with explicit blockers and approval before writing files.
    - Saves one Markdown file per ticket under `.agents/issues/<feature-slug>/` in the target project.

## Installation

Install a skill via the `skills` CLI:

```bash
# Install to your current project
npx skills add IO42630/skills@plexy-do-less

# Or install globally for your agents
npx skills add IO42630/skills@plexy-do-less -g
```

## One-off Usage (without installing)

```bash
npx skills use IO42630/skills@plexy-markdown
```
