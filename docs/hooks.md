# Plugin Hooks — Reference

`laravel-superpowers` ships Claude Code hooks that enforce conventions automatically at the right moment in your workflow. Hooks are deterministic — they fire on Claude Code events (`PreToolUse`, `PostToolUse`, `SessionStart`, etc.) and can block, warn, or inject context.

All hooks read from the plugin config foundation ([`docs/config.md`](config.md)) and can be enabled/disabled per-project via the `hook_enabled.<hook_name>` flag.

---

## Hooks

### `banned-token-leak-guard`

**Event:** `PreToolUse` on `Bash` (filters internally to `git commit` invocations).

**What it does:** scans staged files at commit time for banned tokens (Phase/Sprint/Track/MR-numbers/dated refs) in code and comments. Blocks the commit if any are found.

**Why:** code comments must not reference Phase/Sprint state — they rot fast and look unprofessional in shipped code. Caught Block 1H Phase 6 leaks at the last step before push; this hook eliminates the need for end-of-sprint hard-gate sweeps.

**Default banned-token patterns:**

| Pattern | Example match |
|---|---|
| `Phase [0-9]+` | `Phase 3` |
| `Slice [0-9]+` | `Slice 2` |
| `Track [0-9]+` | `Track 1` |
| `Sprint [0-9]+` | `Sprint 12` |
| `MR !?[0-9]+` | `MR !345` |
| `Pilot 2\.0` | `Pilot 2.0` |
| `\b20[0-9]{2}-[0-9]{2}-[0-9]{2}\b` | `2026-05-14` |

**Default exception paths (not scanned):**

- `docs/plans/**`
- `docs/superpowers/**`
- `CHANGELOG.md`

**Files scanned:** `.php`, `.blade.php`, `.js`, `.ts`, `.css`, `.md` (in non-exception paths).

**Per-line override marker:**

Add `banned-token-ok: <reason>` to a line to allow it past the sweep:

```php
// Valid domain states: Phase 1, Phase 2, Phase 3 — banned-token-ok: domain term, not sprint state
const STATES = ['draft', 'review', 'published'];
```

The marker is required to include a reason after the colon (operator convention — the hook only checks for the marker's presence).

**Configuration:**

In `~/.claude/plugins/altraweb-laravel/laravel-superpowers/config.yaml` (user) or `./.laravel-superpowers.yaml` (per-project):

```yaml
hook_enabled:
  banned_token_leak_guard: true      # set to false to disable

banned_tokens:
  project_extras:                    # additional patterns to ban
    - "AcmeCorp"
    - "INT-[0-9]+"
  exception_paths:                   # extend the default exception list
    - "docs/plans/**"
    - "docs/superpowers/**"
    - "CHANGELOG.md"
    - "docs/adr/**"                  # add project-specific exception
```

**Failure mode:** if Python helper crashes or anything goes sideways, the hook **fails open** — exits 0 and allows the commit. Banned-token enforcement is best-effort, never blocks legitimate commits due to plugin internals failing.

**Test evidence:** the hook ships with `tests/test_banned_token_hook.sh` — 6 scenarios:
1. Block on `Phase 4` in PHP docblock (Block 1H regression case) ✅
2. Allow clean commit (no banned tokens) ✅
3. Allow override-marker line ✅
4. Passthrough on non-commit Bash calls (e.g. `git status`) ✅
5. Allow Phase ref in `docs/plans/` exception path ✅
6. Block dated audit ref in Blade comment ✅

Run: `bash tests/test_banned_token_hook.sh` from repo root.

---

## Forthcoming (V2-MVP)

- `no-claude-attribution` ([#17](https://github.com/altraWeb/laravel-superpowers/issues/17)) — PreToolUse hook blocking commit messages with `Co-Authored-By: Claude` or similar AI attribution
- `teamcity-always` ([#18](https://github.com/altraWeb/laravel-superpowers/issues/18)) — PreToolUse hook injecting `--teamcity` into `php artisan test` for parsable output
- `anti-silent-deferral` ([#19](https://github.com/altraWeb/laravel-superpowers/issues/19)) — PreToolUse hook on `git push` that scans plan-docs for unresolved "Deferred Items"
- `brainstorm-t1-audit` ([#20](https://github.com/altraWeb/laravel-superpowers/issues/20)) — PostToolUse hook on `superpowers:brainstorming` activation that auto-dispatches the specialist agents (#1-#5)
- `visual-companion-default-on` ([#21](https://github.com/altraWeb/laravel-superpowers/issues/21)) — PostToolUse hook setting the brainstorming visual-companion default per config

See [ROADMAP.md](ROADMAP.md) for the full V2 plan and the broader V2.1/V2.2/V3 roadmap.
