# laravel-superpowers

Laravel-specific workflow skills for [Claude Code](https://claude.ai/code).

## Install

```bash
claude plugin marketplace add github:altraWeb/laravel-superpowers
claude plugin install laravel-superpowers@altraweb-laravel
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
