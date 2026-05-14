# Plugin Agents — Reference

`laravel-superpowers` ships specialized agents you invoke for Laravel-specific tasks. Each agent has a focused scope and runs in its own context.

## Agents

### `laravel-best-practices`

**Use when:** asking how something should be done in current-Laravel terms — *"how should I implement X?"*, *"is approach Y still recommended in Laravel 12?"*, *"is there a Spatie package for Z?"*.

**Approach:** searches official Laravel docs + core-team blogs (Tim MacDonald, Taylor Otwell) + trusted community (Spatie, Laracasts, Laravel News), synthesizes a 2025/2026-current recommendation with code example, pitfalls, and version notes.

**Tools:** Read, Bash, WebSearch, WebFetch.

---

### `laravel-livewire-specialist`

**Use when:** auditing a plan-phase or code snippet that touches Livewire 4 components, blade templates with `wire:*` directives, or Echo/broadcasting integration. Particularly valuable before implementation when a plan mentions a `$this->...()` method — the agent verifies API existence via reflection against the vendor source, catching fabricated methods (like the `$this->hasLoading()` case from Block 1H Phase 5) before they ship.

**The 5 audit checks:**

1. **API verification** — PHP reflection on `Livewire\Component` (catches fabricated methods like `$this->hasLoading()`)
2. **`wire:ignore` zone scan** — finds descendants with `wire:*` directives inside ignored subtrees (silent reactivity failure)
3. **Form-Object pattern recommendation** — picks between `Livewire\Form` / property+`rules()` / Spatie LaravelData based on use-case shape
4. **Echo / broadcasting morphing-race detection** — flags callbacks that mutate DOM directly before Livewire's next morph
5. **Lifecycle hook usage** — verifies hook names and flags common mistakes (`updated()` without filtering, `mount()` doing work that belongs in `hydrate()`, etc.)

**Output:** structured markdown audit report with severity classification (critical / important / minor) and concrete suggestions per finding.

**Tools:** Read, Bash, WebFetch, WebSearch.

**Required:** PHP 8+ in PATH (for reflection invocation). Falls back to docs-only verification via WebFetch if `vendor/livewire/` is missing.

**Smoke-test evidence:** See [`superpowers/test-evidence/2026-05-15-livewire-specialist-smoke-*.md`](superpowers/test-evidence/) for captured outputs covering the canonical bug, a clean phase, and a non-Livewire fail-clean case.

---

### `laravel-pest-specialist`

**Use when:** about to write or edit a Pest 4 test, especially when the test will use multi-arg expectations like `toContain`, browser plugin APIs, view rendering, or `arch()` structural assertions. Catches Pest 4 stolperer that would either RED on first run (variadic misuse) or silently produce wrong-positives (`->wait(1)` before assertions that already have implicit timeout, reserved-name view keys, runtime calls inside `arch()` blocks).

**The 5 audit checks:**

1. **Variadic-API Verification** — reflects on `Pest\Expectation` to flag misuse like `toContain($needle, $message)` where Pest treats both args as needles. Suggests `->because('msg')` modifier.
2. **Browser-Plugin Smell Scan** — flags `->wait(N)` before assertions (5s implicit timeout already), recommends `data-testid` selectors over text/class.
3. **View-Context Anti-Patterns** — catches reserved-name keys in `view()->with([...])` (`'this'`, `'loop'`, `'errors'`, etc.).
4. **Test-Location Convention** — flags content/location mismatches (HTTP in Unit, DB without `LazilyRefreshDatabase`, browser tests outside `tests/Browser/`).
5. **it()/arch()/dataset Block Patterns** — flags runtime calls inside `arch()` blocks (structural-only), suggests `dataset()` for drift-guards.

**Output:** structured markdown audit report with severity classification (critical / important / minor) and concrete suggestions per finding.

**Tools:** Read, Bash, WebFetch, WebSearch.

**Required:** PHP 8+ in PATH. Falls back to docs-only verification if `vendor/pestphp/` is missing.

**Smoke-test evidence:** See [`superpowers/test-evidence/2026-05-15-pest-specialist-smoke-*.md`](superpowers/test-evidence/) for captured outputs covering the variadic-misuse catch, a clean expectation chain, and a non-Pest fail-clean case.

---

## Forthcoming (V2-MVP)

- `laravel-flux-pro-specialist` ([#3](https://github.com/altraWeb/laravel-superpowers/issues/3)) — Flux Pro v2 vendor source + slot composition
- `laravel-architect` ([#4](https://github.com/altraWeb/laravel-superpowers/issues/4)) — Eloquent + architecture decisions (N+1, eager-loading, Actions vs Services)
- `laravel-reviewer` ([#5](https://github.com/altraWeb/laravel-superpowers/issues/5)) — wraps `laravel-code-review` skill with grep/find/MCP integration

See [ROADMAP.md](ROADMAP.md) for the full V2 plan and the broader V2.1/V2.2/V3 roadmap.
