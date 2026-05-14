# laravel-superpowers Roadmap

> **Plugin extends [superpowers](https://github.com/anthropics/claude-plugins-official) with Laravel/Livewire/Flux/Pest expertise.**
>
> Status snapshots derived from labeled GitHub issues — see [Project board](https://github.com/altraWeb/laravel-superpowers/projects) for live status, [Milestones](https://github.com/altraWeb/laravel-superpowers/milestones) for version grouping.

This roadmap captures planned additions evidence-based from observed real-world sprint catches. Every entry links to a tracked GitHub issue with motivation, scope, and acceptance criteria.

## How V2 came to be

V1 of `laravel-superpowers` shipped 1 agent (`laravel-best-practices`) + 4 skills (`laravel-brainstorming`, `laravel-tdd`, `laravel-debugging`, `laravel-code-review`). Adequate for "ship working code".

V2 was driven by an observed gap: when operators run the plugin against real multi-phase Laravel sprints (Livewire 4 + Flux Pro v2 + Pest 4 stack), V1 catches generic anti-patterns but misses stack-specific stolperer that ship as production bugs. A test sprint (Block 1H Editor AI-Toolbar, 2026-05-14, 22 commits) running V1 + a manual Pilot 2.0 workflow contract surfaced **4 P0 bugs at audit-time** that V1 alone would have missed:

1. **Fabricated `$this->hasLoading()` Livewire API** — would have shipped a `BadMethodCallException` on first dropdown click in production
2. **`Bus::fake()` wrong mock layer** for synchronous `AiAgentRunner::*` static calls — test would have fired real Anthropic with blanked phpunit key → 401 → RED
3. **`view()->with(['this' => new class{}])`** anti-pattern — `$this` is reserved by PHP/Blade
4. **Redundant `<flux:tooltip>` outer wrapper** — would have broken `<ui-toolbar>` roving-tabindex (silent a11y regression)

V2 builds the agents + skills + hooks that catch these classes of bugs **by construction**, not by discipline.

---

## V2-MVP — Tier-1 (highest-ROI, observed-sprint catches)

**Goal**: ship the bug-catchers that the Block 1H + 1E sprints needed but didn't have. 1-week build.

### New agents

- [ ] **[#1](https://github.com/altraWeb/laravel-superpowers/issues/1) `laravel-livewire-specialist`** — deep Livewire 4 API + lifecycle knowledge. API-existence verification via reflection (catches fabricated `$this->hasLoading()` class of bug).
- [ ] **[#2](https://github.com/altraWeb/laravel-superpowers/issues/2) `laravel-pest-specialist`** — Pest 4 API depth + browser-plugin recipes. Catches `toContain` variadic, `wait(N)` smell, `$this`-mock-in-view anti-pattern.
- [ ] **[#3](https://github.com/altraWeb/laravel-superpowers/issues/3) `laravel-flux-pro-specialist`** — Flux Pro v2 vendor source traversal + slot composition. Catches redundant tooltip wrappers, position+align convention drift.
- [ ] **[#4](https://github.com/altraWeb/laravel-superpowers/issues/4) `laravel-architect`** — Eloquent + architecture decisions (N+1, eager-loading, Actions vs Services, migration safety).
- [ ] **[#5](https://github.com/altraWeb/laravel-superpowers/issues/5) `laravel-reviewer`** — wraps `laravel-code-review` skill with grep/find/MCP tool integration.

### Skill enhancements

- [ ] **[#13](https://github.com/altraWeb/laravel-superpowers/issues/13) Enhance `laravel-tdd`** — Pest 4 specifics (because modifier, datasets, it vs arch, assertAttribute)
- [ ] **[#14](https://github.com/altraWeb/laravel-superpowers/issues/14) Enhance `laravel-code-review`** — Livewire 4 + Flux Pro v2 sub-checklists
- [ ] **[#15](https://github.com/altraWeb/laravel-superpowers/issues/15) Enhance `laravel-debugging`** — top-10 Pest 4 RED-debugging recipes

### Hooks

- [ ] **[#16](https://github.com/altraWeb/laravel-superpowers/issues/16) Banned-token-leak guard** — PreToolUse on git commit
- [ ] **[#17](https://github.com/altraWeb/laravel-superpowers/issues/17) No-Claude-attribution** — PreToolUse on git commit + MR create
- [ ] **[#18](https://github.com/altraWeb/laravel-superpowers/issues/18) `--teamcity` always** — PreToolUse on `php artisan test`
- [ ] **[#19](https://github.com/altraWeb/laravel-superpowers/issues/19) Anti-silent-deferral pre-push** — PreToolUse on git push
- [ ] **[#20](https://github.com/altraWeb/laravel-superpowers/issues/20) Brainstorm-time T1 audit auto-dispatch** — PostToolUse on `superpowers:brainstorming`
- [ ] **[#21](https://github.com/altraWeb/laravel-superpowers/issues/21) Visual-companion-default-on** — PostToolUse brainstorming Step 2

### Plugin infrastructure

- [ ] **[#22](https://github.com/altraWeb/laravel-superpowers/issues/22) Plugin config foundation** — config.yaml with sane defaults + project-override
- [ ] **[#23](https://github.com/altraWeb/laravel-superpowers/issues/23) Slash command `/laravel-superpowers:status`** — current sprint + Pilot 2.0 obligations

**V2-MVP total**: 16 issues

---

## V2.1 — Tier-2 (polish + automation)

**Goal**: round out the V2-MVP with the next-most-valuable additions. 3-day sprint after V2-MVP ships.

### Agents + skills

- [ ] **[#6](https://github.com/altraWeb/laravel-superpowers/issues/6) `laravel-a11y-specialist` skill** — WCAG 2.2 + ARIA + reduced-motion patterns
- [ ] **[#7](https://github.com/altraWeb/laravel-superpowers/issues/7) `laravel-echo-reverb-specialist` agent** — broadcasting + realtime decision support
- [ ] **[#8](https://github.com/altraWeb/laravel-superpowers/issues/8) `laravel-mr-body-writer` skill** — canonical MR body from sprint state

### Hooks + slash commands

- [ ] **[#24](https://github.com/altraWeb/laravel-superpowers/issues/24) Sprint-state context-injection** — SessionStart auto-resume
- [ ] **[#25](https://github.com/altraWeb/laravel-superpowers/issues/25) Master-roadmap drift detector** — PostToolUse on docs/plans commits
- [ ] **[#26](https://github.com/altraWeb/laravel-superpowers/issues/26) Stale-branch sweep** — SessionStart cleanup
- [ ] **[#27](https://github.com/altraWeb/laravel-superpowers/issues/27) Slash commands `/audit-phase N` + `/retro`** — expand command suite

**V2.1 total**: 7 issues

---

## V2.2 — Tier-3 (future-sprint utility)

**Goal**: extensions that activate when the first project hits the relevant use case.

### Agents + skills

- [ ] **[#9](https://github.com/altraWeb/laravel-superpowers/issues/9) `spatie-permission-auditor` agent** — gate coverage + dead-permission detection
- [ ] **[#11](https://github.com/altraWeb/laravel-superpowers/issues/11) `laravel-perf-auditor` skill** — preventLazyLoading + query-count + cache patterns
- [ ] **[#12](https://github.com/altraWeb/laravel-superpowers/issues/12) `laravel-package-evaluator` agent** — build-vs-buy decision support

### Hooks

- [ ] **[#28](https://github.com/altraWeb/laravel-superpowers/issues/28) Vendor-source pre-flight** — PreToolUse on Flux/Livewire blade edits
- [ ] **[#29](https://github.com/altraWeb/laravel-superpowers/issues/29) Lang-key existence pre-flight** — PreToolUse on blade edits with `__()` calls

**V2.2 total**: 5 issues

---

## V3 — Meta layer

**Goal**: workflow enforcement at the orchestrator level. Requires V2-MVP + V2.1 in production first to inform meta-orchestrator design.

### Meta agents + hooks

- [ ] **[#10](https://github.com/altraWeb/laravel-superpowers/issues/10) `laravel-pilot-orchestrator` agent** — Pilot 2.0 contract enforcer (on-demand)
- [ ] **[#30](https://github.com/altraWeb/laravel-superpowers/issues/30) Pilot 2.0 contract enforcer hook** — meta hook reading orchestrator transcript (continuous)

**V3 total**: 2 issues

---

## Contributing

Issues with the `good first issue` label (none yet — coming as V2-MVP design crystallizes) are good entry points.

For new proposals, please use the issue templates:
- [Agent template](.github/ISSUE_TEMPLATE/agent.yml)
- [Skill template](.github/ISSUE_TEMPLATE/skill.yml)
- [Hook / infra template](.github/ISSUE_TEMPLATE/hook.yml)

Each template ensures the proposal includes: **observed-sprint motivation** + **concrete scope** + **measurable acceptance criteria** + **tier** + **related references**.

---

## Stack assumptions

The plugin is opinionated about the Laravel ecosystem stack it targets:

- **Laravel 13** (current at plugin creation)
- **Livewire 4** + **FluxUI Pro v2** (the canonical full-stack Livewire combination)
- **Pest 4** (with browser plugin — Browser tests are first-class)
- **PHP 8.5** (using typed class constants, readonly properties, asymmetric visibility where appropriate)
- **Spatie Permission 7** for roles + permissions
- **Laravel Reverb v1** + **Echo v2** for real-time broadcasting

Projects on older Laravel + Livewire versions can still benefit from the generic skills (`laravel-brainstorming`, `laravel-tdd`, `laravel-code-review`, `laravel-debugging`) but the V2-MVP agents lean on Livewire 4 / Flux Pro v2 / Pest 4 API knowledge specifically.

---

*Last updated: 2026-05-14 — roadmap initialized with 30 V2 issues across 4 milestones, derived from Block 1H + 1E sprint retros.*
