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

### `no-claude-attribution`

**Event:** `PreToolUse` on `Bash` (filters internally to `git commit`, `gh pr create`, `gh pr edit`, `glab mr create`, `glab mr update`).

**What it does:** intercepts commit-message / PR-body / MR-description input and blocks if Claude / AI attribution is detected. Reads message content from inline flags (`-m`, `--body`, `--description`) and file flags (`-F`, `--body-file`, `--description-file`).

**Why:** operator's project canon — ZERO Claude attribution in commit messages, PR titles, MR bodies. Real-session evidence: 9 of 19 commits on the `spec/22-config-foundation` branch had Claude attribution before manual cleanup via `git filter-branch`. Subagent-dispatched commits inherited the default Bash-tool template behavior. This hook makes the rule **discipline-free** — even a subagent with the default template trying to add `Co-Authored-By: Claude` gets blocked before the commit lands.

**Default attribution patterns:**

| Pattern | Example match |
|---|---|
| `Co-Authored-By:.*Claude` | `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` |
| `Co-Authored-By:.*[Aa]nthropic` | `Co-Authored-By: claude@anthropic.com` |
| `🤖.*Claude Code` | `🤖 Generated with [Claude Code]` |
| `Generated with.*Claude` | `Generated with Claude` |
| `\bAI-assisted\b` | `AI-assisted refactor` |
| `\bAI-generated\b` | `AI-generated commit` |
| `noreply@anthropic\.com` | the literal email |

**Diagnostic on block:** offending line(s) + sanitized rewrite suggestion (the original message with attribution lines removed). Operator can copy-paste the sanitized version.

**Configuration:**

```yaml
hook_enabled:
  no_claude_attribution: true        # set to false to disable
```

**Failure mode:** fail-open — never blocks a legitimate commit due to plugin internals failing.

**Known limitation:** editor-mode `git commit` (no `-m`, no `-F`) cannot be intercepted from a PreToolUse Bash hook (the commit-message edit happens AFTER the Bash invocation returns). Editor-mode commits emit a warning to stderr but pass through; rely on `laravel-reviewer` agent or post-commit hooks to catch the rare editor-mode case.

**Test evidence:** ships with `tests/test_no_claude_attribution_hook.sh` — 10 scenarios:
1. Block on `Co-Authored-By: Claude` trailer ✅
2. Block on `🤖 Generated with Claude Code` banner ✅
3. Block on `AI-assisted` phrase ✅
4. Block on `git commit -F file` with attribution in file ✅
5. Block on `gh pr create --body` with attribution ✅
6. Block on `glab mr create --description-file` with attribution in file ✅
7. Allow clean commit ✅
8. Passthrough on `git status` ✅
9. Editor-mode `git commit` (passthrough with stderr warning) ✅
10. Allow clean `gh pr create` ✅

Run: `bash tests/test_no_claude_attribution_hook.sh` from repo root.

---

### `teamcity-always`

**Event:** `PreToolUse` on `Bash` (filters internally to `php artisan test`, `php artisan test:parallel`, `php artisan test:compact`).

**What it does:** blocks the call if `--teamcity` is missing, shows a retry suggestion with the flag inserted in the right position. Skips silently when `--teamcity` already present or when an alternate reporter (`--testdox`, `--printer-class`, `--printer=`) is explicit.

**Why:** project canon (CLAUDE.md PersonalGuidelines): always use `--teamcity` for IDE-friendly per-test event output. PhpStorm/VSCode test runners need the TeamCity reporter for parsable results. Without it, IDE integration falls back to plain-stdout parsing and loses fidelity.

**Skip conditions:**

- `--teamcity` already in the command
- Alternative reporter explicit (`--testdox`, `--printer-class=...`, `--printer=...`)
- `hook_enabled.teamcity_always: false` in config
- Top-level `teamcity_always: false` in config (semantic difference: "operator never wants this enforced" vs "disable just the hook")

**Spec deviation from issue:** issue #18 asked for "auto-append". Implementation **BLOCKS with retry suggestion** instead — auto-modifying tool_input from a PreToolUse hook is not a portable Claude Code feature. 90% of the value (operator always uses `--teamcity`) at 10% of the complexity. Operator retypes once, then the muscle memory kicks in.

**Configuration:**

```yaml
hook_enabled:
  teamcity_always: true              # set to false to disable just the hook

teamcity_always: true                # top-level project-canon flag (false = never enforce)
```

**Test evidence:** ships with `tests/test_teamcity_always_hook.sh` — 9 scenarios:
1. Block plain `php artisan test` ✅
2. Block `php artisan test --filter=X` ✅
3. Block `php artisan test:parallel` ✅
4. Allow `php artisan test --teamcity` (already present) ✅
5. Allow `php artisan test --testdox` (alt reporter) ✅
6. Passthrough `php artisan migrate` (not test) ✅
7. Passthrough `./vendor/bin/pest` (not artisan) ✅
8. Passthrough `git status` (not artisan) ✅
9. Diagnostic suggests rewrite with `--teamcity` in correct position ✅

Run: `bash tests/test_teamcity_always_hook.sh` from repo root.

---

## Forthcoming (V2-MVP)

- `anti-silent-deferral` ([#19](https://github.com/altraWeb/laravel-superpowers/issues/19)) — PreToolUse hook on `git push` that scans plan-docs for unresolved "Deferred Items"
- `brainstorm-t1-audit` ([#20](https://github.com/altraWeb/laravel-superpowers/issues/20)) — PostToolUse hook on `superpowers:brainstorming` activation that auto-dispatches the specialist agents (#1-#5)
- `visual-companion-default-on` ([#21](https://github.com/altraWeb/laravel-superpowers/issues/21)) — PostToolUse hook setting the brainstorming visual-companion default per config

See [ROADMAP.md](ROADMAP.md) for the full V2 plan and the broader V2.1/V2.2/V3 roadmap.
