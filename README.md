# laravel-superpowers

Laravel-specific workflow skills, agents, and hooks for [Claude Code](https://claude.ai/code) — designed to complement the [superpowers](https://github.com/anthropics/claude-plugins-official) base plugin.

📍 **[Roadmap](docs/ROADMAP.md)** — see what's planned + tracked GitHub issues organized by version
📊 **[Milestones](https://github.com/altraWeb/laravel-superpowers/milestones)** — V2-MVP / V2.1 / V2.2 / V3 progress
📋 **[Project board](https://github.com/altraWeb/laravel-superpowers/projects)** — live status across all issues

## Install

```bash
claude plugin marketplace add github:altraWeb/laravel-superpowers
claude plugin install laravel-superpowers@altraweb-laravel
```

## Configuration

Per-user and per-project settings via YAML. See [`docs/config.md`](docs/config.md) for the full reference.

```bash
# Scaffold a user-global config you can edit
python3 <plugin>/lib/config.py init

# See effective merged config with source attribution
python3 <plugin>/lib/config.py show
```

Requires Python 3.10+ with `pyyaml` and `jsonschema`. On Homebrew Python:

```bash
pip3 install --user --break-system-packages pyyaml jsonschema
```

## Skills

- **laravel-brainstorming** — Architecture brainstorming for Laravel: layers, Eloquent relationships, Events, Policies, queuing decisions
- **laravel-tdd** — TDD workflow with Pest: factories, HTTP testing, facade faking, Feature vs Unit
- **laravel-debugging** — Debugging with Laravel-specific tools: Telescope, query logging, queue introspection
- **laravel-code-review** — Code review checklist: N+1, mass assignment, authorization, validation, security

## Agents

- **laravel-best-practices** — Web research agent for current Laravel best practices (Spatie, Laracasts, Laravel News). Use when asking *"how should I implement X?"* or *"is my current approach still best practice?"*.
- **laravel-livewire-specialist** — Audits Livewire-touching code/plans for fabricated APIs, `wire:ignore` zones, Form-Object patterns, Echo/broadcasting race conditions, and lifecycle-hook misuse. Verifies via PHP reflection against the actual Livewire vendor source — ground truth, not docs. Use before any Livewire-touching implementation phase.
- **laravel-pest-specialist** — Audits Pest 4 tests for variadic-API misuse (`toContain($needle, $message)` gotcha), browser-plugin smells (`wait(N)` abuse), view-context anti-patterns (reserved-name keys), test-location mismatches, and `it()`/`arch()`/dataset block correctness. Verifies via PHP reflection against the actual Pest vendor source. Use before any test write/edit.
- **laravel-flux-pro-specialist** — Audits Flux Pro v2 Blade components for double-tooltip wrapping (a11y break on `<ui-toolbar>` roving-tabindex), position/align convention drift, `<flux:editor.spacer/>` misplacement, `wire:ignore`-zone reactive-descendant issues on Flux components, and slot-vs-string-prop trade-offs. Reads `vendor/livewire/flux-pro/stubs/resources/views/flux/` as ground truth, cites file:line in findings. Use before any `<flux:*>` write/edit.
- **laravel-architect** — Audits Eloquent + architecture decisions: N+1 detection in `foreach`/`->each()` blocks, sibling-canon-aware pattern recommendations (Actions vs Services), flags Repository anti-pattern + fat controllers, migration safety, performance smells (uncached computed, `count()` vs `exists()`, pagination strategy), API design. Reads existing `app/Actions/`, `app/Services/`, `app/Http/Requests/`, `app/Data/` for project-specific consistency. Use before any plan-phase touching models/migrations/queries.
- **laravel-reviewer** — Evidence-based code review that wraps the `laravel-code-review` skill with tool access (grep/find/`php artisan`). Runs banned-token sweep on touched paths, performs sibling-canon verification, and **recommends** calling specialist agents (livewire/pest/flux-pro/architect) when stack-specific code is in scope — composes them rather than re-implementing. Output grouped by Blocker / Should-fix / Nice-to-have with `file:line` citations. Use after every implementation commit, before pushing.

See [`docs/agents.md`](docs/agents.md) for the full agent reference.

## Hooks

- **banned-token-leak-guard** — PreToolUse hook on `git commit` that blocks commits with banned tokens (Phase/Sprint/Track/MR/dated refs) in staged code/comments. Honors exception paths (`docs/plans/**`, `docs/superpowers/**`, `CHANGELOG.md`) and per-line override marker `banned-token-ok: <reason>`. Configurable via `hook_enabled.banned_token_leak_guard` and `banned_tokens.*` in plugin config.
- **no-claude-attribution** — PreToolUse hook on `git commit`, `gh pr create`, `glab mr create` that blocks any commit message, PR body, or MR description containing Claude / AI attribution (`Co-Authored-By: Claude`, `🤖 Generated with Claude Code`, `AI-assisted`, etc.). Shows the offending line + sanitized rewrite. Reads from `-m`, `-F`, `--body`, `--body-file`, `--description`, `--description-file`. Configurable via `hook_enabled.no_claude_attribution`.

See [`docs/hooks.md`](docs/hooks.md) for the full hook reference.

## Designed to complement [superpowers](https://github.com/anthropics/claude-plugins-official)

Each skill pairs with its superpowers counterpart:

| superpowers skill | laravel-superpowers skill |
|---|---|
| `superpowers:brainstorming` | `laravel-brainstorming` |
| `superpowers:test-driven-development` | `laravel-tdd` |
| `superpowers:systematic-debugging` | `laravel-debugging` |
| `superpowers:requesting-code-review` | `laravel-code-review` |

Run the superpowers skill first for generic structure; run the laravel-superpowers skill for stack-specific depth.

## V2 in progress

V2 expands the plugin from 1 agent + 4 skills to ~10 agents + 5 skills + 13 hooks + plugin infrastructure (config, slash commands, status). See [ROADMAP.md](docs/ROADMAP.md) for the full breakdown derived from observed real-world Laravel sprint catches.

V2-MVP targets the **highest-ROI tier-1 additions** that would have caught real production bugs in observed test sprints.
