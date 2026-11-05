# skills

A collection of AI agent skills compatible with [skills.sh](https://skills.sh/) and the `skills` CLI.

## Available Skills

### [`com-olexyn-tabdriver`](./com-olexyn-tabdriver/SKILL.md)

- Guides integration of `com.olexyn:tabdriver` browser automation in Java applications.
    - Covers configuration, a shared driver, named tabs, and session handling.

### [`plexy-clean-code`](./plexy-clean-code/SKILL.md)

- Relies on exceptions and stack traces instead of custom error messages.
- Makes fields private whenever possible.

### [`plexy-do-less`](./plexy-do-less/SKILL.md)

- Keeps exploration, analysis, delegation, and explanation proportional to the task.
    - Preserves necessary context and verification.

### [`plexy-follow-the-rules`](./plexy-follow-the-rules/SKILL.md)

- Follows explicit guidelines, user-designated references, and established project idioms.
    - Matches implementation conventions beyond formatting, including libraries and boilerplate-reduction tools.

### [`plexy-java`](./plexy-java/SKILL.md)

- Defines Java conventions for imports, code style, null handling, dependencies, and line breaks.

### [`plexy-kiss`](./plexy-kiss/SKILL.md)

- Keeps the requested solution readable and maintainable without speculative complexity.
    - Uses precise abstractions and meaningful `DRY` rather than minimizing lines or dependencies blindly.

### [`plexy-markdown`](./plexy-markdown/SKILL.md)

Formats Markdown as tight bullets: one statement per bullet, sub-bullets for sub-statements, lines under 120 chars.

### [`plexy-markdown-update`](./plexy-markdown-update/SKILL.md)

- Preserves wording and structure when updating Markdown.
    - Applies its diff-preserving guidance only when explicitly asked to update existing Markdown.

### [`plexy-probe`](./plexy-probe/SKILL.md)

- Runs a one-question-at-a-time probe that sharpens a plan, design, or decision.
    - Tracks every question and answer in `.agents/probes/probe-NN_<slug>.md`.
    - Stops on `end probe` and closes with a shared-understanding summary.

### [`plexy-recipe`](./plexy-recipe/SKILL.md)

- Captures code patterns as self-contained reusable recipes under `.agents/recipes/`.
    - Finds and applies existing recipes when implementation is requested.

### [`plexy-robot`](./plexy-robot/SKILL.md)

- Keeps replies terse, dense, and direct without losing technical accuracy or necessary detail.

### [`plexy-sheep`](./plexy-sheep/SKILL.md)

- Keeps project changes native to established conventions.
    - Uses comparable precedent and asks before introducing unauthorized constructs.

### [`plexy-skill-review`](./plexy-skill-review/SKILL.md)

- Reviews a selected skill bundle for exposed proprietary information, credentials, and personal data.
    - Reports redacted evidence and coverage gaps without claiming a guarantee of safety.

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
