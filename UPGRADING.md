# UPGRADING

## V2 → V3

V3 is a major release that renames the plugin and moves the marketplace to a neutral host repo. The plugin functionality is fully backward compatible — only the install URL changes.

### What changed

- **Plugin name:** `laravel-superpowers` → `laravel-livewire-superpowers`
- **Marketplace:** moved from inside the plugin repo to a new neutral host repo `altraWeb/laravel-marketplace`
- **Slash commands:** `/laravel-superpowers:*` → `/laravel-livewire-superpowers:*`
- **No config schema changes** — your `~/.claude/plugins/altraweb-laravel/laravel-superpowers/config.yaml` (if any) continues to apply unchanged after migration

### Why

The plugin was always implicitly Livewire 4 + Flux Pro v2 focused. With a Vue 3 + Inertia v3 sibling plugin (`laravel-vue-superpowers`) now released, the rename makes the stack scope explicit and the two variants symmetric.

### Migration steps

> **Important:** these are slash commands. Run them INSIDE a running Claude Code session. Do NOT prefix with `claude` from your bash shell — the `/plugin` commands only work inside an active session.

```
# 1. Uninstall the V2 plugin
/plugin uninstall laravel-superpowers

# 2. Remove the old marketplace
/plugin marketplace remove altraweb-laravel

# 3. Add the new neutral marketplace
/plugin marketplace add altraWeb/laravel-marketplace

# 4. Install the renamed V3 plugin
/plugin install laravel-livewire-superpowers@altraweb-laravel
```

### Updating muscle memory

Replace any habitual `/laravel-superpowers:status` invocations with `/laravel-livewire-superpowers:status`. The plugin name in CLAUDE.md files, project notes, or shell history that referenced `laravel-superpowers` should be updated to `laravel-livewire-superpowers` (no functional break — just hygiene).

### Verifying the migration

After the four steps above, run (inside Claude Code):

```
/laravel-livewire-superpowers:status
```

Expected: `/status` panel renders cleanly with current sprint state. If the slash command is "not found", the install step did not complete — re-run step 4.

### Troubleshooting

- **Marketplace `altraweb-laravel` already exists after the remove step.** The marketplace name `altraweb-laravel` is reused intentionally by the new host repo. After `/plugin marketplace remove altraweb-laravel` + `/plugin marketplace add altraWeb/laravel-marketplace`, the marketplace re-registers under the same name but pointing at the new repo.
- **Old `/laravel-superpowers:status` still works.** This means the V2 plugin is still installed in parallel. Run `/plugin list` to confirm and `/plugin uninstall laravel-superpowers` to remove.
- **Config not applied to V3 plugin.** The config helper reads `~/.claude/plugins/altraweb-laravel/laravel-superpowers/config.yaml` — V3 keeps the V2 plugin name in the path for backward compatibility (see design spec section 8). If your config seems ignored, run `python3 lib/config.py doctor` to diagnose.
