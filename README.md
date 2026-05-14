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

## Agent

- **laravel-best-practices** — Web research agent for current Laravel best practices (Spatie, Laracasts, Laravel News)

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
