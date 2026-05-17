# laravel-livewire-superpowers

Laravel + **Livewire 4** + **Flux Pro v2** + **Pest 4** specialist toolkit for [Claude Code](https://claude.ai/code) — designed to complement the [superpowers](https://github.com/anthropics/claude-plugins-official) base plugin with deep stack-specific expertise.

> **Stack scope:** This plugin targets the Livewire 4 + Flux Pro v2 stack. For the Vue 3 + Inertia v2 variant, see the planned sibling plugin [`laravel-vue-superpowers`](https://github.com/altraWeb/laravel-vue-superpowers) (not yet released).

📍 **[Roadmap](docs/ROADMAP.md)** — see what's planned + tracked GitHub issues organized by version
📊 **[Milestones](https://github.com/altraWeb/laravel-livewire-superpowers/milestones)** — V3 alpha / V3 stable progress
📋 **[Project board](https://github.com/altraWeb/laravel-livewire-superpowers/projects)** — live status across all issues

## Install

```bash
claude /plugin marketplace add altraWeb/laravel-marketplace
claude /plugin install laravel-livewire-superpowers@altraweb-laravel
```

The marketplace is hosted at [`altraWeb/laravel-marketplace`](https://github.com/altraWeb/laravel-marketplace) — a neutral host repo that will also list the future `laravel-vue-superpowers` sibling.

## Migrating from v2 (laravel-superpowers)

```bash
claude /plugin uninstall laravel-superpowers
claude /plugin marketplace remove altraweb-laravel
claude /plugin marketplace add altraWeb/laravel-marketplace
claude /plugin install laravel-livewire-superpowers@altraweb-laravel
```

See [`UPGRADING.md`](UPGRADING.md) for the full migration guide.

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

## Skills (7)

- **laravel-brainstorming** — Architecture brainstorming for Laravel: layers, Eloquent relationships, Events, Policies, queuing decisions
- **laravel-tdd** — TDD workflow with Pest 4: factories, HTTP testing, facade faking, Feature vs Unit
- **laravel-debugging** — Debugging with Laravel-specific tools: Telescope, query logging, queue introspection
- **laravel-code-review** — Code review checklist: N+1, mass assignment, authorization, validation, security
- **laravel-a11y** *(Phase B+)* — Accessibility audit for Livewire + Flux Pro components
- **laravel-mr-body-writer** *(Phase B+)* — MR/PR description writer for Laravel projects
- **laravel-perf-auditor** *(Phase B+)* — Performance audit: N+1, eager loading, cache strategies

## Agents (10)

- **laravel-best-practices** — Web research agent for current Laravel best practices (Spatie, Laracasts, Laravel News). Use when asking *"how should I implement X?"* or *"is my current approach still best practice?"*.
- **laravel-livewire-specialist** — Audits Livewire-touching code/plans for fabricated APIs, `wire:ignore` zones, Form-Object patterns, Echo/broadcasting race conditions, and lifecycle-hook misuse. Verifies via PHP reflection against the actual Livewire vendor source — ground truth, not docs. Use before any Livewire-touching implementation phase.
- **laravel-pest-specialist** — Audits Pest 4 tests for variadic-API misuse, browser-plugin smells, view-context anti-patterns, test-location mismatches, and `it()`/`arch()`/dataset block correctness. Verifies via PHP reflection against the actual Pest vendor source. Use before any test write/edit.
- **laravel-flux-pro-specialist** — Audits Flux Pro v2 Blade components for double-tooltip wrapping, position/align convention drift, `<flux:editor.spacer/>` misplacement, `wire:ignore`-zone reactive-descendant issues, and slot-vs-string-prop trade-offs. Reads the Flux Pro vendor stubs as ground truth, cites file:line in findings. Use before any `<flux:*>` write/edit.
- **laravel-architect** — Audits Eloquent + architecture decisions: N+1 detection, sibling-canon-aware pattern recommendations, migration safety, performance smells, API design. Use before any plan-phase touching models/migrations/queries.
- **laravel-reviewer** — Evidence-based code review wrapping the `laravel-code-review` skill with tool access (grep/find/`php artisan`). Runs banned-token sweep, sibling-canon verification, and recommends specialist agents when stack-specific code is in scope.
- **laravel-echo-reverb-specialist** — Broadcasting / realtime decision support. Scans channels, notifications, Echo callbacks to surface reuse-vs-new-channel decisions. Closes [#7](https://github.com/altraWeb/laravel-livewire-superpowers/issues/7).
- **spatie-permission-auditor** — Gate-coverage + dead-permission audit. Cross-references seeded permissions vs actual `@can()` / `can()` / Policy usage. Closes [#9](https://github.com/altraWeb/laravel-livewire-superpowers/issues/9).
- **laravel-package-evaluator** — Build-vs-buy decision support. Searches Packagist + GitHub for 2-5 candidates, builds trade-off matrix. Closes [#12](https://github.com/altraWeb/laravel-livewire-superpowers/issues/12).
- **laravel-pilot-orchestrator** *(Phase D+)* — Pilot 2.0 contract orchestrator agent

See [`docs/agents.md`](docs/agents.md) for the full agent reference.

## Hooks (9 shipped — 13 planned for full V3)

- **banned-token-leak-guard** — PreToolUse hook on `git commit` that blocks commits with banned tokens (Phase/Sprint/Track/MR/dated refs) in staged code/comments.
- **no-claude-attribution** — PreToolUse hook on `git commit`, `gh pr create`, `glab mr create` that blocks any Claude / AI attribution.
- **teamcity-always** — PreToolUse hook on `php artisan test` that blocks invocations missing `--teamcity`.
- **anti-silent-deferral** — PreToolUse hook on `git push` that scans plan docs for uncaptured deferred items.
- **visual-companion-default-on** — PostToolUse hook on brainstorming skill that injects a Visual Companion reminder.
- **brainstorm-t1-audit** — PostToolUse hook on brainstorming skill that dispatches `laravel-best-practices` audit (Pilot 2.0 T1).
- **sprint-state-context-injection** — SessionStart hook that injects active sprint state (branch, plan-doc, phase, last commit) into session context.
- **stale-branch-sweep** — SessionStart hook that lists local branches whose upstream is gone (post-merge cleanup suggestion).
- **master-roadmap-drift-detector** — PostToolUse hook on `git commit` touching plan-docs that warns when master-roadmap entry is out of sync.
- **vendor-source-preflight** *(Phase C+)* — Vendor source verification preflight
- **lang-key-existence-preflight** *(Phase C+)* — Lang key existence verification
- **pilot-2-contract-enforcer** *(Phase C+)* — Full Pilot 2.0 contract enforcement (T1-T6)
- *(13th hook planned for Phase C+)*

See [`docs/hooks.md`](docs/hooks.md) for the full hook reference.

## Slash Commands (3)

- **`/laravel-livewire-superpowers:status`** — Read-only status panel. Surfaces current sprint state, Pilot 2.0 contract obligations, hook compliance, open obligations. ≤2s response, no state mutation.
- **`/laravel-livewire-superpowers:audit-phase`** *(Phase E+)* — Phase audit command
- **`/laravel-livewire-superpowers:retro`** *(Phase E+)* — Retrospective command

## Designed to complement [superpowers](https://github.com/anthropics/claude-plugins-official)

Each skill pairs with its superpowers counterpart:

| superpowers skill | laravel-livewire-superpowers skill |
|---|---|
| `superpowers:brainstorming` | `laravel-livewire-superpowers:laravel-brainstorming` |
| `superpowers:test-driven-development` | `laravel-livewire-superpowers:laravel-tdd` |
| `superpowers:systematic-debugging` | `laravel-livewire-superpowers:laravel-debugging` |
| `superpowers:requesting-code-review` | `laravel-livewire-superpowers:laravel-code-review` |

Run the superpowers skill first for generic structure; run the laravel-livewire-superpowers skill for stack-specific depth.

## Sibling plugins

| Plugin | Stack | Status |
|---|---|---|
| `laravel-livewire-superpowers` | Laravel + Livewire 4 + Flux Pro v2 + Pest 4 | Active (this repo) |
| [`laravel-vue-superpowers`](https://github.com/altraWeb/laravel-vue-superpowers) | Laravel + Vue 3 (Composition API) + Inertia v2 + Pest 4 | Planned |

## Versions

- **v3.0.0-alpha.2 (2026-05-17) — V3 Megarelease Phase B** *(current)* — Three context-aware hooks that surface daily sprint state without operator action: `sprint-state-context-injection`, `stale-branch-sweep`, `master-roadmap-drift-detector`. Now 9 hooks shipped.
- **v3.0.0-alpha.1 (2026-05-17) — V3 Megarelease Phase A** — Plugin renamed to `laravel-livewire-superpowers`, marketplace moved to neutral host `altraWeb/laravel-marketplace`, all branding updated. Foundation phase that unblocks Phases B-G.
- **v2.0.2 (2026-05-17) — Deprecation notice** — No code changes. Deprecation notice announcing V3 + rename.
- **v2.0.1 (2026-05-15) — V2-MVP self-audit hotfix** — Quote-bypass, date false-positives, composer-test, command-position filter.
- **v2.0.0 (2026-05-15) — V2-MVP** — 6 specialist agents + 6 enforcement hooks + 3 stack-enhanced skills + plugin config foundation + status slash command. (V3 Phase C adds 3 more: echo-reverb / spatie-permission / package-evaluator → 9 total)
- **v1.0.0 (2026-05-13) — Initial** — 1 agent + 4 skills.

See [CHANGELOG.md](CHANGELOG.md) for the full release history and [ROADMAP.md](docs/ROADMAP.md) for upcoming V3 milestones.
