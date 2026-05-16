# Plugin Hooks — Reference

> **Stack:** Laravel + Livewire 4 + Flux Pro v2 + Pest 4. For the Vue 3 + Inertia v2 variant see the planned sibling plugin [`laravel-vue-superpowers`](https://github.com/altraWeb/laravel-vue-superpowers).

`laravel-livewire-superpowers` ships Claude Code hooks that enforce conventions automatically at the right moment in your workflow. Hooks are deterministic — they fire on Claude Code events (`PreToolUse`, `PostToolUse`, `SessionStart`, etc.) and can block, warn, or inject context.

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

### `anti-silent-deferral`

**Event:** `PreToolUse` on `Bash` (filters internally to `git push`).

**What it does:** scans the current branch's plan-docs (`docs/plans/*.md` files changed vs `main`) for `## Phase N — Deferred Items` sections. Blocks the push if any section has uncaptured deferrals — free-form prose or bullets without filed-issue refs.

**Why:** Pilot 2.0 contract requires anti-silent-deferral as a hard-gate Task at the end of every plan (Block 1H Task 6.4, Block 1E Task 4.4). Currently relies on operator memory. This hook automates the gate.

**Section validation:** a section body is **captured** if at least one holds:

- **Empty body** — header followed by blank line / next `##` header
- **Explicit None marker** — `**None — all tasks completed as planned.**` or close variants (`**None.**`, `_None._`, anything matching `None.*tasks completed`)
- **All bullets carry issue refs** — every `-` / `*` bullet contains one of:
  - `#[0-9]+` (GitHub/GitLab issue reference)
  - `gh issue #N` / `glab issue #N`
  - `https://github.com/.../issues/N` / `https://gitlab.com/.../issues/N`

A bullet without an issue ref OR a free-form prose line = uncaptured = block.

**Emergency override:** set `LARAVEL_SUPERPOWERS_ALLOW_UNCAPTURED_DEFERRAL=1` for the single push. The hook logs the override to stderr.

**Per-doc skip marker:** add `<!-- anti-silent-deferral-skip: <reason> -->` anywhere in the plan-doc to bypass validation for that file (useful for WIP plans not ready for push-gate).

**Diagnostic on block:** names the plan-doc, the phase, and the offending lines. Suggests three remediation paths: complete the work + remove section, file each deferral as an issue + use bullets, or mark `None — all tasks completed`.

**Configuration:**

```yaml
hook_enabled:
  anti_silent_deferral: true         # set to false to disable
```

**Failure mode:** fail-open — never blocks a push due to plugin internals. If `main` ref doesn't exist (rare: fresh repo, detached HEAD), hook exits 0 (can't determine branch scope).

**Test evidence:** ships with `tests/test_anti_silent_deferral_hook.sh` — 11 scenarios:
1. Block on free-form prose in Deferred Items ✅
2. Block on bullets without issue refs ✅
3. Allow `**None — all tasks completed**` marker ✅
4. Allow bullets with `#N` issue refs ✅
5. Allow empty section body ✅
6. Passthrough non-push (`git status`) ✅
7. Passthrough `git push --help` ✅
8. Passthrough when no plan-docs on branch ✅
9. Emergency override env var bypass ✅
10. Per-doc skip marker bypass ✅
11. Multi-section detection (Phase 4 captured, Phase 5 uncaptured → blocks naming Phase 5) ✅

Run: `bash tests/test_anti_silent_deferral_hook.sh` from repo root.

---

### `visual-companion-default-on`

**Event:** `PostToolUse` on `Skill` (filters internally to `skill === superpowers:brainstorming`).

**What it does:** when the brainstorming skill is invoked, the hook emits an `additionalContext` reminder into the agent's context that the Visual Companion is default-on per operator memory rule `feedback_visual_companion_default_on`. The reminder lives in the agent's working context for the duration of the brainstorm, nudging it to offer the Companion at Step 2 unless the topic is provably text-only.

**Why:** operator rule (saved 2026-05-14 after Block 1E missed Visual Companion offer): the Companion is default-on for any topic that could benefit from mockups/diagrams/wireframes. Block 1H used it for 4 visual screens; Block 1E rationalized "sounds are auditory" and missed it. This hook prevents the rationalization-skip.

**Default text-only denylist (skip auto-emit when args match, case-insensitive):**

| Pattern | Example match |
|---|---|
| `\bname[d]? vote\b` | "name vote for the new flag" |
| `\bnaming\b` | "naming convention for endpoints" |
| `\brename\b` | "rename UserService to AuthService" |
| `\bsemver\b` | "semver bump strategy" |
| `\bversion bump\b` | "version bump for next release" |
| `\bconfig flag\b` | "config flag for feature X" |
| `\bconfig flip\b` | "config flip rollout" |
| `\bwhich constant\b` | "which constant should we use" |
| `\bnumeric default\b` | "numeric default for timeout" |
| `\benum value\b` | "enum value for status" |

**Spec deviation from issue:** issue #21 asked for "auto-emits Visual Companion offer in own message". The skill spec requires the offer to be "its own message" — a PostToolUse `additionalContext` injection can't strictly guarantee that. Implementation injects a **REMINDER** instead. The agent still issues the actual offer as its own message at Step 2 per the skill spec; the hook just nudges. Documented in spec §7.

**Configuration:**

```yaml
hook_enabled:
  visual_companion_default_on: true     # set to false to disable just the hook

visual_companion_default: on            # top-level: 'on' / 'off' / 'ask'
                                        # 'off' = operator never wants this enforced

visual_companion_default:
  text_only_patterns:                   # extend denylist with project-specific patterns
    - "\\bcompliance\\b"
    - "\\baudit log\\b"
  always_offer_patterns:                # allowlist override — emit even if denylist matches
    - "\\bUI mockup\\b"
```

**Failure mode:** fail-open — silent (exits 0) on any input/config issue. PostToolUse hooks signal via stdout JSON, not exit code. When the hook skips, stdout is empty; the agent's context is unchanged.

**Test evidence:** ships with `tests/test_visual_companion_default_on_hook.sh` — 9 scenarios:
1. `superpowers:brainstorming` activation emits reminder ✅
2. Different skill (e.g., `writing-plans`) passthrough — no emit ✅
3. Naming-vote topic skips (denylist match) ✅
4. Semver-bump topic skips ✅
5. Config-flag topic skips ✅
6. UI-design topic emits reminder ✅
7. Empty args default-emit (cannot detect text-only) ✅
8. Empty stdin → silent ✅
9. Malformed JSON → silent ✅

Run: `bash tests/test_visual_companion_default_on_hook.sh` from repo root.

---

### `brainstorm-t1-audit`

**Event:** `PostToolUse` on `Skill` (filters internally to `skill === superpowers:brainstorming`).

**What it does:** when the brainstorming skill is invoked, the hook emits an `additionalContext` reminder + canonical dispatch prompt template directing the parent agent to dispatch `laravel-best-practices` Agent as a **parallel background task** via the Task tool. The audit runs alongside interactive brainstorming and surfaces best-practice research + anti-patterns + open questions.

**Why:** Pilot 2.0 Tactic 1 (Phase-Start Agent-Audit) is canonical at brainstorm-time. Block 1H + 1E both ran a parallel `laravel-best-practices` Agent alongside `superpowers:brainstorming`, surfacing 11+ sources of best-practice research per brainstorm. If the orchestrator forgets, the brainstorm proceeds without audit (Block 1A retro: "super aber nicht ULTRA"). This hook automates the reminder.

**Spec deviation from issue:** issue asks for "auto-dispatch Agent in background". Hooks cannot invoke agents (architecture constraint — hooks are shell scripts; agent dispatch is a harness primitive). Implementation injects a **REMINDER + canonical dispatch prompt template** instead. The parent agent does the actual Task-tool dispatch when it sees the reminder. 80% of spec value at 10% of complexity. Documented in spec §2 + §8.

**Reminder content includes:**

- Pilot 2.0 Tactic 1 context
- Topic interpolation (from `tool_input.args`, or "detect from conversation context" fallback)
- Canonical dispatch prompt with:
  - Stack-detection instruction (composer.json + package.json)
  - Output expectations: executive summary + per-decision findings (with source-tier citations) + anti-patterns + open questions
  - Search-discipline: at least 3 sources, always include year filter
- Archival instruction: `docs/superpowers/audits/YYYY-MM-DD-<short-topic>-audit.md`
- Opt-out guidance: if skipping, say so explicitly with reason

**Configuration:**

```yaml
hook_enabled:
  brainstorm_t1_audit: true            # set to false to disable

audit_aggressiveness: every-phase      # every-phase | every-commit | brainstorm-only
                                       # all current values include brainstorm-time
                                       # dispatch — forward-compat for future modes
```

**Failure mode:** fail-open — silent on any internal failure.

**Test evidence:** ships with `tests/test_brainstorm_t1_audit_hook.sh` — 5 scenarios:
1. Brainstorming activation emits reminder + Pilot 2.0 + agent name + topic interpolation ✅
2. Different skill (e.g., `writing-plans`) passthrough — no emit ✅
3. Empty args emits with "detect from conversation context" fallback ✅
4. Empty stdin → silent ✅
5. Malformed JSON → silent ✅

Run: `bash tests/test_brainstorm_t1_audit_hook.sh` from repo root.

---

_**All V2-MVP hooks shipped.** See [ROADMAP.md](ROADMAP.md) for V2.1 forthcoming hooks (sprint-state context-injection, master-roadmap drift detector, stale-branch sweep) and the broader V2.2/V3 roadmap._
- `brainstorm-t1-audit` ([#20](https://github.com/altraWeb/laravel-superpowers/issues/20)) — PostToolUse hook on `superpowers:brainstorming` activation that auto-dispatches the specialist agents (#1-#5)
- `visual-companion-default-on` ([#21](https://github.com/altraWeb/laravel-superpowers/issues/21)) — PostToolUse hook setting the brainstorming visual-companion default per config

See [ROADMAP.md](ROADMAP.md) for the full V2 plan and the broader V2.1/V2.2/V3 roadmap.
