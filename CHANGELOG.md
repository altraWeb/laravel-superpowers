# Changelog

All notable changes to `laravel-superpowers` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2026-05-15 — V2-MVP

**Major release.** Extends V1's "ship working code" baseline (1 agent + 4 skills) into a comprehensive stack-aware toolkit for Laravel 11/12 + Livewire 4 + Flux Pro v2 + Pest 4 projects. Driven by real-world catches from Block 1H + 1E test sprints (4 P0-class bugs that V1 missed).

### Added — Specialist Agents (5)

- **`laravel-livewire-specialist`** ([#1]) — audits Livewire-touching plans/code for fabricated APIs (catches the canonical `$this->hasLoading()` class of bug), `wire:ignore` zone reactivity, Form-Object patterns, Echo morphing race-conditions, lifecycle-hook misuse. Verifies via PHP reflection against `vendor/livewire/livewire/src/Component.php`.
- **`laravel-pest-specialist`** ([#2]) — audits Pest 4 tests for variadic-API misuse (`toContain('foo', 'msg')` gotcha), browser-plugin smells (`wait(N)` abuse), view-context anti-patterns (reserved-name keys), test-location mismatches, `it()`/`arch()`/dataset block correctness. Multi-namespace reflection against `vendor/pestphp/pest/src/`.
- **`laravel-flux-pro-specialist`** ([#3]) — audits Flux Pro v2 Blade components for double-tooltip wrapping (a11y break on `<ui-toolbar>` roving-tabindex), position/align convention drift, `<flux:editor.spacer/>` misplacement, `wire:ignore` reactive descendants, slot-vs-string-prop trade-offs. Cites vendor `file:line` refs from `vendor/livewire/flux-pro/stubs/resources/views/flux/`.
- **`laravel-architect`** ([#4]) — audits Eloquent + architecture decisions. Sibling-canon-aware: reads `app/Actions/`, `app/Services/`, `app/Http/Requests/`, `app/Data/` and recommends consistency with existing project patterns. Catches N+1, surfaces `preventLazyLoading` status, recommends QueryCount-pinning tests, flags Repository anti-pattern + fat controllers.
- **`laravel-reviewer`** ([#5]) — evidence-based code review wrapping the `laravel-code-review` skill with grep/find/`php artisan` tool access. Banned-token sweep default, sibling-canon verification, **composes** specialist agents (recommends them when stack-specific code in scope, never re-implements). Output: Blocker / Should-fix / Nice-to-have with `file:line` citations.

Plus existing `laravel-best-practices` (V1) — kept as the web-research general-Laravel advisor.

### Added — Skill Enhancements (3)

- **`laravel-tdd`** ([#13]) — appended Pest 4 specifics module: variadic-expectation trap (`->because()` modifier), `wait(N)` smell + 5s implicit timeout, `$this` reserved in views, `it()`/`arch()`/dataset decision tree, test-file location convention (Unit/Feature/Architecture/Browser), `actingAs()` placement, `assertAttribute` API availability check.
- **`laravel-code-review`** ([#14]) — appended Livewire 4 sub-checklist (API existence, reactivity modifiers, `#[Computed]` cache modes, `#[Locked]` for non-rehydratable props, `wire:ignore` Alpine bridges, Echo callback patterns, Form Objects, lifecycle hooks) + Flux Pro v2 sub-checklist (tooltip double-wrap, position/align convention, editor.spacer placement, wire:ignore + Flux components, slot vs string, Floating UI auto-flip). Each sub-checklist invokes the corresponding specialist agent for deep audit.
- **`laravel-debugging`** ([#15]) — appended top-10 RED-recipes table covering Pest 4 / Livewire 4 / Flux Pro v2 stolperer (variadic, `$this`, fabricated APIs, `Bus::fake` mock-layer, route mismatch, hasOne/hasMany juggle, FK constraints, Livewire properties, lang keys, browser flake). Plus specialist-dispatch matrix.

### Added — Enforcement Hooks (6)

- **`banned-token-leak-guard`** ([#16]) — PreToolUse on `git commit`. Blocks commits containing Phase/Sprint/Track/MR/dated refs in staged code/comments. Exception paths (`docs/plans/**`, `docs/superpowers/**`, `CHANGELOG.md`), per-line override marker (`banned-token-ok: <reason>`), configurable extras via `banned_tokens.project_extras`.
- **`no-claude-attribution`** ([#17]) — PreToolUse on `git commit`, `gh pr create`, `glab mr create`. Blocks any Claude / AI attribution variant in commit messages or MR bodies. Reads from `-m`, `-F`, `--body`, `--body-file`, `--description`, `--description-file`. Shows offending line + sanitized rewrite suggestion.
- **`teamcity-always`** ([#18]) — PreToolUse on `php artisan test`. Blocks when `--teamcity` missing, shows retry suggestion with flag inserted in correct position. Respects alternate reporters (`--testdox`, `--printer-class`) and config kill-switches.
- **`anti-silent-deferral`** ([#19]) — PreToolUse on `git push`. Scans `docs/plans/*.md` files on the branch for `## Phase N — Deferred Items` sections. Blocks when free-form prose or bullets without `#N` issue refs. Allows explicit `**None — all tasks completed**` markers. Emergency override env var + per-doc skip marker.
- **`visual-companion-default-on`** ([#21]) — PostToolUse on `superpowers:brainstorming`. Injects `additionalContext` reminder that Visual Companion is default-on unless topic is provably text-only (naming votes, semver, config-flips). Configurable denylist + allowlist override.
- **`brainstorm-t1-audit`** ([#20]) — PostToolUse on `superpowers:brainstorming`. Injects `additionalContext` with canonical dispatch prompt template for `laravel-best-practices` agent (Pilot 2.0 Tactic 1 — Phase-Start Agent-Audit). Topic interpolated from skill args.

### Added — Plugin Infrastructure (2)

- **Plugin config foundation** ([#22]) — `config.defaults.yaml` + `config.schema.json` + Python helper (`lib/config.py`) with 5 subcommands: `get`, `validate`, `show`, `init`, `doctor`. Three-layer merge: defaults < user-global (`~/.claude/plugins/altraweb-laravel/laravel-superpowers/config.yaml`) < per-project (`<project>/.laravel-superpowers.yaml`). All hooks read config at fire-time. Fail-open architecture — broken config helper never blocks user operations.
- **`/laravel-superpowers:status` slash command** ([#23]) — read-only status panel surfacing current sprint state (active plan-doc + phase progress), Pilot 2.0 obligations (T1/T3/T4 dispatch evidence; T5/T6 automated via hooks), hook compliance per config, open obligations. Target: ≤2s response time.

### Documentation

- New: `docs/agents.md`, `docs/hooks.md`, `docs/config.md`
- Enhanced: `README.md` with full Skills / Agents / Hooks / Slash Commands sections + Configuration section
- Updated: `docs/ROADMAP.md` — V2-MVP marked complete, V2.1/V2.2/V3 milestones remain
- New: 16 design specs + 16 implementation plans under `docs/superpowers/specs/` + `docs/superpowers/plans/`
- New: 15 specialist-agent smoke-test evidence files under `docs/superpowers/test-evidence/`

### Tests

- **45 shell-test scenarios** covering all 6 hooks (6 + 10 + 9 + 11 + 9 + 5)
- **23 Python unit tests** for the config foundation helper (`tests/test_config.py`)
- **1 shell smoke test** for hook integration pattern (`tests/test_hook_integration.sh`)
- All green at release time

### Notable design decisions documented in PR bodies

- **Hooks cannot invoke agents directly** (#20) — implemented as REMINDER + dispatch prompt template via `additionalContext`. Parent agent does the Task-tool dispatch.
- **Teamcity-always BLOCKS with retry** (#18) — issue asked for auto-append; hook output schema for tool_input modification is not portable. Block-with-suggestion gets 90% of value at 10% of complexity.
- **Visual-companion hook injects reminder, not literal offer** (#21) — skill spec requires offer as "own message" which `additionalContext` can't strictly guarantee. Reminder nudges the agent to offer at Step 2.

### Breaking changes

None. V2.0.0 is fully additive over V1.

### Stack assumptions (unchanged from V1)

Laravel 11/12 + Livewire 4 + Flux Pro v2 + Pest 4 + PHP 8.4+. Older Laravel/Livewire versions can still use the generic skills (`laravel-brainstorming`, `laravel-tdd`, `laravel-code-review`, `laravel-debugging`) but the V2-MVP specialists lean on Livewire 4 / Flux Pro v2 / Pest 4 specifically.

[#1]: https://github.com/altraWeb/laravel-superpowers/issues/1
[#2]: https://github.com/altraWeb/laravel-superpowers/issues/2
[#3]: https://github.com/altraWeb/laravel-superpowers/issues/3
[#4]: https://github.com/altraWeb/laravel-superpowers/issues/4
[#5]: https://github.com/altraWeb/laravel-superpowers/issues/5
[#13]: https://github.com/altraWeb/laravel-superpowers/issues/13
[#14]: https://github.com/altraWeb/laravel-superpowers/issues/14
[#15]: https://github.com/altraWeb/laravel-superpowers/issues/15
[#16]: https://github.com/altraWeb/laravel-superpowers/issues/16
[#17]: https://github.com/altraWeb/laravel-superpowers/issues/17
[#18]: https://github.com/altraWeb/laravel-superpowers/issues/18
[#19]: https://github.com/altraWeb/laravel-superpowers/issues/19
[#20]: https://github.com/altraWeb/laravel-superpowers/issues/20
[#21]: https://github.com/altraWeb/laravel-superpowers/issues/21
[#22]: https://github.com/altraWeb/laravel-superpowers/issues/22
[#23]: https://github.com/altraWeb/laravel-superpowers/issues/23

---

## [1.0.0] — 2026-05-13 — Initial release

- 1 agent: `laravel-best-practices`
- 4 skills: `laravel-brainstorming`, `laravel-tdd`, `laravel-debugging`, `laravel-code-review`
- Marketplace registration: `altraweb-laravel` on GitHub via `altraWeb/laravel-superpowers`
- Plugin discoverable via `claude plugin marketplace add altraWeb/laravel-superpowers`
