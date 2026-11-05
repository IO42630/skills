# skills

A collection of AI agent skills compatible with [skills.sh](https://skills.sh/) and the `skills` CLI.

## Available Skills

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

### [`plexy-save`](./plexy-save/SKILL.md)

- Updates the repository's `AGENTS.md` model and saves a session checkpoint under `.agents/saves/`.

### [`plexy-sheep`](./plexy-sheep/SKILL.md)

- Keeps project changes native to established conventions.
    - Uses comparable precedent and asks before introducing unauthorized constructs.

## Installation

Install a skill via the `skills` CLI:

```bash
# Install to your current project
npx skills add IO42630/skills@plexy-markdown

# Or install globally for your agents
npx skills add IO42630/skills@plexy-markdown -g
```

## One-off Usage (without installing)

```bash
npx skills use IO42630/skills@plexy-markdown
```
