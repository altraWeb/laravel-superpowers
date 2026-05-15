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
- **teamcity-always** — PreToolUse hook on `php artisan test` that blocks invocations missing the `--teamcity` flag (per project canon — IDE integration like PhpStorm/VSCode needs the TeamCity reporter for parsable per-test events). Shows a retry suggestion with `--teamcity` inserted in the right position. Skips when `--teamcity` already present or when an alternate reporter (`--testdox`, `--printer-class`) is explicit. Configurable via `hook_enabled.teamcity_always` and the top-level `teamcity_always` kill switch.
- **anti-silent-deferral** — PreToolUse hook on `git push` that scans branch's `docs/plans/*.md` files for uncaptured `## Phase N — Deferred Items` sections. Blocks push when any section has free-form prose or bullets without filed-issue refs. Allows explicit `**None — all tasks completed**` markers and bullets with `#N` issue links. Emergency override via `LARAVEL_SUPERPOWERS_ALLOW_UNCAPTURED_DEFERRAL=1`. Per-doc skip marker `<!-- anti-silent-deferral-skip: <reason> -->`. Configurable via `hook_enabled.anti_silent_deferral`.
- **visual-companion-default-on** — PostToolUse hook on `superpowers:brainstorming` skill invocation. Injects an `additionalContext` reminder that the Visual Companion is default-on unless the topic is provably text-only (naming votes, semver bumps, config-flips). Configurable denylist (`visual_companion_default.text_only_patterns`) and allowlist override (`visual_companion_default.always_offer_patterns`). Two disable paths: `hook_enabled.visual_companion_default_on: false` (hook-only) or `visual_companion_default: off` top-level (operator-wide opt-out).
- **brainstorm-t1-audit** — PostToolUse hook on `superpowers:brainstorming` skill invocation. Injects an `additionalContext` reminder + canonical dispatch prompt template directing the parent agent to dispatch `laravel-best-practices` Agent as a parallel background task (Pilot 2.0 Tactic 1 — Phase-Start Agent-Audit). Topic auto-interpolated from skill args; falls back to "detect from conversation context". Configurable via `hook_enabled.brainstorm_t1_audit` and `audit_aggressiveness`.

See [`docs/hooks.md`](docs/hooks.md) for the full hook reference.

## Slash Commands

- **`/laravel-superpowers:status`** — Read-only status panel. Surfaces current sprint state (active plan-doc + phase progress), Pilot 2.0 contract obligations (T1/T3/T4 status + T5/T6 hook-automated), hook compliance per config, open obligations (deferred items, pending audits). ≤2s response time, no state mutation.

## Designed to complement [superpowers](https://github.com/anthropics/claude-plugins-official)

Each skill pairs with its superpowers counterpart:

| superpowers skill | laravel-superpowers skill |
|---|---|
| `superpowers:brainstorming` | `laravel-brainstorming` |
| `superpowers:test-driven-development` | `laravel-tdd` |
| `superpowers:systematic-debugging` | `laravel-debugging` |
| `superpowers:requesting-code-review` | `laravel-code-review` |

Run the superpowers skill first for generic structure; run the laravel-superpowers skill for stack-specific depth.

## Versions

- **v2.0.0 (2026-05-15) — V2-MVP** *(current)* — 6 specialist agents + 6 enforcement hooks + 3 stack-enhanced skills + plugin config foundation + status slash command. Derived from Block 1H + 1E test-sprint catches; ships the bug-catchers V1 was missing.
- **v1.0.0 (2026-05-13) — Initial** — 1 agent (`laravel-best-practices`) + 4 skills (`laravel-brainstorming`, `laravel-tdd`, `laravel-debugging`, `laravel-code-review`).

See [CHANGELOG.md](CHANGELOG.md) for the full release history and [ROADMAP.md](docs/ROADMAP.md) for upcoming V2.1 / V2.2 / V3 milestones.
